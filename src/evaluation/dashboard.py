"""Evaluation dashboard: render metrics as Plotly tables and charts."""

from typing import Any

import plotly.graph_objects as go


def render_metrics_table(metrics: dict[str, Any], title: str = "Evaluation Metrics") -> go.Figure:
    """Render a metrics dict as a styled Plotly table."""
    names = []
    values = []
    for key, val in metrics.items():
        if isinstance(val, dict):
            for sub_key, sub_val in val.items():
                names.append(f"{key}.{sub_key}")
                values.append(f"{sub_val:.4f}" if isinstance(sub_val, float) else str(sub_val))
        else:
            names.append(key)
            values.append(f"{val:.4f}" if isinstance(val, float) else str(val))

    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=["Metric", "Value"],
                    fill_color="#2c3e50",
                    font=dict(color="white", size=14),
                    align="left",
                ),
                cells=dict(
                    values=[names, values],
                    fill_color=[["#ecf0f1", "#ffffff"] * (len(names) // 2 + 1)],
                    font=dict(size=12),
                    align="left",
                ),
            )
        ]
    )
    fig.update_layout(title=title, width=600, height=max(300, 50 * len(names)))
    return fig


def render_strategy_comparison(
    strategy_results: dict[str, dict[str, float]],
    title: str = "Retrieval Strategy Comparison",
) -> go.Figure:
    """Render a grouped bar chart comparing retrieval strategies across metrics.

    Parameters
    ----------
    strategy_results : {strategy_name: {metric_name: value, ...}, ...}
    """
    strategies = list(strategy_results.keys())
    if not strategies:
        return go.Figure()

    metric_names = list(next(iter(strategy_results.values())).keys())

    fig = go.Figure()
    for metric in metric_names:
        values = [strategy_results[s].get(metric, 0) for s in strategies]
        fig.add_trace(go.Bar(name=metric, x=strategies, y=values))

    fig.update_layout(
        title=title,
        barmode="group",
        xaxis_title="Strategy",
        yaxis_title="Score",
        yaxis=dict(range=[0, 1]),
        width=800,
        height=500,
    )
    return fig


def render_csv_correctness_chart(details: list[dict]) -> go.Figure:
    """Render CSV query correctness as a horizontal bar chart."""
    questions = [d["question"][:50] + "..." for d in details]
    matches = [d["matches"] for d in details]
    colors = ["#27ae60" if d["correct"] else "#e74c3c" for d in details]

    fig = go.Figure(
        go.Bar(
            y=questions,
            x=matches,
            orientation="h",
            marker_color=colors,
            text=matches,
            textposition="auto",
        )
    )
    fig.update_layout(
        title="CSV Query Correctness (green=matched, red=no results)",
        xaxis_title="Matching Records",
        yaxis=dict(autorange="reversed"),
        width=900,
        height=max(400, 30 * len(details)),
    )
    return fig
