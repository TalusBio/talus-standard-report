"""src/talus_standard_report/data_loader.py component."""
import numpy as np
import pandas as pd
import streamlit as st

from talus_aws_utils.s3 import read_dataframe, read_numpy_array

from .constants import COLLECTIONS_BUCKET, ENCYCLOPEDIA_BUCKET


@st.cache(allow_output_mutation=True, hash_funcs={pd.DataFrame: lambda _: None})
def get_peptide_proteins_result(dataset: str) -> pd.DataFrame:
    """Get the peptide_proteins_results for the given dataset.

    Parameters
    ----------
    dataset : str
        The name of the dataset as it is stored in S3. E.g. '210308_MLLtx'.

    Returns
    -------
    pd.DataFrame
        The peptide_proteins_results for the given dataset.
    """
    try:
        if st.secrets.get("LOCAL_MODE"):
            return pd.read_parquet("data/peptide_proteins_results.parquet")
        else:
            return read_dataframe(
                bucket=ENCYCLOPEDIA_BUCKET,
                key=f"wide/{dataset}/peptide_proteins_results.parquet",
            )
    except ValueError:
        return pd.DataFrame()


@st.cache(allow_output_mutation=True, hash_funcs={pd.DataFrame: lambda _: None})
def get_peptide_proteins_normalized(dataset: str) -> pd.DataFrame:
    """Get the peptide_proteins_normalized for the given dataset.

    Parameters
    ----------
    dataset : str
        The name of the dataset as it is stored in S3. E.g. '210308_MLLtx'.

    Returns
    -------
    pd.DataFrame
        The peptide_proteins_normalized for the given dataset.
    """
    try:
        if st.secrets.get("LOCAL_MODE"):
            return pd.read_parquet("data/peptide_proteins_normalized.parquet")
        else:
            return read_dataframe(
                bucket=ENCYCLOPEDIA_BUCKET,
                key=f"wide/{dataset}/peptide_proteins_normalized.parquet",
            )
    except ValueError:
        return pd.DataFrame()


@st.cache(allow_output_mutation=True, hash_funcs={pd.DataFrame: lambda _: None})
def get_unique_peptides_proteins(dataset: str) -> pd.DataFrame:
    """Get the unique_peptides_proteins for the given dataset.

    Parameters
    ----------
    dataset : str
        The name of the dataset as it is stored in S3. E.g. '210308_MLLtx'.

    Returns
    -------
    pd.DataFrame
        The unique_peptides_proteins for the given dataset.
    """
    try:
        if st.secrets.get("LOCAL_MODE"):
            return pd.read_parquet("data/unique_peptides_proteins.parquet")
        else:
            return read_dataframe(
                bucket=ENCYCLOPEDIA_BUCKET,
                key=f"wide/{dataset}/unique_peptides_proteins.parquet",
            )
    except ValueError:
        return pd.DataFrame()


@st.cache(allow_output_mutation=True, hash_funcs={pd.DataFrame: lambda _: None})
def get_quant_proteins(dataset: str) -> pd.DataFrame:
    """Get the quant_proteins for the given dataset.

    Parameters
    ----------
    dataset : str
        The name of the dataset as it is stored in S3. E.g. '210308_MLLtx'.

    Returns
    -------
    pd.DataFrame
        The quant_proteins for the given dataset.
    """
    try:
        if st.secrets.get("LOCAL_MODE"):
            return pd.read_csv("data/RESULTS-quant.elib.proteins.txt", sep="\t")
        else:
            return read_dataframe(
                bucket=ENCYCLOPEDIA_BUCKET,
                key=f"wide/{dataset}/RESULTS-quant.elib.proteins.txt",
            )
    except ValueError:
        return pd.DataFrame()


@st.cache(allow_output_mutation=True, hash_funcs={pd.DataFrame: lambda _: None})
def get_quant_peptides(dataset: str) -> pd.DataFrame:
    """Get the quant_peptides for the given dataset.

    Parameters
    ----------
    dataset : str
        The name of the dataset as it is stored in S3. E.g. '210308_MLLtx'.

    Returns
    -------
    pd.DataFrame
        The quant_peptides for the given dataset.
    """
    try:
        if st.secrets.get("LOCAL_MODE"):
            return pd.read_csv("data/RESULTS-quant.elib.peptides.txt", sep="\t")
        else:
            return read_dataframe(
                bucket=ENCYCLOPEDIA_BUCKET,
                key=f"wide/{dataset}/RESULTS-quant.elib.peptides.txt",
            )
    except ValueError:
        return pd.DataFrame()


@st.cache(allow_output_mutation=True, hash_funcs={pd.DataFrame: lambda _: None})
def get_quant_peptides_pca_reduced(dataset: str) -> pd.DataFrame:
    """Get the quant_peptides_pca_reduced for the given dataset.

    Parameters
    ----------
    dataset : str
        The name of the dataset as it is stored in S3. E.g. '210308_MLLtx'.

    Returns
    -------
    pd.DataFrame
        The quant_peptides_pca_reduced for the given dataset.
    """
    try:
        if st.secrets.get("LOCAL_MODE"):
            return pd.read_parquet("data/quant_peptides_pca_reduced.parquet")
        else:
            return read_dataframe(
                bucket=ENCYCLOPEDIA_BUCKET,
                key=f"wide/{dataset}/quant_peptides_pca_reduced.parquet",
            )
    except ValueError:
        return pd.DataFrame()


@st.cache(allow_output_mutation=True, hash_funcs={np.array: lambda _: None})
def get_quant_peptides_pca_components(dataset: str) -> np.array:
    """Get the quant_peptides_pca_components for the given dataset.

    Parameters
    ----------
    dataset : str
        The name of the dataset as it is stored in S3. E.g. '210308_MLLtx'.

    Returns
    -------
    pd.DataFrame
        The quant_peptides_pca_components for the given dataset.
    """
    try:
        if st.secrets.get("LOCAL_MODE"):
            return np.load("data/quant_peptides_pca_components.npy")
        else:
            return read_numpy_array(
                bucket=ENCYCLOPEDIA_BUCKET,
                key=f"wide/{dataset}/quant_peptides_pca_components.npy",
            )
    except ValueError:
        return np.array([])


@st.cache(allow_output_mutation=True, hash_funcs={pd.DataFrame: lambda _: None})
def get_nuclear_proteins() -> pd.DataFrame:
    """Get the nuclear_proteins for the given dataset.

    Parameters
    ----------
    dataset : str
        The name of the dataset as it is stored in S3. E.g. '210308_MLLtx'.

    Returns
    -------
    pd.DataFrame
        The nuclear_proteins for the given dataset.
    """
    try:
        if st.secrets.get("LOCAL_MODE"):
            return pd.read_csv("data/nuclear_proteins.csv")
        else:
            return read_dataframe(bucket=COLLECTIONS_BUCKET, key="nuclear_proteins.csv")
    except ValueError:
        return pd.DataFrame()


@st.cache(allow_output_mutation=True, hash_funcs={pd.DataFrame: lambda _: None})
def get_expected_fractions_of_locations() -> pd.DataFrame:
    """Get the expected_fractions_of_locations for the given dataset.

    Parameters
    ----------
    dataset : str
        The name of the dataset as it is stored in S3. E.g. '210308_MLLtx'.

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
                bucket=COLLECTIONS_BUCKET, key="expected_fractions_of_locations.parquet"
            )
    except ValueError:
        return pd.DataFrame()


@st.cache(allow_output_mutation=True, hash_funcs={pd.DataFrame: lambda _: None})
def get_protein_locations() -> pd.DataFrame:
    """Get the protein_locations for the given dataset.

    Parameters
    ----------
    dataset : str
        The name of the dataset as it is stored in S3. E.g. '210308_MLLtx'.

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
                bucket=COLLECTIONS_BUCKET, key="protein_locations.parquet"
            )
    except ValueError:
        return pd.DataFrame()
