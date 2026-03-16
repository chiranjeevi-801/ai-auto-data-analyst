import pandas as pd
import numpy as np
from modules.analysis.correlation_analysis import compute_correlation_matrix, get_top_correlated_pairs
from utils.logger import app_logger


def generate_insights(df):
    """
    Generates a list of actionable data insights from the dataset
    using rule-based heuristics. Returns a list of insight strings.
    """
    if df is None or df.empty:
        return ["No data available for insight generation."]

    insights = []
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

    # 1. Missing data insight
    missing_pct = (df.isnull().sum() / len(df) * 100).round(2)
    high_missing = missing_pct[missing_pct > 10]
    if not high_missing.empty:
        cols_list = ", ".join([f"**{c}** ({v}%)" for c, v in high_missing.items()])
        insights.append(f"⚠️ High missing data detected in: {cols_list}. Consider imputation or removal.")

    # 2. Skewness insight
    for col in num_cols:
        skew = df[col].skew()
        if abs(skew) > 1.5:
            direction = "right (positive)" if skew > 0 else "left (negative)"
            insights.append(f"📐 Column **{col}** is strongly skewed {direction} (skew={skew:.2f}). "
                            f"Log transformation may improve model performance.")

    # 3. Outlier insight using IQR
    for col in num_cols[:5]:
        q1, q3 = df[col].quantile(0.25), df[col].quantile(0.75)
        iqr = q3 - q1
        outliers = df[(df[col] < q1 - 1.5 * iqr) | (df[col] > q3 + 1.5 * iqr)]
        if len(outliers) > 0:
            pct = round(len(outliers) / len(df) * 100, 1)
            insights.append(f"🔍 **{col}** has {len(outliers):,} outliers ({pct}% of data). "
                            f"Review these records before modeling.")

    # 4. High correlation insight
    corr = compute_correlation_matrix(df)
    if corr is not None:
        top_pairs = get_top_correlated_pairs(corr, threshold=0.85)
        for pair in top_pairs[:3]:
            insights.append(f"🔗 Strong correlation ({pair['correlation']}) found between "
                            f"**{pair['feature_a']}** and **{pair['feature_b']}**. "
                            f"Consider dimensionality reduction.")

    # 5. High-cardinality categorical columns
    for col in cat_cols:
        if df[col].nunique() > 50:
            insights.append(f"🏷️ Column **{col}** has very high cardinality "
                            f"({df[col].nunique()} unique values). "
                            f"Consider encoding or grouping rare values.")

    # 6. Low-variance / near-constant columns
    for col in num_cols:
        if df[col].std() < 0.01:
            insights.append(f"📉 Column **{col}** has near-zero variance. "
                            f"It may not contribute to analysis and can be dropped.")

    # 7. Data size note
    if len(df) < 100:
        insights.append("⚡ Dataset is very small (< 100 rows). Statistical results may not be reliable.")
    elif len(df) > 1_000_000:
        insights.append("🚀 Large dataset detected (> 1M rows). Consider sampling for faster exploration.")

    if not insights:
        insights.append("✅ No major issues detected. The dataset appears clean and well-structured.")

    app_logger.info(f"Generated {len(insights)} insights.")
    return insights
