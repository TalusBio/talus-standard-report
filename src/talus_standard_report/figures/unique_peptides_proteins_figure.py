"""src/talus_standard_report/figures/unique_peptides_proteins_figure.py module."""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from talus_standard_report.constants import PRIMARY_COLOR, SECONDARY_COLOR
from talus_standard_report.utils import get_svg_download_link, get_table_download_link

from .report_figure_abstract_class import ReportFigureAbstractClass


class UniquePeptidesProteinsFigure(ReportFigureAbstractClass):
    """Unique peptides/proteins figure."""

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(
            *args,
            **kwargs,
        )

    def preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Preprocess the data for the figure.

        Parameters
        ----------
        data : pd.DataFrame
            The input dataframe.

        Returns
        -------
        pd.DataFrame
            The processed dataframe.
        """
        return data

    def get_figure(
        self, df: pd.DataFrame, color_proteins: str, color_peptides: str
    ) -> go.Figure:
        """Create a figure for the unique peptides/proteins plot.

        Parameters
        ----------
        df : pd.DataFrame
            The input dataframe.
        color_proteins : str
            The color to use for proteins.
        color_peptides : str
            The color to use for peptides.

        Returns
        -------
        go.Figure
            A Plotly figure.
        """
        return go.Figure(
            data=[
                go.Bar(
                    name="Unique Proteins",
                    x=df["Sample Name"],
                    y=df["Unique Proteins"],
                    marker_color=color_proteins,
                    yaxis="y",
                    offsetgroup=1,
                ),
                go.Bar(
                    name="Unique Peptides",
                    x=df["Sample Name"],
                    y=df["Unique Peptides"],
                    marker_color=color_peptides,
                    yaxis="y2",
                    offsetgroup=2,
                ),
            ],
            layout={
                "yaxis": {"title": "Unique Proteins"},
                "yaxis2": {
                    "title": "Unique Peptides",
                    "overlaying": "y",
                    "side": "right",
                },
                "width": self._width,
                "height": self._height,
            },
        )

    def display(self) -> None:
        """Display the figure."""
        if self._is_active:
            st.header(self._title)
            if self._subheader:
                st.subheader(self._subheader)
            st.sidebar.header(self._short_title)

            st.dataframe(self._data)
            self._figure = self.get_figure(
                df=self._data,
                color_proteins=PRIMARY_COLOR,
                color_peptides=SECONDARY_COLOR,
            )

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
