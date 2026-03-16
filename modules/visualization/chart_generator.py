import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from utils.logger import app_logger


def bar_chart(df, x_col, y_col, title="Bar Chart", color_col=None):
    """Generate an interactive bar chart."""
    fig = px.bar(df, x=x_col, y=y_col, title=title, color=color_col,
                 template="plotly_dark", color_discrete_sequence=px.colors.qualitative.Vivid)
    fig.update_layout(margin=dict(l=30, r=30, t=50, b=30))
    return fig


def line_chart(df, x_col, y_col, title="Line Chart", color_col=None):
    """Generate an interactive line chart."""
    fig = px.line(df, x=x_col, y=y_col, title=title, color=color_col,
                  template="plotly_dark", markers=True)
    fig.update_layout(margin=dict(l=30, r=30, t=50, b=30))
    return fig


def scatter_chart(df, x_col, y_col, title="Scatter Plot", color_col=None, size_col=None):
    """Generate an interactive scatter plot."""
    fig = px.scatter(df, x=x_col, y=y_col, title=title, color=color_col, size=size_col,
                     template="plotly_dark", opacity=0.8,
                     color_discrete_sequence=px.colors.qualitative.Bold)
    fig.update_layout(margin=dict(l=30, r=30, t=50, b=30))
    return fig


def histogram(df, col, title="Histogram", bins=30):
    """Generate an interactive histogram."""
    fig = px.histogram(df, x=col, title=title, nbins=bins,
                       template="plotly_dark",
                       color_discrete_sequence=["#636EFA"])
    fig.update_layout(margin=dict(l=30, r=30, t=50, b=30))
    return fig


def box_plot(df, x_col=None, y_col=None, title="Box Plot", color_col=None):
    """Generate an interactive box plot."""
    fig = px.box(df, x=x_col, y=y_col, title=title, color=color_col,
                 template="plotly_dark",
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_layout(margin=dict(l=30, r=30, t=50, b=30))
    return fig


def pie_chart(df, names_col, values_col, title="Pie Chart"):
    """Generate an interactive pie chart."""
    fig = px.pie(df, names=names_col, values=values_col, title=title,
                 template="plotly_dark", hole=0.3,
                 color_discrete_sequence=px.colors.qualitative.Set3)
    fig.update_layout(margin=dict(l=30, r=30, t=50, b=30))
    return fig


def correlation_heatmap(corr_matrix, title="Correlation Heatmap"):
    """Generate an interactive correlation heatmap."""
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns.tolist(),
        y=corr_matrix.index.tolist(),
        colorscale='RdBu',
        zmid=0,
        text=corr_matrix.round(2).values,
        texttemplate="%{text}",
        textfont={"size": 10}
    ))
    fig.update_layout(
        title=title,
        template="plotly_dark",
        margin=dict(l=30, r=30, t=50, b=30)
    )
    return fig
