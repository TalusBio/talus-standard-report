"""src/talus_standard_report/unique_peptides_proteins_figure.py"""
from typing import Tuple

import numpy as np
import pandas as pd
import plotly.express as px
import shortuuid
import streamlit as st

from plotly.graph_objects import Figure
from talus_utils.dataframe import copy, drop_na, log_scaling, pivot_table

from talus_standard_report.constants import PRIMARY_COLOR

from .components import CustomProteinUploader
from .report_figure_abstract_class import ReportFigureAbstractClass


class UniquePeptidesProteinsFigure(ReportFigureAbstractClass):
    def __init__(
        self,
        title: str,
        short_title: str,
        dataset_name: str,
        data: pd.DataFrame,
        description_placeholder: str,
        width: int,
        height: int,
        subheader: str = None,
    ):
        super().__init__(
            title=title,
            short_title=short_title,
            subheader=subheader,
            dataset_name=dataset_name,
            data=data,
            description_placeholder=description_placeholder,
            width=width,
            height=height,
        )

    def display(self) -> None:
        if self._is_active:
            st.header(self._title)
            if self._subheader:
                st.subheader(self._subheader)
            st.write(self._figure)
            self._description = st.text_area(
                "Description", value=self._description_placeholder, key=shortuuid.uuid()
            )


class SubcellularLocationEnrichmentFigure(ReportFigureAbstractClass):
    def __init__(
        self,
        title: str,
        short_title: str,
        dataset_name: str,
        data: pd.DataFrame,
        description_placeholder: str,
        width: int,
        height: int,
        subheader: str = None,
    ):
        super().__init__(
            title=title,
            short_title=short_title,
            subheader=subheader,
            dataset_name=dataset_name,
            data=data,
            description_placeholder=description_placeholder,
            width=width,
            height=height,
        )

    def display(self) -> None:
        if self._is_active:
            st.header(self._title)
            if self._subheader:
                st.subheader(self._subheader)
            st.sidebar.header(self._short_title)
            # min_max_normalize = st.sidebar.checkbox(
            #     "Use Min-Max Normalization", key=shortuuid.uuid(), value=True
            # )
            st.write(self._figure)
            self._description = st.text_area(
                "Description", value=self._description_placeholder, key=shortuuid.uuid()
            )


class NuclearProteinOverlapFigure(ReportFigureAbstractClass):
    def __init__(
        self,
        title: str,
        short_title: str,
        dataset_name: str,
        data: pd.DataFrame,
        description_placeholder: str,
        width: int,
        height: int,
        subheader: str = None,
    ):
        super().__init__(
            title=title,
            short_title=short_title,
            subheader=subheader,
            dataset_name=dataset_name,
            data=data,
            description_placeholder=description_placeholder,
            width=width,
            height=height,
        )

    def display(self) -> None:
        if self._is_active:
            st.header(self._title)
            if self._subheader:
                st.subheader(self._subheader)
            st.sidebar.header(self._short_title)
            # use_custom_proteins = st.sidebar.checkbox(
            #     "Use custom proteins", key=shortuuid.uuid()
            # )
            st.write(self._figure)
            self._description = st.text_area(
                "Description", value=self._description_placeholder, key=shortuuid.uuid()
            )


class PeptideIntensitiesScatterMatrixFigure(ReportFigureAbstractClass):
    def __init__(
        self,
        title: str,
        short_title: str,
        dataset_name: str,
        data: pd.DataFrame,
        description_placeholder: str,
        width: int,
        height: int,
        subheader: str = None,
    ):
        super().__init__(
            title=title,
            short_title=short_title,
            subheader=subheader,
            dataset_name=dataset_name,
            data=data,
            description_placeholder=description_placeholder,
            width=width,
            height=height,
        )

    @copy
    @drop_na(subset=["Intensity"])
    @pivot_table(index="ProteinName", columns="Condition", values="Intensity")
    # TODO: add as a variable somehow
    @log_scaling(filter_outliers=True)
    def get_figure(
        self,
        df: pd.DataFrame,
        title: str = None,
        color: str = PRIMARY_COLOR,
        opacity: float = None,
    ) -> Figure:
        """Creates a Scatter Matrix Plot using Plotly.

        Args:
            df (pd.DataFrame): input data frame
            title (str): The figure title
            color (str): Color to use for the scatter plot
            opacity (float): Opacity of the points in the plot (default: None)

        Returns:
            fig (Figure): a Plotly figure
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
        if self._is_active:
            st.header(self._title)
            if self._subheader:
                st.subheader(self._subheader)
            st.sidebar.header(self._short_title)
            filter_outliers = st.sidebar.checkbox(
                "Filter outliers", key=shortuuid.uuid()
            )
            opacity = st.sidebar.slider(
                "Point Opacity", min_value=0, max_value=100, value=50
            )
            # TODO: make its own function Preprocessing
            # TODO: use itertools.chain
            self._figure = self.get_figure(
                df=self._data,
                color=PRIMARY_COLOR,
                opacity=opacity / 100,
            )
            st.write(self._figure)
            self._description = st.text_area(
                "Description", value=self._description_placeholder, key=shortuuid.uuid()
            )


class PeptideIntensitiesBoxPlotFigure(ReportFigureAbstractClass):
    def __init__(
        self,
        title: str,
        short_title: str,
        dataset_name: str,
        data: pd.DataFrame,
        description_placeholder: str,
        width: int,
        height: int,
        subheader: str = None,
    ):
        super().__init__(
            title=title,
            short_title=short_title,
            subheader=subheader,
            dataset_name=dataset_name,
            data=data,
            description_placeholder=description_placeholder,
            width=width,
            height=height,
        )

    def display(self) -> None:
        if self._is_active:
            st.header(self._title)
            st.sidebar.header(self._short_title)
            left_column, right_column = st.beta_columns(2)

            if self._subheader[0]:
                left_column.subheader(self._subheader[0])
            # box_filter_outliers = st.sidebar.checkbox(
            #     "Filter outliers (raw)", key=shortuuid.uuid()
            # )
            left_column.write(self._figure[0])
            self._description = left_column.text_area(
                "Description",
                value=self._description_placeholder[0],
                key=shortuuid.uuid(),
            )

            if self._subheader[1]:
                right_column.subheader(self._subheader[1])
            # box_norm_filter_outliers = st.sidebar.checkbox(
            #     "Filter outliers (normalized)", key=shortuuid.uuid()
            # )
            right_column.write(self._figure[1])
            self._description = right_column.text_area(
                "Description",
                value=self._description_placeholder[1],
                key=shortuuid.uuid(),
            )


class NumPeptidesPerProtein(ReportFigureAbstractClass):
    def __init__(
        self,
        title: str,
        short_title: str,
        dataset_name: str,
        data: pd.DataFrame,
        description_placeholder: str,
        width: int,
        height: int,
        subheader: str = None,
    ):
        super().__init__(
            title=title,
            short_title=short_title,
            subheader=subheader,
            dataset_name=dataset_name,
            data=data,
            description_placeholder=description_placeholder,
            width=width,
            height=height,
        )

    def display(self) -> None:
        if self._is_active:
            st.header(self._title)
            if self._subheader:
                st.subheader(self._subheader)
            st.write(self._figure)
            self._description = st.text_area(
                "Description", value=self._description_placeholder, key=shortuuid.uuid()
            )
            with st.beta_expander("Show Descriptive Stats"):
                st.dataframe(self._data.describe())
            st.text("")


class ProteinIntensitiesHeatmap(ReportFigureAbstractClass):
    def __init__(
        self,
        title: str,
        short_title: str,
        dataset_name: str,
        data: pd.DataFrame,
        description_placeholder: str,
        width: int,
        height: int,
        custom_protein_uploader: CustomProteinUploader,
        subheader: str = None,
    ):
        super().__init__(
            title=title,
            short_title=short_title,
            subheader=subheader,
            dataset_name=dataset_name,
            data=data,
            description_placeholder=description_placeholder,
            width=width,
            height=height,
        )
        self._custom_protein_uploader = custom_protein_uploader

    def display(self) -> None:
        if self._is_active:
            # TODO: put this somewhere where it makes sense
            # NUM_PROTEINS = 50

            st.header(self._title)
            if self._subheader:
                st.subheader(self._subheader)
            st.sidebar.header(self._short_title)
            # custom_proteins = self.custom_protein_uploader.data()
            # heatmap_use_custom_proteins = False
            # if len(custom_proteins) != 0:
            # heatmap_use_custom_proteins = st.sidebar.checkbox(
            #     "Use custom proteins", key="heatmap_custom_proteins"
            # )
            # if heatmap_use_custom_proteins:
            #     df_proteins = self._data[self._data.index.isin(custom_proteins)]

            # start = st.sidebar.slider(
            #     "Select start of range (50 proteins)",
            #     min_value=0,
            #     max_value=len(df_proteins) - NUM_PROTEINS,
            # )
            # normalize_val = st.sidebar.radio(
            #     "Select normalization", ["Row", "Column", "None"]
            # )
            st.write(self._figure)
            self._description = st.text_area(
                "Description", value=self._description_placeholder, key=shortuuid.uuid()
            )


class HitSelectionFigure(ReportFigureAbstractClass):
    def __init__(
        self,
        title: str,
        short_title: str,
        dataset_name: str,
        data: pd.DataFrame,
        description_placeholder: str,
        width: int,
        height: int,
        custom_protein_uploader: CustomProteinUploader,
        subheader: str = None,
    ):
        super().__init__(
            title=title,
            short_title=short_title,
            subheader=subheader,
            dataset_name=dataset_name,
            data=data,
            description_placeholder=description_placeholder,
            width=width,
            height=height,
        )
        self._custom_protein_uploader = custom_protein_uploader

    def display(self) -> None:
        if self._is_active:
            # TODO: put this somewhere where it makes sense
            MIN_PEPTIDES = 2
            MAX_NAN_VALUES = 2

            st.header(self._title)
            if self._subheader:
                st.subheader(self._subheader)
            st.sidebar.header(self._short_title)
            custom_proteins = self._custom_protein_uploader.data
            hitselection_use_custom_proteins = False
            if len(custom_proteins) != 0:
                hitselection_use_custom_proteins = st.sidebar.checkbox(
                    "Use custom proteins", key="hitselection_custom_proteins"
                )
            hitselection_split = st.sidebar.checkbox(
                "Split above/below mean", key="split"
            )
            # hitselection_show = st.sidebar.radio(
            #     "Select which Proteins to show", ["All", "Below Mean", "Above Mean"]
            # )
            min_peptides = st.sidebar.number_input(
                "Minimum Number of Peptides for a valid Protein", value=MIN_PEPTIDES
            )
            max_nan_values = st.sidebar.number_input(
                "Maximum Number of NaN values for a Peptide across Samples",
                value=MAX_NAN_VALUES,
            )

            # protein_df = hit_selection(
            #     peptide_df=df_peptides,
            #     min_peptides=min_peptides,
            #     max_nan_values=max_nan_values,
            #     split_above_below=False,
            # )

            # filter for custom proteins
            # if hitselection_use_custom_proteins:
            #     protein_df = protein_df[protein_df.index.isin(custom_proteins)]

            st.write(self._figure)
            self._description = st.text_area(
                "Description", value=self._description_placeholder, key=shortuuid.uuid()
            )


class PeptideIntensitiesPCAPlot(ReportFigureAbstractClass):
    def __init__(
        self,
        title: str,
        short_title: str,
        dataset_name: str,
        data: pd.DataFrame,
        description_placeholder: str,
        width: int,
        height: int,
        subheader: str = None,
    ):
        super().__init__(
            title=title,
            short_title=short_title,
            subheader=subheader,
            dataset_name=dataset_name,
            data=data,
            description_placeholder=description_placeholder,
            width=width,
            height=height,
        )

    def display(self) -> None:
        if self._is_active:
            st.header(self._title)
            if self._subheader:
                st.subheader(self._subheader)

            st.write(self._figure)
            self._description = st.text_area(
                "Description", value=self._description_placeholder, key=shortuuid.uuid()
            )


class PeptideIntensitiesClustergram(ReportFigureAbstractClass):
    def __init__(
        self,
        title: str,
        short_title: str,
        dataset_name: str,
        data: pd.DataFrame,
        description_placeholder: str,
        width: int,
        height: int,
        pca_components: np.array,
        subheader: str = None,
    ):
        super().__init__(
            title=title,
            short_title=short_title,
            subheader=subheader,
            dataset_name=dataset_name,
            data=data,
            description_placeholder=description_placeholder,
            width=width,
            height=height,
        )
        self._pca_components = pca_components

    def display(self) -> None:
        if self._is_active:
            # TODO: put this somewhere where it makes sense
            NUM_PEPTIDES = 150
            st.header(self._title)
            if self._subheader:
                st.subheader(self._subheader)
            st.sidebar.header(self._short_title)
            cluster_selection_method = st.sidebar.selectbox(
                "Sort By",
                ["PCA Most Influential Peptides", "Chronological"],
                key=shortuuid.uuid(),
            )
            if cluster_selection_method == "Chronological":
                # cluster_start = st.sidebar.slider(
                #     f"Select start of range ({NUM_PEPTIDES} peptides at a time)",
                #     min_value=0,
                #     max_value=len(self._data) - NUM_PEPTIDES,
                # )
                # df_clust = self._data.iloc[
                #     cluster_start : cluster_start + NUM_PEPTIDES, :
                # ]
                pass
            else:
                # TODO: add len(pca_dims) instead of magic number
                pca_dim = st.sidebar.selectbox(
                    "PCA Dimension", [i + 1 for i in list(range(2))]
                )
                most_important_features = [
                    (-np.abs(comp)).argsort()[:NUM_PEPTIDES]
                    for comp in self._pca_components
                ]
                # df_clust = self._data.iloc[most_important_features[pca_dim - 1], :]

            st.write(self._figure)
            self._description = st.text_area(
                "Description",
                value=self._description_placeholder.format(
                    NUM_PEPTIDES, cluster_selection_method
                ),
                key=shortuuid.uuid(),
            )
