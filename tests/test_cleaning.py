"""
tests/test_cleaning.py

Unit tests for data processing modules.
"""
import os
import sys
import pytest
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from modules.data_processing.data_cleaner import clean_dataset
from modules.data_processing.data_validator import validate_dataset
from modules.data_processing.data_converter import convert_format


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "Name":   ["Alice", "Bob", "Bob", None, "Charlie"],
        "Age":    [25.0, 30.0, 30.0, None, 28.0],
        "Score":  [88.0, 92.0, 92.0, 70.0, None],
    })


# ─── data_cleaner ────────────────────────────────────────────────────────
def test_clean_removes_duplicates(sample_df):
    cleaned, _, _ = clean_dataset(sample_df)
    assert cleaned.duplicated().sum() == 0


def test_clean_fills_missing_numeric(sample_df):
    cleaned, _, _ = clean_dataset(sample_df)
    assert cleaned["age"].isnull().sum() == 0
    assert cleaned["score"].isnull().sum() == 0


def test_clean_fills_missing_categorical(sample_df):
    cleaned, _, _ = clean_dataset(sample_df)
    assert cleaned["name"].isnull().sum() == 0


def test_clean_standardizes_column_names(sample_df):
    cleaned, _, _ = clean_dataset(sample_df)
    for col in cleaned.columns:
        assert col == col.lower(), f"Column '{col}' is not lowercase"
        assert " " not in col, f"Column '{col}' still contains spaces"


def test_clean_returns_removed_rows(sample_df):
    _, removed, _ = clean_dataset(sample_df)
    # rows that originally had NaN should be captured
    assert removed is not None
    assert len(removed) > 0


def test_clean_empty_df():
    result = clean_dataset(pd.DataFrame())
    assert result is None or result[0] is None or result[0].empty


# ─── data_validator ──────────────────────────────────────────────────────
def test_validate_good_df():
    df = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
    valid, msg = validate_dataset(df)
    assert valid, msg


def test_validate_empty_column():
    df = pd.DataFrame({"a": [1, 2], "b": [None, None]})
    valid, msg = validate_dataset(df)
    assert not valid


def test_validate_empty_df():
    valid, msg = validate_dataset(pd.DataFrame())
    assert not valid


# ─── data_converter ──────────────────────────────────────────────────────
def test_convert_to_csv(tmp_path):
    df = pd.DataFrame({"x": [1, 2], "y": [3, 4]})
    out = str(tmp_path / "out")
    fp = convert_format(df, out, "csv")
    assert fp is not None and fp.endswith(".csv")
    assert os.path.exists(fp)
    loaded = pd.read_csv(fp)
    assert len(loaded) == 2


def test_convert_to_excel(tmp_path):
    df = pd.DataFrame({"x": [1, 2], "y": [3, 4]})
    out = str(tmp_path / "out")
    fp = convert_format(df, out, "excel")
    assert fp is not None and fp.endswith(".xlsx")
    assert os.path.exists(fp)
