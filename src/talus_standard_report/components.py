"""src/talus_standard_report/components.py"""
import pandas as pd
import shortuuid
import streamlit as st
from talus_utils.fasta import parse_fasta_header_uniprot_entry


class CustomProteinUploader:
    def __init__(self):
        self._uploaded_files = []
        self._data = None

    def display(self):
        st.sidebar.header("Custom Protein List")
        self._uploaded_files = st.sidebar.file_uploader(
            "Choose a file (.csv)", accept_multiple_files=True
        )
        self._data = set()
        for uploaded_file in self._uploaded_files:
            custom_df = pd.read_csv(uploaded_file, sep=None)
            st.sidebar.write(uploaded_file.name)
            protein_col = st.sidebar.selectbox(
                "Select Protein Column",
                options=list(custom_df.columns),
                key=shortuuid.uuid(),
            )
            custom_df[protein_col] = custom_df[protein_col].apply(
                lambda x: parse_fasta_header_uniprot_entry(x)[0]
            )
            self._data.update(list(custom_df[protein_col].tolist()))

    @property
    def data(self):
        """Getter for data."""
        return self._data

    @property
    def uploaded_files(self):
        """Getter for uploaded_files."""
        return self._uploaded_files
