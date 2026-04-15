"""Diagrams: NetworkX force-directed graph and Mermaid architecture diagrams."""

from collections import defaultdict

import networkx as nx
import plotly.graph_objects as go
import pandas as pd

from src.config import CSV_PATH


def country_disaster_network(
    df: pd.DataFrame | None = None,
    top_countries: int = 30,
    min_shared_types: int = 3,
) -> go.Figure:
    """Force-directed graph: countries connected by shared disaster types.

    Nodes = top countries by disaster count.
    Edges = countries that share >= min_shared_types disaster types.
    Node size = total disaster count.
    """
    if df is None:
        df = pd.read_csv(CSV_PATH)

    # Get top countries
    top = df["Country"].value_counts().head(top_countries).index.tolist()
    filtered = df[df["Country"].isin(top)]

    # Build country → set of disaster types
    country_types: dict[str, set] = {}
    country_counts: dict[str, int] = {}
    for country in top:
        sub = filtered[filtered["Country"] == country]
        country_types[country] = set(sub["Disaster Type"].unique())
        country_counts[country] = len(sub)

    # Build graph
    G = nx.Graph()
    for country in top:
        G.add_node(country, count=country_counts[country])

    for i, c1 in enumerate(top):
        for c2 in top[i + 1 :]:
            shared = country_types[c1] & country_types[c2]
            if len(shared) >= min_shared_types:
                G.add_edge(c1, c2, weight=len(shared), shared=", ".join(sorted(shared)))

    # Layout
    pos = nx.spring_layout(G, k=2.0, iterations=50, seed=42)

    # Edge traces
    edge_x, edge_y = [], []
    for u, v in G.edges():
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=0.5, color="#888"),
        hoverinfo="none",
        mode="lines",
    )

    # Node traces
    node_x = [pos[n][0] for n in G.nodes()]
    node_y = [pos[n][1] for n in G.nodes()]
    node_sizes = [G.nodes[n]["count"] / 10 + 8 for n in G.nodes()]
    node_text = [
        f"{n}<br>Disasters: {G.nodes[n]['count']}<br>Connections: {G.degree(n)}"
        for n in G.nodes()
    ]

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        hoverinfo="text",
        text=[n for n in G.nodes()],
        textposition="top center",
        textfont=dict(size=8),
        hovertext=node_text,
        marker=dict(
            size=node_sizes,
            color=[G.degree(n) for n in G.nodes()],
            colorscale="Viridis",
            colorbar=dict(title="Connections"),
            line_width=1,
        ),
    )

    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title="Country–Disaster Network (connected by shared disaster types)",
            showlegend=False,
            hovermode="closest",
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            width=900,
            height=700,
        ),
    )
    return fig


ARCHITECTURE_MERMAID = """\
```mermaid
graph TD
    A[User] --> B[Jupyter Notebook Chat UI]
    B --> C[LangGraph Agent - ReAct Routing]
    C --> D{Intent Classification}
    D -->|disaster_data| E[MCP Server]
    D -->|knowledge_base| F[RAG Pipeline]
    D -->|mixed| G[Both Paths]
    D -->|general| H[Direct LLM Response]

    E --> I[CSV Query Tool - Pandas]
    I --> J[(EM-DAT CSV 1970-2021)]

    F --> K[Hybrid Retriever]
    K --> L[Dense Search - ChromaDB]
    K --> M[Sparse Search - BM25]
    L --> N[Reciprocal Rank Fusion]
    M --> N
    N --> O[Cohere Reranker]

    G --> E
    G --> F

    O --> P[LLM Generation - GPT-4o-mini]
    I --> P
    H --> P
    P --> Q[Response with Citations]
    Q --> B

    style A fill:#3498db,color:#fff
    style C fill:#2ecc71,color:#fff
    style E fill:#e74c3c,color:#fff
    style F fill:#9b59b6,color:#fff
    style J fill:#f39c12,color:#fff
    style L fill:#1abc9c,color:#fff
    style P fill:#e67e22,color:#fff
```
"""

RAG_PIPELINE_MERMAID = """\
```mermaid
graph LR
    A[PDF Documents] --> B[PyPDF Loader]
    C[CSV Data] --> D[Row-to-Doc Converter]
    B --> E[Parent Chunker 2048 chars]
    D --> E
    E --> F[Child Chunker 512 chars]
    F --> G[HuggingFace Embeddings BGE-M3]
    G --> H[(ChromaDB Vector Store)]

    I[User Query] --> J[Dense Search top-20]
    I --> K[BM25 Sparse Search top-20]
    H --> J
    J --> L[RRF Fusion top-15]
    K --> L
    L --> M[Cohere Reranker top-5]
    M --> N[LLM Generation]
    N --> O[Answer + Citations]

    style H fill:#3498db,color:#fff
    style L fill:#2ecc71,color:#fff
    style M fill:#e74c3c,color:#fff
    style N fill:#e67e22,color:#fff
```
"""
