import pandas as pd
import numpy as np
from modules.visualization.chart_generator import (
    bar_chart, histogram, pie_chart, scatter_chart, line_chart, box_plot, correlation_heatmap
)
from modules.analysis.correlation_analysis import compute_correlation_matrix
from utils.logger import app_logger


def auto_generate_charts(df, max_charts=8):
    """
    Intelligently picks the best chart types for a given dataframe
    based on column data types and cardinalities.
    Returns a list of (title, figure) tuples.
    """
    charts = []
    if df is None or df.empty:
        return charts

    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

    # 1. Correlation heatmap (if ≥2 numeric columns)
    if len(num_cols) >= 2:
        corr = compute_correlation_matrix(df)
        if corr is not None:
            charts.append(("Correlation Heatmap", correlation_heatmap(corr)))

    # 2. Histograms for first 3 numeric columns
    for col in num_cols[:3]:
        charts.append((f"Distribution of {col}", histogram(df, col, title=f"Distribution of {col}")))

    # 3. Box plots for numeric columns vs first categorical
    if cat_cols and num_cols:
        cat = cat_cols[0]
        for num in num_cols[:2]:
            if df[cat].nunique() <= 15:
                charts.append((f"{num} by {cat}", box_plot(df, x_col=cat, y_col=num,
                                                            title=f"{num} by {cat}")))

    # 4. Pie chart if a low-cardinality categorical column exists
    if cat_cols and num_cols:
        for cat in cat_cols:
            if 2 <= df[cat].nunique() <= 8:
                grouped = df.groupby(cat)[num_cols[0]].sum().reset_index()
                charts.append((f"{num_cols[0]} by {cat} (Pie)",
                                pie_chart(grouped, names_col=cat, values_col=num_cols[0],
                                          title=f"{num_cols[0]} by {cat}")))
                break

    # 5. Bar chart – top 15 by first numeric, grouped by first categorical
    if cat_cols and num_cols:
        cat = cat_cols[0]
        num = num_cols[0]
        grouped = df.groupby(cat)[num].sum().nlargest(15).reset_index()
        charts.append((f"Top 15 {cat} by {num}",
                        bar_chart(grouped, x_col=cat, y_col=num,
                                  title=f"Top 15 {cat} by {num}")))

    # 6. Scatter plot for first two numeric columns
    if len(num_cols) >= 2:
        charts.append((f"{num_cols[0]} vs {num_cols[1]}",
                        scatter_chart(df, x_col=num_cols[0], y_col=num_cols[1],
                                      title=f"{num_cols[0]} vs {num_cols[1]}",
                                      color_col=cat_cols[0] if cat_cols else None)))

    app_logger.info(f"Auto-generated {len(charts)} charts.")
    return charts[:max_charts]
