"""src/talus_standard_report/data_loader.py component."""
import numpy as np
import pandas as pd
import streamlit as st

from talus_aws_utils.s3 import read_dataframe

from .constants import METADATA_BUCKET, EXPERIMENT_BUCKET


@st.cache(allow_output_mutation=True)
def get_unique_peptides_proteins(dataset: str, tool: str) -> pd.DataFrame:
    """Get the unique_peptides_proteins for the given dataset.

    Parameters
    ----------
    dataset : str
        The name of the dataset as it is stored in S3. E.g. '210308_MLLtx'.
    tool : str
        The name of the tool used. E.g. 'encyclopedia'.

    Returns
    -------
    pd.DataFrame
        The unique_peptides_proteins for the given dataset.
    """
    try:
        if st.secrets.get("LOCAL_MODE"):
            return pd.read_parquet("data/unique_peptides_proteins.parquet")
        else:
            try:
                unique_peptides_proteins = read_dataframe(
                    bucket=EXPERIMENT_BUCKET,
                    key=f"{dataset}/{tool}/quant_unique_peptides_proteins.csv",
                )
                unique_peptides_proteins = unique_peptides_proteins.rename(columns={
                    "Run": "Sample Name"
                })
                return unique_peptides_proteins
            except:
                print("No quant_* unique peptides available. Must be old version.")
                return read_dataframe(
                    bucket=EXPERIMENT_BUCKET,
                    key=f"{dataset}/{tool}/unique_peptides_proteins.csv",
                )
    except ValueError:
        return pd.DataFrame()


@st.cache(allow_output_mutation=True)
def get_quant_proteins(dataset: str, tool: str) -> pd.DataFrame:
    """Get the quant_proteins for the given dataset.

    Parameters
    ----------
    dataset : str
        The name of the dataset as it is stored in S3. E.g. '210308_MLLtx'.
    tool : str
        The name of the tool used. E.g. 'encyclopedia'.

    Returns
    -------
    pd.DataFrame
        The quant_proteins for the given dataset.
    """
    try:
        if st.secrets.get("LOCAL_MODE"):
            quant_proteins = pd.read_csv("data/RESULTS-quant.elib.proteins.txt", sep="\t")
        else:
            quant_proteins = read_dataframe(
                bucket=EXPERIMENT_BUCKET,
                key=f"{dataset}/{tool}/result-quant.elib.proteins.txt",
            )
        quant_proteins.columns = [c.replace(".mzML", "") for c in quant_proteins.columns]
        return quant_proteins
    except ValueError:
        return pd.DataFrame()


@st.cache(allow_output_mutation=True)
def get_quant_peptides(dataset: str, tool: str) -> pd.DataFrame:
    """Get the quant_peptides for the given dataset.

    Parameters
    ----------
    dataset : str
        The name of the dataset as it is stored in S3. E.g. '210308_MLLtx'.
    tool : str
        The name of the tool used. E.g. 'encyclopedia'.

    Returns
    -------
    pd.DataFrame
        The quant_peptides for the given dataset.
    """
    try:
        if st.secrets.get("LOCAL_MODE"):
            quant_peptides = pd.read_csv("data/RESULTS-quant.elib.peptides.txt", sep="\t")
        else:
            quant_peptides = read_dataframe(
                bucket=EXPERIMENT_BUCKET,
                key=f"{dataset}/{tool}/result-quant.elib.peptides.txt",
            )
        quant_peptides.columns = [c.replace(".mzML", "") for c in quant_peptides.columns]
        return quant_peptides
    except ValueError:
        return pd.DataFrame()


@st.cache(allow_output_mutation=True)
def get_nuclear_proteins() -> pd.DataFrame:
    """Get the nuclear_proteins for the given dataset.

    Returns
    -------
    pd.DataFrame
        The nuclear_proteins for the given dataset.
    """
    try:
        if st.secrets.get("LOCAL_MODE"):
            return pd.read_csv("data/nuclear_proteins.csv")
        else:
            return read_dataframe(bucket=METADATA_BUCKET, key="protein-collections/nuclear_proteins.csv")
    except ValueError:
        return pd.DataFrame()


@st.cache(allow_output_mutation=True)
def get_expected_fractions_of_locations() -> pd.DataFrame:
    """Get the expected_fractions_of_locations for the given dataset.

    Returns
    -------
    pd.DataFrame
        The expected_fractions_of_locations for the given dataset.
    """
    try:
        if st.secrets.get("LOCAL_MODE"):
            return pd.read_parquet("data/expected_fractions_of_locations.parquet")
        else:
            return read_dataframe(
                bucket=METADATA_BUCKET, key="protein-collections/expected_fractions_of_locations.parquet"
            )
    except ValueError:
        return pd.DataFrame()


@st.cache(allow_output_mutation=True)
def get_protein_locations() -> pd.DataFrame:
    """Get the protein_locations for the given dataset.

    Returns
    -------
    pd.DataFrame
        The protein_locations for the given dataset.
    """
    try:
        if st.secrets.get("LOCAL_MODE"):
            return pd.read_parquet("data/protein_locations.parquet")
        else:
            return read_dataframe(
                bucket=METADATA_BUCKET, key="protein-collections/protein_locations.parquet"
            )
    except ValueError:
        return pd.DataFrame()


@st.cache(allow_output_mutation=True)
def get_metadata(dataset: str, tool: str) -> pd.DataFrame:
    """Get the metadata for the given dataset.

    Parameters
    ----------
    dataset : str
        The name of the dataset as it is stored in S3. E.g. '210308_MLLtx'.
    tool : str
        The name of the tool used. E.g. 'encyclopedia'.

    Returns
    -------
    pd.DataFrame
        The metadata for the given dataset.
    """
    try:
        if st.secrets.get("LOCAL_MODE"):
            return pd.read_csv("data/benchling_metadata.csv")
        else:
            return read_dataframe(
                bucket=EXPERIMENT_BUCKET,
                key=f"{dataset}/{tool}/benchling_metadata.csv",
            )
    except ValueError:
        return pd.DataFrame()
