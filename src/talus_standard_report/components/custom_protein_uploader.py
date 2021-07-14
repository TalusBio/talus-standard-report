"""src/talus_standard_report/components/custom_protein_uploader.py module."""
import pandas as pd
import streamlit as st

from talus_utils.fasta import parse_fasta_header_uniprot_protein


class CustomProteinUploader:
    """Custom protein uploader class."""

    def __init__(self):
        self._uploaded_files = []
        self._data = set()
        self._protein_column = None
        self._use_custom_proteins = False

    def display(self):
        """Display the custom protein uploader."""
        st.sidebar.header("Custom Protein List")
        self._uploaded_files = st.sidebar.file_uploader(
            "Choose a file (.csv)", accept_multiple_files=True
        )
        for uploaded_file in self._uploaded_files:
            custom_df = pd.read_csv(uploaded_file, sep=None)
            st.sidebar.write(uploaded_file.name)
            self._protein_column = st.sidebar.selectbox(
                "Select Protein Column",
                options=list(custom_df.columns),
                key="custom_protein_uploader",
            )
            custom_df[self._protein_column] = custom_df[self._protein_column].apply(
                parse_fasta_header_uniprot_protein
            )
            self._data.update(list(custom_df[self._protein_column].tolist()))

    def display_choice(self, session_key: str):
        """Display the choice whether to use custom proteins or not.

        Parameters
        ----------
        session_key : str
            Session key to create a unique idenitifer in the Streamlit session state.
        """
        if len(self._data) != 0:
            self._use_custom_proteins = st.sidebar.checkbox(
                "Use custom proteins",
                key=f"{session_key}_custom_proteins",
                value=True,
            )

    @property
    def data(self):
        """Getter for data."""
        return self._data

    @property
    def uploaded_files(self):
        """Getter for uploaded_files."""
        return self._uploaded_files

    @property
    def protein_column(self):
        """Getter for protein_column."""
        return self._protein_column

    @property
    def use_custom_proteins(self):
        """Getter for use_custom_proteins."""
        return self._use_custom_proteins
