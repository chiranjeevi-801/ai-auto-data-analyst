import pandas as pd
import numpy as np
from utils.logger import app_logger

def compute_correlation_matrix(df, method='pearson'):
    """
    Computes the pairwise correlation matrix for all numeric columns.
    method: 'pearson', 'kendall', 'spearman'
    """
    if df is None or df.empty:
        return None

    num_df = df.select_dtypes(include=[np.number])
    if num_df.shape[1] < 2:
        app_logger.warning("Not enough numeric columns for correlation analysis.")
        return None

    corr_matrix = num_df.corr(method=method)
    app_logger.info(f"Correlation matrix computed using {method} method.")
    return corr_matrix


def get_top_correlated_pairs(corr_matrix, threshold=0.7):
    """
    Returns pairs of features with absolute correlation above the given threshold.
    """
    if corr_matrix is None:
        return []

    pairs = []
    cols = corr_matrix.columns.tolist()
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            val = corr_matrix.iloc[i, j]
            if abs(val) >= threshold:
                pairs.append({
                    'feature_a': cols[i],
                    'feature_b': cols[j],
                    'correlation': round(val, 4)
                })

    pairs_sorted = sorted(pairs, key=lambda x: abs(x['correlation']), reverse=True)
    return pairs_sorted
