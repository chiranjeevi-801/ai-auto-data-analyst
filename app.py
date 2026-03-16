import streamlit as st
import pandas as pd
import os


from modules.dashboard.layout_manager import render_kpi_row, render_chart_grid, sidebar_navigation
from modules.data_ingestion.file_uploader import handle_upload, register_dataset_in_db
from modules.data_ingestion.url_importer import download_from_url
from modules.data_processing.data_cleaner import clean_dataset
from modules.data_processing.data_validator import validate_dataset
from modules.data_processing.data_converter import convert_format
from modules.analysis.eda_analyzer import basic_eda
from modules.analysis.statistical_analysis import compute_statistics
from modules.analysis.correlation_analysis import compute_correlation_matrix
from modules.visualization.auto_visualization import auto_generate_charts
from modules.visualization.chart_generator import correlation_heatmap
from modules.ai_modules.dataset_summary import generate_dataset_summary
from modules.ai_modules.insight_generator import generate_insights
from modules.ai_modules.natural_language_query import nl_query, reset_chat, get_chat_history
from modules.ai_modules.story_report_generator import generate_html_report, read_report
from modules.recommendation.dataset_recommender import recommend_datasets
from database.db_connection import init_db
from database.data_storage import save_dataframe_to_db
from config import settings
from utils.file_manager import initialize_working_directories
from modules.data_ingestion.kaggle_importer import search_kaggle_datasets, download_kaggle_dataset
from modules.data_ingestion.file_uploader import handle_upload, register_dataset_in_db  


# ── one-time startup ───────────────────────────────────────────────────────
initialize_working_directories()
init_db()

def inject_global_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

        /* Dark page background */
        .stApp { background-color: #0f1117; color: #e0e0e0; }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background: #1a1f2e !important;
            border-right: 1px solid #2d3650;
        }
        section[data-testid="stSidebar"] * { color: #e0e0e0 !important; }

        /* Metric cards */
        [data-testid="metric-container"] {
            background: #1a1f2e;
            border: 1px solid #2d3650;
            border-radius: 12px;
            padding: 16px !important;
        }

        /* Header accents */
        h1 { color: #6366f1 !important; }
        h2 { color: #06b6d4 !important; }
        h3 { color: #a5f3fc !important; }

        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #6366f1, #06b6d4) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            padding: 8px 20px !important;
            transition: opacity 0.2s ease;
        }
        .stButton > button:hover { opacity: 0.85; }

        /* Input / file uploader */
        .stFileUploader, .stTextInput input, .stTextArea textarea {
            background: #1a1f2e !important;
            border: 1px solid #2d3650 !important;
            border-radius: 8px !important;
            color: #e0e0e0 !important;
        }

        /* Expander */
        .streamlit-expanderHeader { color: #6366f1 !important; font-weight: 600; }

        /* Divider */
        hr { border-color: #2d3650; }

        /* Data tables */
        .dataframe thead th { background: #252c3b !important; color: #6366f1 !important; }
        .dataframe tbody tr:hover td { background: #20263a !important; }

        /* Insight boxes */
        .insight-box {
            background: #1a1f2e;
            border-left: 4px solid #6366f1;
            padding: 12px 16px;
            border-radius: 0 8px 8px 0;
            margin-bottom: 10px;
            color: #e0e0e0;
        }

        /* Recommendation cards */
        .rec-card {
            background: #1a1f2e;
            border: 1px solid #2d3650;
            border-radius: 10px;
            padding: 16px;
            margin-bottom: 12px;
        }
        .rec-card h4 { color: #6366f1; margin-bottom: 4px; }
        .rec-card p  { font-size: 0.85rem; color: #9ca3af; margin: 0; }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════
#  Session State Helpers
# ══════════════════════════════════════════════════════════════════════════
def _init_session():
    for key, default in {
        "raw_df": None,
        "cleaned_df": None,
        "removed_rows": None,
        "dataset_name": "dataset",
        "auto_charts": [],
    }.items():
        if key not in st.session_state:
            st.session_state[key] = default


# ══════════════════════════════════════════════════════════════════════════
#  Page: Home
# ══════════════════════════════════════════════════════════════════════════
def page_home():
    st.title(" AI Auto Data Analyst")
    st.markdown("#### *Your intelligent, automated end-to-end data analytics platform*")
    st.divider()

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("###  Ingest Data\nUpload CSV/Excel, import from URL, or search Kaggle datasets.")
    with c2:
        st.markdown("###  AI Analysis\nAutomatic cleaning, EDA, KPIs, charts, and AI-powered insights.")
    with c3:
        st.markdown("###  Report\nGenerate a beautiful storytelling HTML report in one click.")

    st.divider()
    if st.session_state.raw_df is not None:
        st.success(f"✅ Active dataset: **{st.session_state.dataset_name}** "
                   f"({len(st.session_state.raw_df):,} rows × "
                   f"{len(st.session_state.raw_df.columns)} columns)")
    else:
        st.info(" Go to **Data Ingestion** to upload or import a dataset to get started.")


# ══════════════════════════════════════════════════════════════════════════
#  Page: Data Ingestion
# ══════════════════════════════════════════════════════════════════════════
def page_data_ingestion():
    st.title(" Data Ingestion")
    st.divider()

    tab1, tab2, tab3 = st.tabs([" Upload File", " Import from URL", " Kaggle Search"])

    # ── Tab 1: File Upload ────────────────────────────────────────────────
    with tab1:
        uploaded = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx", "xls"])
        if uploaded and st.button("Load Dataset", key="btn_upload"):
            with st.spinner("Loading ..."):
                file_path = handle_upload(uploaded)
                if file_path:
                    df = pd.read_csv(file_path) if uploaded.name.endswith(".csv") else pd.read_excel(file_path)
                    st.session_state.raw_df = df
                    st.session_state.dataset_name = os.path.splitext(uploaded.name)[0]
                    st.session_state.cleaned_df = None
                    st.session_state.auto_charts = []
                    register_dataset_in_db(file_path, uploaded.name, "upload", len(df), len(df.columns))
                    save_dataframe_to_db(df, "raw_dataset")
                    st.success(f"✅ Loaded **{uploaded.name}** — {len(df):,} rows × {len(df.columns)} columns")
                    st.dataframe(df.head(10), use_container_width=True)

    # ── Tab 2: URL Import ─────────────────────────────────────────────────
    with tab2:
        url = st.text_input("Paste a direct CSV URL", placeholder="https://example.com/data.csv")
        fname = st.text_input("Save as filename", value="url_dataset.csv")
        if st.button("Download & Load", key="btn_url") and url:
            with st.spinner("Downloading ..."):
                fp = download_from_url(url, fname)
                if fp:
                    try:
                        df = pd.read_csv(fp) if fp.endswith(".csv") else pd.read_excel(fp)
                        st.session_state.raw_df = df
                        st.session_state.dataset_name = os.path.splitext(fname)[0]
                        st.session_state.cleaned_df = None
                        st.session_state.auto_charts = []
                        st.success(f"✅ Downloaded and loaded — {len(df):,} rows × {len(df.columns)} columns")
                        st.dataframe(df.head(10), use_container_width=True)
                    except Exception as e:
                        st.error(f"Could not parse file: {e}")
                else:
                    st.error("Failed to download the file. Check the URL and try again.")

    # ── Tab 3: Kaggle Search ──────────────────────────────────────────────
    with tab3:
        st.info("ℹ Kaggle import requires **KAGGLE_USERNAME** and **KAGGLE_KEY** set in your `.env` file.")
        query = st.text_input("Search Kaggle datasets", placeholder="e.g. titanic, covid, sales")
        if st.button("Search", key="btn_kaggle") and query:
            with st.spinner("Searching Kaggle ..."):
                try:
                    from modules.data_ingestion.kaggle_importer import search_kaggle_datasets, download_kaggle_dataset
                    results = search_kaggle_datasets(query)
                    if results:
                        for r in results:
                            with st.expander(f" {r['title']} — {r['size']}"):
                                st.write(f"**Ref:** `{r['ref']}`  |  **Votes:** {r['votes']}")
                                if st.button(f"Download {r['ref']}", key=f"dl_{r['ref']}"):
                                    with st.spinner("Downloading ..."):
                                        path = download_kaggle_dataset(r['ref'])
                                        if path:
                                            st.success(f"Downloaded to `{path}` — select the file in the **Upload** tab.")
                    else:
                        st.warning("No datasets found. Try a different search term.")
                except Exception as e:
                    st.error(f"Kaggle search failed: {e}")


# ══════════════════════════════════════════════════════════════════════════
#  Page: Data Processing
# ══════════════════════════════════════════════════════════════════════════
def page_data_processing():
    st.title("🧹 Data Processing")
    st.divider()

    if st.session_state.raw_df is None:
        st.warning("Please upload a dataset first.")
        return

    df = st.session_state.raw_df

    # Validation
    st.subheader("✅ Dataset Validation")
    is_valid, msg = validate_dataset(df)
    if is_valid:
        st.success(f"✅ {msg}")
    else:
        st.warning(f" {msg}")

    st.divider()

    # Cleaning
    st.subheader("🧹 Auto Cleaning")
    if st.button("Run Auto-Cleaner"):
        with st.spinner("Cleaning ..."):
            result = clean_dataset(df)
            cleaned_df, removed_rows, report = result
            st.session_state.cleaned_df = cleaned_df
            st.session_state.removed_rows = removed_rows
            save_dataframe_to_db(cleaned_df, "cleaned_dataset")

            # Save cleaned file
            clean_path = os.path.join(settings.CLEANED_DATA_DIR, f"{st.session_state.dataset_name}_cleaned.csv")
            cleaned_df.to_csv(clean_path, index=False)

           # Save removed rows
            if removed_rows is not None and len(removed_rows) > 0:
                removed_path = os.path.join(settings.CLEANED_DATA_DIR,
                                            f"{st.session_state.dataset_name}_removed_rows.csv")
                removed_rows.to_csv(removed_path, index=False)

            col1, col2, col3 = st.columns(3)
            col1.metric("Duplicates Removed", f"{report['duplicates_removed']:,}")
            col2.metric("Missing Values Handled", "✅" if report["missing_values_handled"] else "❌")
            col3.metric("Columns Standardized", "✅" if report["columns_standardized"] else "❌")
            st.success(f"Cleaned dataset saved to `{clean_path}`")

    if st.session_state.cleaned_df is not None:
        st.divider()
        st.subheader(" Cleaned Dataset Preview")
        st.dataframe(st.session_state.cleaned_df.head(15), use_container_width=True)

        if st.session_state.removed_rows is not None and len(st.session_state.removed_rows) > 0:
            with st.expander(f" Removed / Imputed Rows ({len(st.session_state.removed_rows):,})"):
                st.dataframe(st.session_state.removed_rows.head(20), use_container_width=True)

        st.divider()
        st.subheader(" Export Cleaned Dataset")
        fmt = st.selectbox("Export format", ["CSV", "Excel", "SQL"])
        if st.button("Export"):
            ext_map = {"CSV": "csv", "Excel": "excel", "SQL": "sql"}
            out_path = os.path.join(settings.EXPORTS_DIR, f"{st.session_state.dataset_name}_cleaned")
            fp = convert_format(st.session_state.cleaned_df, out_path, ext_map[fmt])
            if fp:
                st.success(f"Exported to `{fp}`")


# ══════════════════════════════════════════════════════════════════════════
#  Page: EDA & Analysis
# ══════════════════════════════════════════════════════════════════════════
def page_eda():
    st.title(" EDA & Statistical Analysis")
    st.divider()

    active_df = st.session_state.cleaned_df if st.session_state.cleaned_df is not None else st.session_state.raw_df
    if active_df is None:
        st.warning("Please upload a dataset first.")
        return

    eda = basic_eda(active_df)

    # KPI row
    render_kpi_row(active_df)
    st.divider()

    # Summary Statistics
    st.subheader(" Summary Statistics")
    st.dataframe(eda["summary_statistics"], use_container_width=True)

    # Missing values
    st.subheader(" Missing Values")
    missing_df = pd.DataFrame(
        {"Column": list(eda["missing_values"].keys()),
         "Missing Count": list(eda["missing_values"].values())}
    )
    missing_df = missing_df[missing_df["Missing Count"] > 0]
    if missing_df.empty:
        st.success("No missing values found! 🎉")
    else:
        st.dataframe(missing_df, use_container_width=True)

    # Per-column statistics
    st.divider()
    st.subheader(" Column Statistics")
    num_cols = active_df.select_dtypes(include='number').columns.tolist()
    if num_cols:
        chosen = st.selectbox("Select a numeric column", num_cols)
        stats = compute_statistics(active_df, chosen)
        sc = st.columns(4)
        for i, (k, v) in enumerate(stats.items()):
            sc[i % 4].metric(k.capitalize(), f"{v:.4f}" if isinstance(v, float) else str(v))
    else:
        st.info("No numeric columns available for statistics.")

    # Correlation matrix
    st.divider()
    st.subheader(" Correlation Heatmap")
    corr = compute_correlation_matrix(active_df)
    if corr is not None:
        st.plotly_chart(correlation_heatmap(corr), use_container_width=True)
    else:
        st.info("Need at least 2 numeric columns for correlation analysis.")


# ══════════════════════════════════════════════════════════════════════════
#  Page: Visualizations
# ══════════════════════════════════════════════════════════════════════════
def page_visualizations():
    st.title(" Visualizations")
    st.divider()

    active_df = st.session_state.cleaned_df if st.session_state.cleaned_df is not None else st.session_state.raw_df
    if active_df is None:
        st.warning("Please upload a dataset first.")
        return

    if st.button(" Auto-Generate Charts"):
        with st.spinner("Generating charts ..."):
            st.session_state.auto_charts = auto_generate_charts(active_df)

    if st.session_state.auto_charts:
        render_chart_grid(st.session_state.auto_charts, cols_per_row=2)
    else:
        st.info("Click **Auto-Generate Charts** to create visualizations automatically.")


# ══════════════════════════════════════════════════════════════════════════
#  Page: AI Insights
# ══════════════════════════════════════════════════════════════════════════
def page_ai_insights():
    st.title(" AI Insights")
    st.divider()

    active_df = st.session_state.cleaned_df if st.session_state.cleaned_df is not None else st.session_state.raw_df
    if active_df is None:
        st.warning("Please upload a dataset first.")
        return

    # Dataset Summary
    st.subheader(" Dataset Summary")
    summary_md = generate_dataset_summary(active_df, st.session_state.dataset_name)
    st.markdown(summary_md)

    st.divider()

    # Insights
    st.subheader(" Automated Insights")
    insights = generate_insights(active_df)
    for ins in insights:
        st.markdown(f"<div class='insight-box'>{ins}</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
#  Page: Ask the Data (Chatbot)
# ══════════════════════════════════════════════════════════════════════════
def page_chatbot():
    st.title(" Ask the Data")
    st.markdown("*Ask any natural-language question about your dataset.*")
    st.divider()

    active_df = st.session_state.cleaned_df if st.session_state.cleaned_df is not None else st.session_state.raw_df
    if active_df is None:
        st.warning("Please upload a dataset first.")
        return

    # Render past conversation
    for msg in get_chat_history():
        role = " You" if msg["role"] == "user" else " Assistant"
        st.markdown(f"**{role}:** {msg['content']}")

    # Input
    with st.form("chat_form", clear_on_submit=True):
        question = st.text_input("Your question:", placeholder="e.g. What is the average age?")
        col1, col2 = st.columns([4, 1])
        submitted = col1.form_submit_button("Ask")
        cleared = col2.form_submit_button("Clear")

    if cleared:
        reset_chat()
        st.rerun()

    if submitted and question.strip():
        with st.spinner("Thinking ..."):
            answer = nl_query(active_df, question)
        st.markdown(f"** Assistant:** {answer}")
        st.rerun()

    # Suggested prompts
    with st.expander(" Suggested Questions"):
        suggestions = [
            "How many rows does this dataset have?",
            "What columns are in this dataset?",
            "Show me missing values.",
            "What is the average of each numeric column?",
            "What are the top 5 most common values in the first categorical column?",
        ]
        for s in suggestions:
            st.markdown(f"• `{s}`")


# ══════════════════════════════════════════════════════════════════════════
#  Page: Report
# ══════════════════════════════════════════════════════════════════════════
def page_report():
    st.title(" Storytelling Report")
    st.divider()

    active_df = st.session_state.cleaned_df if st.session_state.cleaned_df is not None else st.session_state.raw_df
    if active_df is None:
        st.warning("Please upload a dataset first.")
        return

    if st.button(" Generate Report"):
        with st.spinner("Creating your report ..."):
            path = generate_html_report(active_df, st.session_state.dataset_name)
            if path:
                st.success(f"✅ Report saved to `{path}`")
                html_content = read_report(path)
                if html_content:
                    with st.expander(" Preview Report (HTML)"):
                        st.components.v1.html(html_content, height=700, scrolling=True)
                    st.download_button(
                        label="⬇ Download Report",
                        data=html_content,
                        file_name=os.path.basename(path),
                        mime="text/html"
                    )
            else:
                st.error("Failed to generate the report.")


# ══════════════════════════════════════════════════════════════════════════
#  Page: Recommendations
# ══════════════════════════════════════════════════════════════════════════
def page_recommendations():
    st.title(" Dataset Recommendations")
    st.divider()

    active_df = st.session_state.cleaned_df if st.session_state.cleaned_df is not None else st.session_state.raw_df

    keyword = st.text_input("Search for datasets (optional)", placeholder="e.g. sales, movies, healthcare")
    if st.button("Get Recommendations"):
        recs = recommend_datasets(df=active_df, keyword=keyword if keyword else None)
        if recs:
            for r in recs:
                st.markdown(
                    f"""<div class='rec-card'>
                        <h4> {r['name']}</h4>
                        <p>{r['description']}</p>
                        <p> Kaggle ref: <code>{r['ref']}</code> &nbsp;|&nbsp; Size: <strong>{r['size']}</strong></p>
                    </div>""",
                    unsafe_allow_html=True,
                )
        else:
            st.info("No recommendations found for that search term.")


# ══════════════════════════════════════════════════════════════════════════
#  Main
# ══════════════════════════════════════════════════════════════════════════
def main():
    inject_global_css()
    _init_session()

    page = sidebar_navigation()

    if page == " Home":
        page_home()
    elif page == " Data Ingestion":
        page_data_ingestion()
    elif page == " Data Processing":
        page_data_processing()
    elif page == " EDA & Analysis":
        page_eda()
    elif page == " Visualizations":
        page_visualizations()
    elif page == " AI Insights":
        page_ai_insights()
    elif page == " Ask the Data":
        page_chatbot()
    elif page == " Report":
        page_report()
    elif page == " Recommendations":
        page_recommendations()


if __name__ == "__main__":
    main()
