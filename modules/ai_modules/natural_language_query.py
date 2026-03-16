import pandas as pd
import numpy as np
import re
from utils.logger import app_logger


_CHAT_HISTORY = []


def reset_chat():
    """Clears the in-memory conversation history."""
    global _CHAT_HISTORY
    _CHAT_HISTORY = []


def nl_query(df, question: str, use_openai: bool = False, api_key: str = None):
    """
    Answers a natural-language question about the dataset.

    Strategy:
    1. If an OpenAI key is supplied, delegate to GPT-4 via LangChain/PandasAI.
    2. Otherwise, a rule-based keyword router is used so the chatbot still works without an API key.
    """
    global _CHAT_HISTORY

    if df is None or df.empty:
        return "Please upload a dataset first before asking questions."

    question_lower = question.lower().strip()
    _CHAT_HISTORY.append({"role": "user", "content": question})

    # ── OpenAI / PandasAI path ─────────────────────────────────────────────
    if use_openai and api_key:
        try:
            from pandasai import SmartDataframe
            from pandasai.llm.openai import OpenAI as PandasAI_OpenAI

            llm = PandasAI_OpenAI(api_token=api_key)
            sdf = SmartDataframe(df, config={"llm": llm})
            answer = sdf.chat(question)
            answer = str(answer)
        except Exception as e:
            app_logger.warning(f"PandasAI query failed, falling back to rule-based: {e}")
            answer = _rule_based_query(df, question_lower)
    else:
        answer = _rule_based_query(df, question_lower)

    _CHAT_HISTORY.append({"role": "assistant", "content": answer})
    return answer


# ── Rule-based NLP router ──────────────────────────────────────────────────

def _rule_based_query(df, q: str) -> str:
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    all_cols = [c.lower() for c in df.columns]
    col_map = {c.lower(): c for c in df.columns}

    # ── schema / overview ──
    if any(k in q for k in ["columns", "features", "schema", "fields"]):
        return f"The dataset has **{len(df.columns)}** columns: `{'`, `'.join(df.columns.tolist())}`"

    if any(k in q for k in ["rows", "records", "size", "shape", "how many"]):
        return f"The dataset contains **{len(df):,} rows** and **{len(df.columns)} columns**."

    if any(k in q for k in ["missing", "null", "nan", "empty"]):
        missing = df.isnull().sum()
        miss_str = "\n".join([f"- **{c}**: {v} missing" for c, v in missing.items() if v > 0])
        if miss_str:
            return f"Missing values per column:\n{miss_str}"
        return "✅ No missing values found in the dataset."

    if any(k in q for k in ["duplicate", "duplicates"]):
        dup = df.duplicated().sum()
        return f"There are **{dup:,} duplicate rows** in the dataset."

    if any(k in q for k in ["data types", "dtypes", "type of"]):
        dtype_str = "\n".join([f"- **{c}**: {t}" for c, t in df.dtypes.astype(str).items()])
        return f"Column data types:\n{dtype_str}"

    # ── aggregate questions ──
    for op, func in [("average", "mean"), ("mean", "mean"), ("avg", "mean"),
                     ("sum", "sum"), ("total", "sum"),
                     ("maximum", "max"), ("max", "max"), ("highest", "max"),
                     ("minimum", "min"), ("min", "min"), ("lowest", "min"),
                     ("median", "median"), ("std", "std"), ("standard deviation", "std")]:
        if op in q:
            for col_lower, col_orig in col_map.items():
                if col_lower in q and col_orig in num_cols:
                    val = getattr(df[col_orig], func)()
                    return f"The **{op}** of **{col_orig}** is `{val:,.4f}`."

    # ── unique values ──
    if any(k in q for k in ["unique", "distinct"]):
        for col_lower, col_orig in col_map.items():
            if col_lower in q:
                uniq = df[col_orig].nunique()
                return f"**{col_orig}** has **{uniq:,}** unique values."

    # ── top / most common ──
    if any(k in q for k in ["top", "most common", "frequent", "popular"]):
        for col_lower, col_orig in col_map.items():
            if col_lower in q:
                top = df[col_orig].value_counts().head(5)
                lines = "\n".join([f"- `{k}`: {v}" for k, v in top.items()])
                return f"Top 5 values in **{col_orig}**:\n{lines}"

    # ── describe ──
    if any(k in q for k in ["describe", "statistics", "summary", "stats"]):
        desc = df.describe(include='all').to_string()
        return f"```\n{desc}\n```"

    # ── correlation ──
    if "correlat" in q:
        corr_cols = [c for c in num_cols if c.lower() in q]
        if len(corr_cols) >= 2:
            val = df[corr_cols[0]].corr(df[corr_cols[1]])
            return (f"The Pearson correlation between **{corr_cols[0]}** and "
                    f"**{corr_cols[1]}** is **{val:.4f}**.")
        return "Provide two numeric column names to compute their correlation."

    # ── value filter ──
    pattern = re.compile(r"(where|filter|show|when)\s+(\w+)\s*(=|>|<|is|equals?)\s*(.+)")
    match = pattern.search(q)
    if match:
        col_name = match.group(2)
        op = match.group(3)
        val_raw = match.group(4).strip().strip("'\"")
        orig = col_map.get(col_name.lower())
        if orig:
            try:
                if orig in num_cols:
                    val = float(val_raw)
                    if op in ("=", "is", "equals", "equal"):
                        result = df[df[orig] == val]
                    elif op == ">":
                        result = df[df[orig] > val]
                    elif op == "<":
                        result = df[df[orig] < val]
                    else:
                        result = df[df[orig] == val]
                else:
                    result = df[df[orig].astype(str).str.lower() == val_raw.lower()]

                return (f"Found **{len(result):,} rows** where `{orig} {op} {val_raw}`.\n\n"
                        f"Preview (top 5):\n{result.head(5).to_markdown(index=False)}")
            except Exception:
                pass

    # ── fallback ──
    return (
        "I couldn't find a specific answer for that question using the current dataset. "
        "Try asking about column names, statistics (mean, max, min, sum), missing values, "
        "duplicates, unique values, or correlations. "
        "For more complex questions, please configure your OpenAI API key."
    )


def get_chat_history():
    """Returns the in-memory conversation history."""
    return _CHAT_HISTORY
