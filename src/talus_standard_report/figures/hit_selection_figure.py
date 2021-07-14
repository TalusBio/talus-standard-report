"""src/talus_standard_report/figures/hit_selection_figure.py module."""
from typing import Dict, Optional, Set, Tuple

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import talus_utils.algorithms as algo_utils
import talus_utils.dataframe as df_utils

from talus_utils.fasta import parse_fasta_header_uniprot_protein
from toolz.functoolz import curry, thread_first

from talus_standard_report.components.custom_protein_uploader import (
    CustomProteinUploader,
)
from talus_standard_report.constants import (
    MAX_NAN_VALUES_HIT_SELECTION,
    MAX_NUM_PROTEINS_HEATMAP,
    MIN_PEPTIDES_HIT_SELECTION,
    PRIMARY_COLOR,
)
from talus_standard_report.utils import get_table_download_link

from .report_figure_abstract_class import ReportFigureAbstractClass


class HitSelectionFigure(ReportFigureAbstractClass):
    """Create a figure showing the hit selection."""

    def __init__(
        self,
        custom_protein_uploader: CustomProteinUploader,
        file_to_condition: Dict[str, str],
        *args,
        **kwargs,
    ):
        self._file_to_condition = file_to_condition
        super().__init__(
            *args,
            **kwargs,
        )
        self._custom_protein_uploader = custom_protein_uploader

    @df_utils.explode(column="Protein", ignore_index=True, sep=";")
    @df_utils.update_column(
        column="Protein", update_func=parse_fasta_header_uniprot_protein
    )
    def preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Preprocess the dataframe for plotting.

        Parameters
        ----------
        data : pd.DataFrame
            The dataframe to preprocess.

        Returns
        -------
        pd.DataFrame
            The preprocessed dataframe.
        """
        data = data.drop(["numFragments"], axis=1)
        return data

    def get_figure(
        self,
        df: pd.DataFrame,
        start_index: Optional[int] = 0,
        custom_proteins: Optional[Set[str]] = None,
        title: Optional[str] = None,
        color: Optional[Tuple[str, str]] = ("#FFFFFF", PRIMARY_COLOR),
        zdim: Tuple[Optional[float], Optional[float]] = (None, None),
    ) -> go.Figure:
        """Create a heatmap showing the hit selection.

        Parameters
        ----------
        df : pd.DataFrame
            The dataframe to plot.
        start_index : Optional[int], optional
            The index to start plotting at, by default 0.
        custom_proteins : Optional[Set[str]], optional
            A set of custom proteins to plot, by default None.
        title : Optional[str], optional
            The title of the figure, by default None.
        color : Optional[Tuple[str, str]], optional
            The color scale to use for the plot, by default ("#FFFFFF", PRIMARY_COLOR)
        zdim : Tuple[Optional[float], Optional[float]], optional
            The z-dimension to use, by default (None, None)

        Returns
        -------
        go.Figure
            The figure to plot.
        """
        # filter for custom proteins if given
        if len(custom_proteins) > 0:
            df = df[df.index.isin(custom_proteins)]

        # filter by start_index
        df = df.iloc[start_index : start_index + MAX_NUM_PROTEINS_HEATMAP]

        return px.imshow(
            df,
            title=title,
            zmin=zdim[0],
            zmax=zdim[1],
            width=self._width,
            height=self._height,
            color_continuous_scale=color,
            aspect="auto",
        )

    def display(self) -> None:
        """Display the figure."""
        if self._is_active:
            st.header(self._title)
            if self._subheader:
                st.subheader(self._subheader)
            st.sidebar.header(self._short_title)

            self._custom_protein_uploader.display_choice(session_key=self._session_key)
            custom_proteins = self._custom_protein_uploader.data
            use_custom_proteins = self._custom_protein_uploader.use_custom_proteins
            if not use_custom_proteins:
                custom_proteins = set()

            start_index = st.sidebar.slider(
                f"Select start of range ({MAX_NUM_PROTEINS_HEATMAP} proteins)",
                min_value=0,
                max_value=self._data.shape[0] - MAX_NUM_PROTEINS_HEATMAP,
                key=f"{self._session_key}_start",
            )
            proteins_to_show = st.sidebar.radio(
                "Select which Proteins to show", ["All", "Below Mean", "Above Mean"]
            )
            min_peptides = st.sidebar.number_input(
                "Minimum Number of Peptides for a valid Protein",
                value=MIN_PEPTIDES_HIT_SELECTION,
            )
            max_nan_values = st.sidebar.number_input(
                "Maximum Number of NaN values for a Peptide across Samples",
                value=MAX_NAN_VALUES_HIT_SELECTION,
            )
            if proteins_to_show.lower() == "above mean":
                protein_df, _ = algo_utils.hit_selection(
                    peptide_df=self._data,
                    min_peptides=min_peptides,
                    max_nan_values=max_nan_values,
                    split_above_below=True,
                )
            elif proteins_to_show.lower() == "below mean":
                _, protein_df = algo_utils.hit_selection(
                    peptide_df=self._data,
                    min_peptides=min_peptides,
                    max_nan_values=max_nan_values,
                    split_above_below=True,
                )
            else:
                protein_df = algo_utils.hit_selection(
                    peptide_df=self._data,
                    min_peptides=min_peptides,
                    max_nan_values=max_nan_values,
                )

            self._figure = thread_first(
                self.get_figure,
                curry(df_utils.sort_row_values(how="max", sort_ascending=False)),
                df_utils.copy,
            )(
                df=protein_df,
                start_index=start_index,
                custom_proteins=custom_proteins,
                zdim=(0.0, 1.0),
            )

            st.write(self._figure)
            self._description = st.text_area(
                "Description",
                value=self._description_placeholder,
                key=f"{self._session_key}_description",
            )

            st.markdown(
                get_table_download_link(
                    df=protein_df, downloads_path=self._downloads_path
                ),
                unsafe_allow_html=True,
            )
