"""src/talus_standard_report/figures/subcellular_location_enrichment_figure.py module."""
from typing import Optional, Tuple

import gopher
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import streamlit as st
import talus_utils.dataframe as df_utils

from toolz.functoolz import thread_first

from talus_standard_report.constants import PRIMARY_COLOR
from talus_standard_report.utils import get_svg_download_link, get_table_download_link

from .report_figure_abstract_class import ReportFigureAbstractClass


class GOEnrichmentFigure(ReportFigureAbstractClass):
    """GOEnrichmentFigure class."""

    def __init__(
        self,
        metadata,
        *args,
        **kwargs,
    ):
        self._metadata = metadata
        super().__init__(
            *args,
            **kwargs,
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
        accessions = data["Protein"].str.extract(f"\|(.+?)\|", expand=False)
        data = data.set_index(accessions)
        data = data.drop(columns=["Protein", "NumPeptides", "PeptideSequences"], axis=1)
        return data

    def get_figure(
        self,
        df: pd.DataFrame,
        title: Optional[str] = None,
    ) -> go.Figure:
        """Create a bar plot for GO enrichment terms.

        Parameters
        ----------
        df : pd.DataFrame
            The data to plot.
        title : str, optional
            The title of the figure, by default None

        Returns
        -------
        go.Figure
            Bar plot of GO enrichment scores.
        """
        return px.bar(
            df, 
            title=title,
            x="GO Name", 
            y="pvalue (-log10)",
            color="Sample Name",
            barmode="group",
            width=self._width,
            height=self._height,
        )

    def display(self) -> None:
        """Display the figure."""
        if self._is_active:
            st.header(self._title)
            if self._subheader:
                st.subheader(self._subheader)
            st.sidebar.header(self._short_title)

            extraction_fractions = st.sidebar.multiselect(
                "Extraction Fractions", 
                options=set(self._metadata["Extraction Fraction"]),
                key=f"{self._session_key}_extraction_fractions"
            )
            working_compounds = st.sidebar.multiselect(
                "Working Compounds", 
                options=set(self._metadata["Working Compound"]),
                key=f"{self._session_key}_working_compound"
            )
            go_filter_options = [
                "nucleus", 
                "nuclear chromosome", 
                "nucleoplasm", 
                "protein-DNA complex", 
                "transcription regulator complex", 
                "inner mitochondrial membrane protein complex",
                "mitochondrial nucleoid",
                "cell surface",
                "ER to Golgi transport vesicle membrane",
                "organelle membrane",
                "lysosome",
                "cytoplasm",
            ]
            go_filters = st.sidebar.multiselect(
                "GO term filters", 
                options=go_filter_options,
                default=go_filter_options,
                key=f"{self._session_key}_go_filters"
            )

            subset_df = self._data[self._data.columns.intersection(list(self._metadata[(self._metadata["Extraction Fraction"].isin(extraction_fractions)) & (self._metadata["Working Compound"].isin(working_compounds))]["Condition"].unique()))]
            if not subset_df.empty:
                go_enrichment = gopher.test_enrichment(
                    subset_df,
                    aspect="c",
                    go_filters=go_filters, 
                    filter_contaminants=True,
                    progress=False
                )
                results_df = go_enrichment.melt(id_vars="GO Name", value_vars=go_enrichment.columns[3:], value_name="pvalue", var_name="Sample Name")
                results_df["pvalue (-log10)"] = -np.log10(results_df["pvalue"])

                self._figure = thread_first(
                    self.get_figure,
                )(df=results_df)

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
                        df=results_df, downloads_path=self._downloads_path
                    ),
                    unsafe_allow_html=True,
                )
