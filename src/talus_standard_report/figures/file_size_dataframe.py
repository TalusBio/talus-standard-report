"""src/talus_standard_report/figures/file_sizes_dataframe.py module."""
from pathlib import Path

import pandas as pd
import streamlit as st

from talus_aws_utils.s3 import file_size

from talus_standard_report.constants import RAW_BUCKET
from talus_standard_report.utils import get_table_download_link

from .report_figure_abstract_class import ReportFigureAbstractClass


class FileSizeDataFrame(ReportFigureAbstractClass):
    """Create a dataframe of file sizes."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
        return data[["RAW S3 Path", "Acquisition Type"]].drop_duplicates()

    def get_figure(self) -> pd.DataFrame:
        """Get the figure data.

        Returns
        -------
        pd.DataFrame
            The data to plot.
        """
        size_dicts = []

        for file_key, file_type in zip(self._data["RAW S3 Path"], self._data["Acquisition Type"]):
            if not isinstance(file_key, str):
                continue
            size = file_size(bucket=RAW_BUCKET, key=file_key)
            size_dicts.append(
                {
                    "File": Path(file_key).parts[-1],
                    "Type": file_type,
                    "Size": size,
                }
            )
        return pd.DataFrame(size_dicts).sort_values(by="File").reset_index(drop=True)

    def display(self) -> None:
        """Display the figure."""
        if self._is_active:
            st.header(self._title)
            if self._subheader:
                st.subheader(self._subheader)

            self._data = self.get_figure()
            st.dataframe(self._data)

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
