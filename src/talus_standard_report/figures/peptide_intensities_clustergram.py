"""src/talus_standard_report/figures/peptide_intensities_clustergram.py module."""

from typing import Dict, List

import dash_bio as dashbio
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import talus_utils.dataframe as df_utils

from sklearn.decomposition import PCA
from toolz.functoolz import curry, thread_first

from talus_standard_report.constants import MAX_NUM_PEPTIDES_HEATMAP, PRIMARY_COLOR
from talus_standard_report.utils import get_table_download_link

from .report_figure_abstract_class import ReportFigureAbstractClass


class PeptideIntensitiesClustergram(ReportFigureAbstractClass):
    """Peptide intensities clustergram figure class."""

    def __init__(
        self,
        pca_model: PCA,
        file_to_condition: Dict[str, str],
        *args,
        **kwargs,
    ):
        self._file_to_condition = file_to_condition
        super().__init__(
            *args,
            **kwargs,
        )
        self._pca_model = pca_model

    @df_utils.copy
    def preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Preprocess the dataframe for plotting.

        Parameters
        ----------
        data : pd.DataFrame
            The dataframe to preprocess.

        Returns
        -------
        pd.DataFrame
            The preprocessed dataframe.
        """
        data = data.drop(["Protein", "numFragments"], axis=1)
        data = data.drop_duplicates(subset="Peptide")
        data = data.set_index(["Peptide"])
        # Remove all the columns that are not present in the validation dataframe
        data = data[list(self._file_to_condition.values())]
        return data

    def get_figure(
        self,
        df: pd.DataFrame,
        selected_indices: slice,
        column_labels: List[str] = None,
        cluster: str = "all",
        hide_row_labels: bool = True,
        color: str = PRIMARY_COLOR,
    ) -> go.Figure:
        """Create a clustergram figure using dash-bio.

        Parameters
        ----------
        df : pd.DataFrame
            The dataframe to use for the figure.
        selected_indices : slice
            The dataframe indices to use for the figure.
        column_labels : List[str], optional
            A list of column labels to use for the figure, by default None
        cluster : str, optional
            The cluster method to use, by default "all"
        hide_row_labels : bool, optional
            If True, don't display the row labels, by default True
        color : str, optional
            The color to use for the figure, by default PRIMARY_COLOR

        Returns
        -------
        go.Figure
            The figure object.
        """
        hidden_labels = []
        if hide_row_labels:
            hidden_labels.append("row")

        # filter by selected indices
        df = df.iloc[selected_indices, :]

        fig = dashbio.Clustergram(
            data=df,
            color_threshold={"row": 150, "col": 700},
            column_labels=column_labels,
            row_labels=list(df.index),
            hidden_labels=hidden_labels,
            cluster=cluster,
            width=self._width,
            height=self._height,
            plot_bg_color="#FFFFFF",
            paper_bg_color="#FFFFFF",
            color_map=[
                [0.0, "#FFFFFF"],
                [1.0, color],
            ],
            line_width=2,
        )

        # sort x-axis alphabetically
        if column_labels:
            for axis_obj in fig.layout:
                if "xaxis" in axis_obj and fig.layout[axis_obj]["showticklabels"]:
                    fig.layout[axis_obj]["ticktext"] = sorted(
                        fig.layout[axis_obj]["ticktext"]
                    )

        return fig

    def display(self) -> None:
        """Display the figure."""
        if self._is_active:
            st.header(self._title)
            if self._subheader:
                st.subheader(self._subheader)
            st.sidebar.header(self._short_title)
            cluster_selection_method = st.sidebar.selectbox(
                "Sort By",
                ["PCA Most Influential Peptides", "Chronological"],
                key=f"{self._session_key}_sortby",
            )
            if cluster_selection_method == "Chronological":
                start_index = st.sidebar.slider(
                    f"Select start of range ({MAX_NUM_PEPTIDES_HEATMAP} peptides at a time)",
                    min_value=0,
                    max_value=self._data.shape[0] - MAX_NUM_PEPTIDES_HEATMAP,
                    key=f"{self._session_key}_start",
                )
                selected_indices = slice(
                    start_index, start_index + MAX_NUM_PEPTIDES_HEATMAP
                )
            else:
                pca_dim = st.sidebar.selectbox(
                    "PCA Dimension",
                    [i for i in range(1, self._pca_model.components_.shape[0] + 1)],
                )
                most_important_features = [
                    (-np.abs(component)).argsort()[:MAX_NUM_PEPTIDES_HEATMAP]
                    for component in self._pca_model.components_
                ]
                selected_indices = most_important_features[pca_dim - 1]

            self._figure = thread_first(
                self.get_figure,
                curry(
                    df_utils.log_scaling(log_function=np.log10, filter_outliers=False)
                ),
                df_utils.copy,
            )(
                df=self._data,
                selected_indices=selected_indices,
                column_labels=list(self._data.columns),
            )

            st.write(self._figure)
            self._description = st.text_area(
                "Description",
                value=self._description_placeholder.format(
                    MAX_NUM_PEPTIDES_HEATMAP, cluster_selection_method
                ),
                key=f"{self._session_key}_description",
            )
            st.markdown(
                get_table_download_link(
                    df=self._data, downloads_path=self._downloads_path
                ),
                unsafe_allow_html=True,
            )
