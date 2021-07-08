"""src/talus_standard_report/unique_peptides_proteins_figure.py"""
import pandas as pd
import shortuuid
import streamlit as st

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
        subheader: str = None,
    ):
        super().__init__(
            title=title,
            short_title=short_title,
            subheader=subheader,
            dataset_name=dataset_name,
            data=data,
            description_placeholder=description_placeholder,
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
        subheader: str = None,
    ):
        super().__init__(
            title=title,
            short_title=short_title,
            subheader=subheader,
            dataset_name=dataset_name,
            data=data,
            description_placeholder=description_placeholder,
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
        subheader: str = None,
    ):
        super().__init__(
            title=title,
            short_title=short_title,
            subheader=subheader,
            dataset_name=dataset_name,
            data=data,
            description_placeholder=description_placeholder,
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
        subheader: str = None,
    ):
        super().__init__(
            title=title,
            short_title=short_title,
            subheader=subheader,
            dataset_name=dataset_name,
            data=data,
            description_placeholder=description_placeholder,
        )

    def display(self) -> None:
        if self._is_active:
            st.header(self._title)
            if self._subheader:
                st.subheader(self._subheader)
            st.sidebar.header(self._short_title)
            # filter_outliers = st.sidebar.checkbox(
            #     "Filter outliers", key=shortuuid.uuid()
            # )
            # opacity = st.sidebar.slider(
            #     "Point Opacity", min_value=0, max_value=100, value=50
            # )
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
        subheader: str = None,
    ):
        super().__init__(
            title=title,
            short_title=short_title,
            subheader=subheader,
            dataset_name=dataset_name,
            data=data,
            description_placeholder=description_placeholder,
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
        subheader: str = None,
    ):
        super().__init__(
            title=title,
            short_title=short_title,
            subheader=subheader,
            dataset_name=dataset_name,
            data=data,
            description_placeholder=description_placeholder,
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
            custom_protein_uploader=custom_protein_uploader,
        )

    def display(self) -> None:
        if self._is_active:
            # TODO: put this somewhere where it makes sense
            # NUM_PROTEINS = 50

            st.header(self._title)
            if self._subheader:
                st.subheader(self._subheader)

            # custom_proteins = self.custom_protein_uploader.data()
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
