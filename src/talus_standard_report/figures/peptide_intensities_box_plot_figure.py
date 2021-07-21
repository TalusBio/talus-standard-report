"""src/talus_standard_report/figures/peptide_intensities_box_plot_figure.py module."""
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import talus_utils.dataframe as df_utils
import talus_utils.plot as plot_utils

from toolz.functoolz import curry, thread_first

from talus_standard_report.constants import PRIMARY_COLOR
from talus_standard_report.utils import get_table_download_link

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
            st.sidebar.header(self._short_title)
            left_column, right_column = st.beta_columns(2)

            # left column
            if self._subheader[0]:
                left_column.subheader(self._subheader[0])
            filter_outliers = st.sidebar.checkbox(
                "Filter outliers (raw)", key=f"{self._session_key}_filter_outliers"
            )
            self._figure = (
                thread_first(
                    self.get_figure,
                    curry(
                        plot_utils.update_layout(
                            xaxis_title="Sample",
                            yaxis_title="log2_intensity",
                            xaxis={"categoryorder": "category ascending"},
                        )
                    ),
                    curry(
                        df_utils.log_scaling(
                            log_function=np.log2, filter_outliers=filter_outliers
                        )
                    ),
                    curry(
                        df_utils.pivot_table(
                            index="ProteinName", columns="Condition", values="Intensity"
                        )
                    ),
                    curry(df_utils.dropna(subset=["Intensity"])),
                    df_utils.copy,
                )(df=self._data[0], color=PRIMARY_COLOR),
            )
            left_column.write(self._figure[0])
            self._description = left_column.text_area(
                "Description",
                value=self._description_placeholder[0],
                key=f"{self._session_key}_description",
            )
            left_column.markdown(
                get_table_download_link(
                    df=self._data[0], downloads_path=self._downloads_path
                ),
                unsafe_allow_html=True,
            )

            # right column
            if self._subheader[1]:
                right_column.subheader(self._subheader[1])
            filter_outliers_norm = st.sidebar.checkbox(
                "Filter outliers (normalized)",
                key=f"{self._session_key}_filter_outliers_norm",
            )
            self._figure = (
                self._figure[0],
                thread_first(
                    self.get_figure,
                    curry(
                        plot_utils.update_layout(
                            xaxis_title="Sample",
                            yaxis_title="log2_intensity",
                            xaxis={"categoryorder": "category ascending"},
                        )
                    ),
                    curry(
                        df_utils.log_scaling(
                            log_function=lambda x: x,
                            filter_outliers=filter_outliers_norm,
                        )
                    ),
                    curry(
                        df_utils.pivot_table(
                            index="PROTEIN",
                            columns="originalRUN",
                            values="ABUNDANCE",
                        )
                    ),
                    curry(df_utils.dropna(subset=["ABUNDANCE"])),
                    df_utils.copy,
                )(df=self._data[1], color=PRIMARY_COLOR),
            )
            right_column.write(self._figure[1])
            self._description = right_column.text_area(
                "Description",
                value=self._description_placeholder[1],
                key=f"{self._session_key}_description_norm",
            )
            right_column.markdown(
                get_table_download_link(
                    df=self._data[1], downloads_path=self._downloads_path
                ),
                unsafe_allow_html=True,
            )
