"""src/talus_standard_report/data_loader.py"""
import numpy as np
import pandas as pd
import streamlit as st

from botocore.exceptions import ClientError


# from talus_aws_utils.s3 import read_dataframe, read_numpy_array

# from .constants import ENCYCLOPEDIA_BUCKET


@st.cache(allow_output_mutation=True, hash_funcs={pd.DataFrame: lambda _: None})
def get_peptide_proteins_result(dataset: str):
    return pd.read_parquet("data/peptide_proteins_results.parquet")
    # return read_dataframe(bucket=ENCYCLOPEDIA_BUCKET, key=f"wide/{dataset}/peptide_proteins_results.parquet")


@st.cache(allow_output_mutation=True, hash_funcs={pd.DataFrame: lambda _: None})
def get_peptide_proteins_normalized(dataset: str):
    return pd.read_parquet("data/peptide_proteins_normalized.parquet")
    # return read_dataframe(bucket=ENCYCLOPEDIA_BUCKET, key=f"wide/{dataset}/peptide_proteins_normalized.parquet")


@st.cache(allow_output_mutation=True, hash_funcs={pd.DataFrame: lambda _: None})
def get_unique_peptides_proteins(dataset: str):
    try:
        return pd.read_parquet("data/unique_peptides_proteins.parquet")
        # return read_dataframe(bucket=ENCYCLOPEDIA_BUCKET, key=f"wide/{dataset}/unique_peptides_proteins.parquet")
    except ClientError:
        return None


@st.cache(allow_output_mutation=True, hash_funcs={pd.DataFrame: lambda _: None})
def get_quant_proteins(dataset: str):
    return pd.read_csv("data/RESULTS-quant.elib.proteins.txt", sep="\t")
    # return read_dataframe(bucket=ENCYCLOPEDIA_BUCKET, key=f"wide/{dataset}/RESULTS-quant.elib.proteins.txt")


@st.cache(allow_output_mutation=True, hash_funcs={pd.DataFrame: lambda _: None})
def get_quant_peptides(dataset: str):
    return pd.read_csv("data/RESULTS-quant.elib.peptides.txt", sep="\t")
    # return read_dataframe(bucket=ENCYCLOPEDIA_BUCKET, key=f"wide/{dataset}/RESULTS-quant.elib.peptides.txt")


@st.cache(allow_output_mutation=True, hash_funcs={pd.DataFrame: lambda _: None})
def get_quant_peptides_pca_reduced(dataset: str):
    return pd.read_parquet("data/quant_peptides_pca_reduced.parquet")
    # return read_dataframe(bucket=ENCYCLOPEDIA_BUCKET, key=f"wide/{dataset}/quant_peptides_pca_reduced.parquet")


@st.cache(allow_output_mutation=True, hash_funcs={pd.DataFrame: lambda _: None})
def get_quant_peptides_pca_components(dataset: str):
    return np.load("data/quant_peptides_pca_components.npy")
    # return read_numpy_array(bucket=ENCYCLOPEDIA_BUCKET, key=f"wide/{dataset}/quant_peptides_pca_components.npy")
