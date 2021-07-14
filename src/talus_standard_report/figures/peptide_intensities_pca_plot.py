"""src/talus_standard_report/figures/peptide_intensities_pca_plot.py module."""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from talus_standard_report.constants import PRIMARY_COLOR
from talus_standard_report.utils import get_table_download_link

from .report_figure_abstract_class import ReportFigureAbstractClass


class PeptideIntensitiesPCAPlot(ReportFigureAbstractClass):
    """Peptide Intensities PCA Plot."""

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
        """Preprocess the data for plotting.

        Parameters
        ----------
        data : pd.DataFrame
            The dataframe to preprocess.

        Returns
        -------
        pd.DataFrame
            The preprocessed dataframe.
        """
        return data

    def get_figure(
        self,
        df: pd.DataFrame,
        title: str = None,
        color: str = PRIMARY_COLOR,
    ) -> go.Figure:
        """Create a Scatter plot of the PCA values using Plotly.

        Parameters
        ----------
        df : pd.DataFrame
            The input dataframe.
        title : str, optional
            The figure title, by default None
        color : str, optional
            The color to use for the plot, by default PRIMARY_COLOR

        Returns
        -------
        go.Figure
            The Plotly figure.
        """
        color_array = np.full(df.shape[0], color)
        return px.scatter(
            data_frame=df,
            x="pc1",
            y="pc2",
            color=color_array,
            color_discrete_map="identity",
            text="index",
            title=title,
            width=self._width,
            height=self._height,
        )

    def display(self) -> None:
        """Display the figure."""
        if self._is_active:
            st.header(self._title)
            if self._subheader:
                st.subheader(self._subheader)

            self._figure = self.get_figure(
                df=self._data,
                color=PRIMARY_COLOR,
            )

            st.write(self._figure)
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
