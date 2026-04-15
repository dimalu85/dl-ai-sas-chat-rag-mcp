"""Plotly charts for natural disaster data visualisation."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.config import CSV_PATH


def load_disaster_df(csv_path=CSV_PATH) -> pd.DataFrame:
    """Load the disaster CSV as a DataFrame."""
    return pd.read_csv(csv_path)


def disaster_type_pie(df: pd.DataFrame | None = None) -> go.Figure:
    """Pie chart: distribution of disaster types."""
    if df is None:
        df = load_disaster_df()
    counts = df["Disaster Type"].value_counts().reset_index()
    counts.columns = ["Disaster Type", "Count"]
    fig = px.pie(
        counts,
        names="Disaster Type",
        values="Count",
        title="Distribution of Disaster Types (1970-2021)",
        hole=0.3,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(width=700, height=500)
    return fig


def disasters_by_year_line(df: pd.DataFrame | None = None) -> go.Figure:
    """Line chart: number of disasters per year."""
    if df is None:
        df = load_disaster_df()
    yearly = df.groupby("Year").size().reset_index(name="Count")
    fig = px.line(
        yearly,
        x="Year",
        y="Count",
        title="Number of Recorded Disasters per Year (1970-2021)",
        markers=True,
    )
    fig.update_layout(width=800, height=450, xaxis_title="Year", yaxis_title="Number of Disasters")
    return fig


def top_countries_bar(df: pd.DataFrame | None = None, top_n: int = 20) -> go.Figure:
    """Horizontal bar chart: top N countries by disaster count."""
    if df is None:
        df = load_disaster_df()
    country_counts = df["Country"].value_counts().head(top_n).sort_values()
    fig = px.bar(
        x=country_counts.values,
        y=country_counts.index,
        orientation="h",
        title=f"Top {top_n} Countries by Number of Disasters",
        labels={"x": "Number of Disasters", "y": "Country"},
    )
    fig.update_layout(width=800, height=600)
    return fig


def deaths_vs_affected_scatter(df: pd.DataFrame | None = None) -> go.Figure:
    """Scatter plot: Total Deaths vs Total Affected, coloured by disaster type."""
    if df is None:
        df = load_disaster_df()
    plot_df = df.dropna(subset=["Total Deaths", "Total Affected"]).copy()
    plot_df = plot_df[plot_df["Total Deaths"] > 0]
    fig = px.scatter(
        plot_df,
        x="Total Deaths",
        y="Total Affected",
        color="Disaster Type",
        hover_data=["Country", "Year"],
        title="Deaths vs Affected Population by Disaster Type",
        log_x=True,
        log_y=True,
    )
    fig.update_layout(width=800, height=550)
    return fig


def monthly_heatmap(df: pd.DataFrame | None = None) -> go.Figure:
    """Heatmap: disaster count by month and disaster type."""
    if df is None:
        df = load_disaster_df()
    month_col = "Start Month"
    if month_col not in df.columns:
        # fallback if column missing
        return go.Figure().update_layout(title="Monthly heatmap: Start Month column not found")

    plot_df = df.dropna(subset=[month_col]).copy()
    plot_df[month_col] = plot_df[month_col].astype(int)
    pivot = plot_df.groupby(["Disaster Type", month_col]).size().reset_index(name="Count")
    matrix = pivot.pivot(index="Disaster Type", columns=month_col, values="Count").fillna(0)

    month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    # Ensure all 12 months present
    for m in range(1, 13):
        if m not in matrix.columns:
            matrix[m] = 0
    matrix = matrix[sorted(matrix.columns)]

    fig = go.Figure(
        go.Heatmap(
            z=matrix.values,
            x=month_labels[: matrix.shape[1]],
            y=matrix.index.tolist(),
            colorscale="YlOrRd",
            colorbar_title="Count",
        )
    )
    fig.update_layout(
        title="Disaster Seasonality: Count by Month and Type",
        width=900,
        height=500,
        xaxis_title="Month",
        yaxis_title="Disaster Type",
    )
    return fig


def create_all_charts(df: pd.DataFrame | None = None) -> dict[str, go.Figure]:
    """Create all 5 charts and return as a dict."""
    if df is None:
        df = load_disaster_df()
    return {
        "disaster_type_pie": disaster_type_pie(df),
        "disasters_by_year": disasters_by_year_line(df),
        "top_countries": top_countries_bar(df),
        "deaths_vs_affected": deaths_vs_affected_scatter(df),
        "monthly_heatmap": monthly_heatmap(df),
    }
