"""src/talus_standard_report/data_loader.py"""
import pandas as pd
import streamlit as st
from botocore.exceptions import ClientError

# from talus_aws_utils.s3 import read_dataframe

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
