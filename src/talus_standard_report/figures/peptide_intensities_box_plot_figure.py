"""src/talus_standard_report/figures/peptide_intensities_box_plot_figure.py module."""
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import talus_utils.dataframe as df_utils
from talus_utils.dataframe import median_normalize, quantile_normalize

from toolz.functoolz import curry, thread_first

from talus_standard_report.constants import PRIMARY_COLOR
from talus_standard_report.utils import get_svg_download_link, get_table_download_link

from .report_figure_abstract_class import ReportFigureAbstractClass


class PeptideIntensitiesBoxPlotFigure(ReportFigureAbstractClass):
    """Peptide Intensities Box plot figure class."""

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
        """Preprocesse the data for plotting.

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
        title: str = None,
        color: str = PRIMARY_COLOR,
    ) -> go.Figure:
        """Create a box plot using plotly.

        Parameters
        ----------
        df : pd.DataFrame
            The input dataframe.
        title : str, optional
            The figure tite, by default None
        color : str, optional
            The color to use for the plot, by default PRIMARY_COLOR

        Returns
        -------
        go.Figure
            The figure object.
        """
        color_array = np.full(df.shape[0], color)
        return px.box(
            df,
            color=color_array,
            color_discrete_map="identity",
            title=title,
            points="outliers",
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

            filter_outliers = st.sidebar.checkbox(
                "Filter outliers", value=True, key=f"{self._session_key}_filter_outliers"
            )
            normalization_options = ["Median", "Quantile"]
            normalization_options.insert(0, None)
            normalization = st.sidebar.selectbox(
                "Select Normalization", options=normalization_options, key=f"{self._session_key}_normalization"
            )
            plot_data = self._data
            if normalization and normalization.lower() == "median":
                plot_data = median_normalize(self._data)
            elif normalization and normalization.lower() == "quantile":
                plot_data = quantile_normalize(self._data)

            self._figure = thread_first(
                    self.get_figure,
                    curry(
                        df_utils.log_scaling(
                            log_function=np.log2, filter_outliers=filter_outliers
                        )
                    ),
                    df_utils.copy,
                )(df=plot_data, color=PRIMARY_COLOR)
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
