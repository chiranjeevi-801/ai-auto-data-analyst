import streamlit as st
import pandas as pd
from modules.visualization.kpi_generator import generate_kpis


def render_kpi_row(df):
    """Renders a row of KPI metric cards from the given dataframe."""
    kpis = generate_kpis(df)
    if not kpis:
        return

    # Display up to 6 KPIs per row
    n = min(len(kpis), 6)
    cols = st.columns(n)
    for i, kpi in enumerate(kpis[:n]):
        with cols[i]:
            st.metric(
                label=f"{kpi.get('icon', '📊')} {kpi['label']}",
                value=kpi['value']
            )


def render_chart_grid(charts, cols_per_row=2):
    """Renders a grid of Plotly figures in a responsive column layout."""
    if not charts:
        st.info("No charts available. Upload a dataset to generate visualizations.")
        return

    for i in range(0, len(charts), cols_per_row):
        row_charts = charts[i: i + cols_per_row]
        col_objects = st.columns(len(row_charts))
        for col, (title, fig) in zip(col_objects, row_charts):
            with col:
                st.plotly_chart(fig, use_container_width=True)


def sidebar_navigation():
    """Renders the fixed sidebar navigation and returns the selected page."""
    with st.sidebar:
        st.markdown(
            """
            <div style='text-align:center; padding: 16px 0 8px;'>
              <span style='font-size:2rem;'>📊</span>
              <p style='font-size:1.1rem; font-weight:700; margin:4px 0 2px; color:#6366f1;'>
                AI Data Analyst
              </p>
              <p style='font-size:0.75rem; color:#9ca3af;'>Automated Analytics Platform</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.divider()

        page = st.radio(
            "Navigate",
            options=[
                "🏠 Home",
                "📂 Data Ingestion",
                "🧹 Data Processing",
                "🔬 EDA & Analysis",
                "📈 Visualizations",
                "🤖 AI Insights",
                "💬 Ask the Data",
                "📄 Report",
                "🔍 Recommendations",
            ],
            label_visibility="collapsed",
        )

        st.divider()
        st.caption("Built with ❤️ using Streamlit + Plotly")

    return page
