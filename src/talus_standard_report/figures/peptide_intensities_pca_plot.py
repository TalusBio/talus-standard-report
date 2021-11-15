"""src/talus_standard_report/figures/peptide_intensities_pca_plot.py module."""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import talus_utils.dataframe as df_utils
import talus_utils.plot as plot_utils

from sklearn.decomposition import PCA
from toolz.functoolz import curry, thread_first
from traitlets.traitlets import default

from talus_standard_report.constants import PRIMARY_COLOR
from talus_standard_report.utils import get_svg_download_link, get_table_download_link

from .report_figure_abstract_class import ReportFigureAbstractClass


class PeptideIntensitiesPCAPlot(ReportFigureAbstractClass):
    """Peptide Intensities PCA Plot."""

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
            The dataframe to preprocess.

        Returns
        -------
        pd.DataFrame
            The preprocessed dataframe.
        """
        data = data.drop(["Protein", "numFragments"], axis=1)
        data = data.set_index(["Peptide"])
        pca_peptides = PCA(n_components=3, random_state=42)
        data_reduced = pca_peptides.fit_transform(data.values.T)
        self._pca_model = pca_peptides
        n_components = data_reduced.shape[1]
        data_reduced_df = pd.DataFrame(
            data_reduced,
            columns=[f"pc{n}" for n in range(1, n_components+1)],
            index=data.columns,
        ).reset_index()
        return data_reduced_df

    def get_figure(
        self,
        df: pd.DataFrame,
        title: str = None,
        color_by=None,
        color: str = PRIMARY_COLOR,
    ) -> go.Figure:
        """Create a Scatter plot of the PCA values using Plotly.

        Parameters
        ----------
        df : pd.DataFrame
            The input dataframe.
        title : str, optional
            The figure title, by default None
        color_by: str, optional
            By which column we color the dots in the plot.
        color : str, optional
            The color to use for the plot, by default PRIMARY_COLOR

        Returns
        -------
        go.Figure
            The Plotly figure.
        """
        color_discrete_map = None
        text = None
        if not color_by:
            color_by = np.full(df.shape[0], color)
            color_discrete_map = "identity"
            text = "index"
        return px.scatter(
            data_frame=df,
            x="pc1",
            y="pc2",
            color=color_by,
            color_discrete_map=color_discrete_map,
            text=text,
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
            st.sidebar.header(self._short_title)

            color_choices = list(self._metadata.columns)
            color_choices.insert(0, None)
            color_by = st.sidebar.selectbox(
                "Color by", 
                options=color_choices,
                index=0,
                key=f"{self._session_key}_color_by"
            )
            if color_by:
                enriched_data = self._data.merge(self._metadata[["Condition", color_by]], left_on="index", right_on="Condition")
            else:
                enriched_data = self._data

            self._figure = thread_first(
                self.get_figure,
                curry(
                    plot_utils.update_layout(
                        xaxis_title=f"Principal Component 1 ({self._pca_model.explained_variance_ratio_[0]*100:.2f}%)",
                        yaxis_title=f"Principal Component 2 ({self._pca_model.explained_variance_ratio_[1]*100:.2f}%)",
                    )
                ),
            )(
                df=enriched_data,
                color_by=color_by,
                color=PRIMARY_COLOR,
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
