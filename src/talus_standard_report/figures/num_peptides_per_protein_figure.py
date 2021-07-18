"""src/talus_standard_report/figures/num_peptides_per_protein.py module."""
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import talus_utils.dataframe as df_utils
import talus_utils.plot as plot_utils

from toolz.functoolz import curry, thread_first

from talus_standard_report.constants import MAX_NUM_PEPTIDES_PER_PROTEIN, PRIMARY_COLOR
from talus_standard_report.utils import get_table_download_link

from .report_figure_abstract_class import ReportFigureAbstractClass


class NumPeptidesPerProteinFigure(ReportFigureAbstractClass):
    """Create a figure that shows the number of peptides per protein."""

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
            The data to preprocess.

        Returns
        -------
        pd.DataFrame
            The preprocessed data.
        """
        data = data[["NumPeptides"]]
        return data.mask(
            data > MAX_NUM_PEPTIDES_PER_PROTEIN, MAX_NUM_PEPTIDES_PER_PROTEIN
        )

    def get_figure(
        self,
        df: pd.DataFrame,
        title: str = None,
        color: str = PRIMARY_COLOR,
    ) -> go.Figure:
        """Create a Histogram Plot using Plotly.

        Parameters
        ----------
        df : pd.DataFrame
            The data to plot.
        title : str, optional
            The figure title, by default None
        color : str, optional
            The color to use for the plot, by default PRIMARY_COLOR

        Returns
        -------
        go.Figure
            The figure object.
        """
        color_array = np.full(df.shape[0], color)
        return px.histogram(
            df,
            color=color_array,
            color_discrete_map="identity",
            title=title,
            nbins=MAX_NUM_PEPTIDES_PER_PROTEIN,
            width=self._width,
            height=self._height,
        )

    def display(self) -> None:
        """Display the figure."""
        if self._is_active:
            st.header(self._title)
            if self._subheader:
                st.subheader(self._subheader)

            self._figure = thread_first(
                self.get_figure,
                curry(
                    plot_utils.update_layout(
                        xaxis_title="# of Peptides",
                        yaxis_title="Number of Proteins",
                        bargap=0.05,
                        bargroupgap=0.05,
                    )
                ),
                df_utils.copy,
            )(df=self._data, color=PRIMARY_COLOR)

            st.write(self._figure)
            self._description = st.text_area(
                "Description",
                value=self._description_placeholder,
                key=f"{self._session_key}_description",
            )
            with st.beta_expander("Show Descriptive Stats"):
                st.dataframe(self._data.describe())
            st.text("")

            st.markdown(
                get_table_download_link(
                    df=self._data, downloads_path=self._downloads_path
                ),
                unsafe_allow_html=True,
            )
