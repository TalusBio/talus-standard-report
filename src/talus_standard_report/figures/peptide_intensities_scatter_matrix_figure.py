"""src/talus_standard_report/figures/peptide_intensities_scatter_matrix_figure.py module."""
from typing import Optional

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import talus_utils.dataframe as df_utils

from toolz.functoolz import curry, thread_first

from talus_standard_report.constants import PRIMARY_COLOR
from talus_standard_report.utils import get_svg_download_link, get_table_download_link

from .report_figure_abstract_class import ReportFigureAbstractClass


class PeptideIntensitiesScatterMatrixFigure(ReportFigureAbstractClass):
    """Create a scatter matrix figure."""

    def __init__(
        self,
        *args,
        **kwargs,
    ):
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
        data = data.drop(["Protein", "numFragments"], axis=1)
        data = data.set_index(["Peptide"])
        return data

    def get_figure(
        self,
        df: pd.DataFrame,
        title: Optional[str] = None,
        color: Optional[str] = PRIMARY_COLOR,
        opacity: Optional[float] = None,
    ) -> go.Figure:
        """Create a Scatter Matrix Plot using Plotly.

        Parameters
        ----------
        df : pd.DataFrame
            The data to plot.
        title : Optional[str], optional
            The title of the figure, by default None.
        color : Optional[str], optional
            The color of the points, by default PRIMARY_COLOR.
        opacity : Optional[float], optional
            The opacity of the points, by default None.

        Returns
        -------
        go.Figure
            The figure object.
        """
        color_array = np.full(df.shape[0], color)
        fig = px.scatter_matrix(
            df,
            dimensions=df.columns,
            color=color_array,
            color_discrete_map="identity",
            opacity=opacity,
            title=title,
            width=self._width,
            height=self._height,
        )
        return fig

    def display(self) -> None:
        """Display the figure."""
        if self._is_active:
            st.header(self._title)
            if self._subheader:
                st.subheader(self._subheader)
            st.sidebar.header(self._short_title)
            filter_outliers = st.sidebar.checkbox(
                "Filter outliers", key=f"{self._session_key}_filter_outliers"
            )
            opacity = st.sidebar.slider(
                "Point Opacity",
                min_value=0,
                max_value=100,
                value=50,
                key=f"{self._session_key}_opacity",
            )
            self._figure = thread_first(
                self.get_figure,
                curry(df_utils.log_scaling(filter_outliers=filter_outliers)),
                df_utils.copy,
            )(df=self._data, color=PRIMARY_COLOR, opacity=opacity/100)
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
