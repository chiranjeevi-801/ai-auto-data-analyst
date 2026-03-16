"""
tests/test_analysis.py

Unit tests for analysis modules: EDA, statistics, and correlation.
"""
import os
import sys
import pytest
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from modules.analysis.eda_analyzer import basic_eda
from modules.analysis.statistical_analysis import compute_statistics
from modules.analysis.correlation_analysis import compute_correlation_matrix, get_top_correlated_pairs


@pytest.fixture
def numeric_df():
    np.random.seed(42)
    return pd.DataFrame({
        "a": np.random.normal(50, 10, 100),
        "b": np.random.normal(20, 5, 100),
        "c": np.random.normal(0, 1, 100),
    })


@pytest.fixture
def mixed_df(numeric_df):
    numeric_df["category"] = np.random.choice(["X", "Y", "Z"], 100)
    return numeric_df


# ─── basic_eda ────────────────────────────────────────────────────────────
def test_eda_returns_expected_keys(mixed_df):
    result = basic_eda(mixed_df)
    for key in ["num_rows", "num_cols", "columns", "dtypes", "missing_values", "head", "summary_statistics"]:
        assert key in result, f"Key '{key}' missing from EDA result"


def test_eda_row_count(mixed_df):
    result = basic_eda(mixed_df)
    assert result["num_rows"] == 100


def test_eda_empty_df():
    result = basic_eda(pd.DataFrame())
    assert result == {}


# ─── compute_statistics ───────────────────────────────────────────────────
def test_stats_mean(numeric_df):
    stats = compute_statistics(numeric_df, "a")
    assert "mean" in stats
    assert abs(stats["mean"] - 50) < 5          # within 5 of the true mean


def test_stats_invalid_column(numeric_df):
    stats = compute_statistics(numeric_df, "nonexistent")
    assert "error" in stats


def test_stats_categorical_column(mixed_df):
    stats = compute_statistics(mixed_df, "category")
    assert "error" in stats


# ─── correlation ──────────────────────────────────────────────────────────
def test_correlation_matrix_shape(numeric_df):
    corr = compute_correlation_matrix(numeric_df)
    assert corr is not None
    assert corr.shape == (3, 3)


def test_correlation_diagonal_is_one(numeric_df):
    corr = compute_correlation_matrix(numeric_df)
    for col in corr.columns:
        assert abs(corr.loc[col, col] - 1.0) < 1e-9


def test_correlation_too_few_columns():
    df = pd.DataFrame({"a": [1, 2, 3]})
    corr = compute_correlation_matrix(df)
    assert corr is None


def test_top_correlated_pairs_threshold(numeric_df):
    # inject a near-perfect correlation
    numeric_df["d"] = numeric_df["a"] * 2 + 1
    corr = compute_correlation_matrix(numeric_df)
    pairs = get_top_correlated_pairs(corr, threshold=0.9)
    assert any(
        (p["feature_a"] == "a" and p["feature_b"] == "d") or
        (p["feature_a"] == "d" and p["feature_b"] == "a")
        for p in pairs
    )
