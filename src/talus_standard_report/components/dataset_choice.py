"""src/talus_standard_report/components/dataset_choice.py module."""
from pathlib import Path
from typing import Optional

import streamlit as st

from talus_aws_utils.s3 import file_keys_in_bucket

from talus_standard_report.constants import SELECTBOX_DEFAULT


class DatasetChoice:
    """A class to handle the dataset choice."""

    def __init__(
        self, bucket: str, key: str, filename_filter: str, file_type: Optional[str] = ""
    ):
        """Create a dataset choice selectbox.

        Parameters
        ----------
        bucket : str
            The bucket to search for files.
        key : str
            The key to search for files.
        filename_filter : str
            The filename that each subfolder needs to have in order to be considered.
        file_type : str, optional
            The file type to filter on. (Default value = "").
        """
        self._dataset = None
        self._dataset_choices = [
            Path(file).parts[0]
            for file in file_keys_in_bucket(bucket=bucket, key=key, file_type=file_type)
            if filename_filter in file
        ]
        self._dataset_choices.insert(0, SELECTBOX_DEFAULT)

    def display(self):
        """Display the dataset choice."""
        self._dataset = st.sidebar.selectbox("Dataset", options=self._dataset_choices)

    @property
    def dataset(self):
        """Getter for dataset."""
        return self._dataset
