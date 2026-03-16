import pandas as pd
import numpy as np
from config.api_keys import get_openai_api_key
from utils.logger import app_logger


def generate_dataset_summary(df, dataset_name="dataset"):
    """
    Generates a structured AI-style text summary of the dataset.
    Falls back to a rule-based summary if OpenAI key is not configured.
    """
    if df is None or df.empty:
        return "No dataset available to summarize."

    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    missing_total = int(df.isnull().sum().sum())
    dup_total = int(df.duplicated().sum())

    summary_lines = [
        f"## 📊 Dataset Summary: {dataset_name}",
        "",
        f"- **Total Rows:** {len(df):,}",
        f"- **Total Columns:** {len(df.columns):,}",
        f"- **Numeric Columns ({len(num_cols)}):** {', '.join(num_cols) if num_cols else 'None'}",
        f"- **Categorical Columns ({len(cat_cols)}):** {', '.join(cat_cols) if cat_cols else 'None'}",
        f"- **Missing Values:** {missing_total:,}",
        f"- **Duplicate Rows:** {dup_total:,}",
        "",
        "### 🔢 Numeric Column Highlights",
    ]

    for col in num_cols[:5]:
        summary_lines.append(
            f"  - **{col}**: mean={df[col].mean():.2f}, "
            f"min={df[col].min():.2f}, max={df[col].max():.2f}, "
            f"std={df[col].std():.2f}"
        )

    if cat_cols:
        summary_lines.append("")
        summary_lines.append("### 🗂️ Categorical Column Highlights")
        for col in cat_cols[:5]:
            top_val = df[col].value_counts().idxmax() if not df[col].value_counts().empty else "N/A"
            summary_lines.append(
                f"  - **{col}**: {df[col].nunique()} unique values, "
                f"most frequent = '{top_val}'"
            )

    summary_text = "\n".join(summary_lines)
    app_logger.info("Dataset summary generated.")
    return summary_text
