"""
dashboard_builder.py

High-level helpers that compose multiple visualization and KPI
components into cohesive Streamlit dashboard sections.
"""

import streamlit as st
import pandas as pd
import numpy as np

from modules.visualization.kpi_generator import generate_kpis
from modules.visualization.auto_visualization import auto_generate_charts
from modules.dashboard.layout_manager import render_kpi_row, render_chart_grid
from modules.ai_modules.insight_generator import generate_insights
from utils.logger import app_logger


def build_overview_section(df, dataset_name="dataset"):
    """Renders a full overview section: KPIs + auto charts + top insights."""
    if df is None or df.empty:
        st.info("No dataset loaded.")
        return

    # ── KPI Row ────────────────────────────────────────────────────────
    st.subheader("📊 Key Performance Indicators")
    render_kpi_row(df)
    st.divider()

    # ── Auto Charts ────────────────────────────────────────────────────
    st.subheader("📈 Automated Visualizations")
    charts = auto_generate_charts(df)
    render_chart_grid(charts, cols_per_row=2)
    st.divider()

    # ── Quick Insights ─────────────────────────────────────────────────
    st.subheader("💡 Quick Insights")
    insights = generate_insights(df)
    for ins in insights[:5]:          # top-5 only for overview
        st.markdown(
            f"<div style='background:#1a1f2e; border-left:4px solid #6366f1; "
            f"padding:10px 16px; border-radius:0 8px 8px 0; margin-bottom:8px;'>"
            f"{ins}</div>",
            unsafe_allow_html=True,
        )

    app_logger.info("Dashboard overview section rendered.")
