"""tests/test_utils module."""
import json

from pathlib import Path

import pandas as pd

from deepdiff import DeepDiff

from talus_standard_report.utils import get_file_to_condition_map


DATA_DIR = Path(__file__).resolve().parent.joinpath("data")

METADATA = pd.read_csv(DATA_DIR.joinpath("benchling_metadata.csv"))
PEPTIDE_PROTEINS_RESULTS = pd.read_parquet(
    DATA_DIR.joinpath("peptide_proteins_results.parquet")
)


def test_get_file_to_condition_mapper() -> None:
    """Test get_file_to_condition_mapper()."""
    dict_expected = json.load(DATA_DIR.joinpath("file_to_condition_map.json").open())
    dict_actual = get_file_to_condition_map(
        peptide_proteins_results=PEPTIDE_PROTEINS_RESULTS, metadata=METADATA
    )

    print(dict_expected)
    print(dict_actual)

    assert DeepDiff(dict_actual, dict_expected, ignore_order=True) == {}
