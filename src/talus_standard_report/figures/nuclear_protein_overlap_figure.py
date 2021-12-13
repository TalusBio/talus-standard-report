"""src/talus_standard_report/figures/nuclear_protein_overlap_figure.py module."""
from typing import Set, Tuple

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import talus_utils.dataframe as df_utils

from talus_utils.fasta import parse_fasta_header_uniprot_protein
from talus_utils.plot import venn

from talus_standard_report.components.custom_protein_uploader import (
    CustomProteinUploader,
)
from talus_standard_report.constants import PRIMARY_COLOR, SECONDARY_COLOR

from .report_figure_abstract_class import ReportFigureAbstractClass


class NuclearProteinOverlapFigure(ReportFigureAbstractClass):
    """Create a figure of the overlap between the nuclear proteins and the custom proteins."""

    def __init__(
        self,
        nuclear_proteins: pd.DataFrame,
        custom_protein_uploader: CustomProteinUploader,
        *args,
        **kwargs,
    ):
        super().__init__(
            *args,
            **kwargs,
        )
        self._nuclear_proteins = nuclear_proteins
        self._custom_protein_uploader = custom_protein_uploader

    def preprocess_data(self, data: pd.DataFrame) -> Set:
        """Preprocess the data to be used in this figure.

        Parameters
        ----------
        data : pd.DataFrame
            The data to be used in this figure.

        Returns
        -------
        Set
            The set of proteins to be used in this figure.
        """
        return set(data["Protein"].str.extract("\|.[^;]*\|(?P<Protein>.+?)_*", expand=False))

    def get_figure(
        self,
        measured_proteins: Set,
        custom_proteins: Set,
        labels: Tuple[str, str],
        title: str = None,
        colors: Tuple[str, str] = (PRIMARY_COLOR, SECONDARY_COLOR),
    ) -> go.Figure:
        """Create a Venn Diagram Overlap Plot using Matplotlib and Plotly.

        Parameters
        ----------
        measured_proteins : Set
            Proteins measured in our experiment.
        custom_proteins : Set
            Custom Proteins to compare to.
        labels : Tuple[str, str]
            The labels for our measured and custom proteins.
        title : str, optional
            The figure title, by default None
        colors : Tuple[str, str], optional
            The colors for each set, by default (PRIMARY_COLOR, SECONDARY_COLOR)

        Returns
        -------
        go.Figure
            The figure object.
        """
        return venn(
            sets=[custom_proteins, measured_proteins],
            labels=labels,
            colors=colors,
            title=title,
            dim=(self._width, self._height),
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
                protein_column = self._nuclear_proteins.columns[-1]
                custom_proteins = set(self._nuclear_proteins[protein_column].unique())

            self._figure = self.get_figure(
                measured_proteins=self._data,
                custom_proteins=custom_proteins,
                labels=[protein_column, "Measured Proteins"],
            )
            st.write(self._figure)
            self._description = st.text_area(
                "Description",
                value=self._description_placeholder,
                key=f"{self._session_key}_description",
            )
