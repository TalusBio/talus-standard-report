"""src/talus_standard_report/figures/subcellular_location_enrichment_figure.py module."""
from typing import Optional, Tuple

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import talus_utils.algorithms as algo_utils
import talus_utils.dataframe as df_utils

from talus_utils.fasta import parse_fasta_header_uniprot_protein
from toolz.functoolz import curry, thread_first

from talus_standard_report.constants import MAX_NUM_PROTEINS_HEATMAP, PRIMARY_COLOR
from talus_standard_report.utils import get_table_download_link

from .report_figure_abstract_class import ReportFigureAbstractClass


class SubcellularLocationEnrichmentFigure(ReportFigureAbstractClass):
    """SubcellularLocationEnrichmentFigure class."""

    def __init__(
        self,
        protein_locations: pd.DataFrame,
        expected_fractions_of_locations: pd.DataFrame,
        *args,
        **kwargs,
    ):
        self._protein_locations = protein_locations
        super().__init__(
            *args,
            **kwargs,
        )
        self._expected_fractions_of_locations = expected_fractions_of_locations

    @df_utils.update_column(
        column="PROTEIN", update_func=parse_fasta_header_uniprot_protein
    )
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
        data = data[data["ABUNDANCE"] > 0.0]
        data = data[["PROTEIN", "originalRUN"]]
        data.columns = ["Protein", "Sample"]
        data = data.drop_duplicates()

        data = pd.merge(
            data,
            self._protein_locations,
            left_on="Protein",
            right_on="Entry name",
            how="left",
        )
        data = data.drop("Entry name", axis=1)
        return data

    def get_figure(
        self,
        df: pd.DataFrame,
        start_index: Optional[int] = 0,
        title: Optional[str] = None,
        color: Optional[Tuple[str, str]] = ("#FFFFFF", PRIMARY_COLOR),
    ) -> go.Figure:
        """Create a heatmap of the subcellular location enrichment scores.

        Parameters
        ----------
        df : pd.DataFrame
            The data to plot.
        start_index : int, optional
            The index to start plotting at, by default 0.
        title : str, optional
            The title of the figure, by default None
        color : Tuple[str, str], optional
            [description], by default ("#FFFFFF", PRIMARY_COLOR)

        Returns
        -------
        go.Figure
            [description]
        """
        # filter by start_index
        df = df.iloc[start_index : start_index + MAX_NUM_PROTEINS_HEATMAP]

        return px.imshow(
            df,
            title=title,
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

            start_index = st.sidebar.slider(
                f"Select start of range ({MAX_NUM_PROTEINS_HEATMAP} proteins)",
                min_value=0,
                max_value=self._data.shape[0] - MAX_NUM_PROTEINS_HEATMAP,
                key=f"{self._session_key}_start",
            )
            min_max_normalize = st.sidebar.checkbox(
                "Use Min-Max Normalization",
                key=f"{self._session_key}_min_max_norm",
                value=True,
            )

            enrichment_scores = algo_utils.subcellular_enrichment_scores(
                proteins_with_locations=self._data,
                expected_fractions_of_locations=self._expected_fractions_of_locations,
            )

            normalize_func = lambda x: x
            if min_max_normalize:
                normalize_func = df_utils.normalize(how="minmax")

            self._figure = thread_first(
                self.get_figure,
                curry(normalize_func),
                df_utils.copy,
            )(df=enrichment_scores, start_index=start_index)

            st.write(self._figure)
            self._description = st.text_area(
                "Description",
                value=self._description_placeholder,
                key=f"{self._session_key}_description",
            )
            st.markdown(
                get_table_download_link(
                    df=enrichment_scores, downloads_path=self._downloads_path
                ),
                unsafe_allow_html=True,
            )
