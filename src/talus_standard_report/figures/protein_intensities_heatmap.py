"""src/talus_standard_report/figures/protein_intensities_heatmap.py module."""
from typing import Optional, Set, Tuple

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import talus_utils.dataframe as df_utils

from talus_utils.fasta import parse_fasta_header_uniprot_protein
from toolz.functoolz import curry, thread_first

from talus_standard_report.components.custom_protein_uploader import (
    CustomProteinUploader,
)
from talus_standard_report.constants import MAX_NUM_PROTEINS_HEATMAP, PRIMARY_COLOR
from talus_standard_report.utils import get_svg_download_link, get_table_download_link

from .report_figure_abstract_class import ReportFigureAbstractClass


class ProteinIntensitiesHeatmap(ReportFigureAbstractClass):
    """Protein intensities heatmap figure class."""

    def __init__(
        self,
        custom_protein_uploader: CustomProteinUploader,
        *args,
        **kwargs,
    ):
        super().__init__(
            *args,
            **kwargs,
        )
        self._custom_protein_uploader = custom_protein_uploader

    @df_utils.copy
    def preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Preprocess the data for plotting.

        Parameters
        ----------
        data : pd.DataFrame
            The data to preprocess.

        Returns
        -------
        pd.DataFrame
            The preprocessed data.
        """
        # This suddenly stopped working
        # protein = data["Protein"].str.extractall("\|.[^;]*\|(?P<Protein>.+?)_*").reset_index(level=[0,1]).groupby("level_0")["Protein"].apply(lambda p: ";".join(p.astype(str)))
        data["Protein"] = data["Protein"].apply(lambda p: p.split("|")[-1].split("_")[0])
        data = data.drop(columns=["NumPeptides", "PeptideSequences"], axis=1)
        data = data.set_index("Protein")
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
            normalize_val = st.sidebar.radio(
                "Select normalization",
                ["Row", "Column", "None"],
                key=f"{self._session_key}_normalize",
            )
            normalize_func = lambda x: x
            if normalize_val in set(["Row", "Column"]):
                normalize_func = df_utils.normalize(how=normalize_val)

            self._figure = thread_first(
                self.get_figure,
                # curry(df_utils.sort_row_values(how="max")),
                curry(normalize_func),
                df_utils.copy,
            )(df=self._data, start_index=start_index, custom_proteins=custom_proteins)

            st.write(self._figure)
            st.markdown(
                get_svg_download_link(
                    fig=self._figure, downloads_path=self._downloads_path
                ),
                unsafe_allow_html=True,
            )

            self._description = st.text_area(
                "Description",
                value=self._description_placeholder,
                key=f"{self._session_key}_description",
            )
            st.markdown(
                get_table_download_link(
                    df=self._data, downloads_path=self._downloads_path
                ),
                unsafe_allow_html=True,
            )
