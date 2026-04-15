"""Strategy comparison: evaluate golden dataset against 4 retrieval strategies."""

import logging
from typing import Any

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from src.config import BM25_TOP_K, DENSE_TOP_K, RERANK_TOP_K, RRF_TOP_K
from src.evaluation.dashboard import render_metrics_table, render_strategy_comparison
from src.evaluation.evaluator import evaluate_hit_rate, load_golden_dataset
from src.retrieval.hybrid import HybridRetriever, reciprocal_rank_fusion

logger = logging.getLogger(__name__)


class DenseOnlyRetriever:
    """Retriever using only vector similarity search."""

    def __init__(self, vectorstore, top_k: int = DENSE_TOP_K):
        self.vectorstore = vectorstore
        self.top_k = top_k

    def retrieve(self, query: str) -> list[Document]:
        return self.vectorstore.similarity_search(query, k=self.top_k)


class BM25OnlyRetriever:
    """Retriever using only BM25 sparse search."""

    def __init__(self, documents: list[Document], top_k: int = BM25_TOP_K):
        from rank_bm25 import BM25Okapi

        self.documents = documents
        self.top_k = top_k
        corpus = [doc.page_content.lower().split() for doc in documents]
        self.bm25 = BM25Okapi(corpus)

    def retrieve(self, query: str) -> list[Document]:
        scores = self.bm25.get_scores(query.lower().split())
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[
            : self.top_k
        ]
        return [self.documents[i] for i in top_indices]


class HybridPlusRerankRetriever:
    """Hybrid retriever + reranking."""

    def __init__(self, hybrid_retriever: HybridRetriever, reranker_fn, top_k: int = RERANK_TOP_K):
        self.hybrid = hybrid_retriever
        self.reranker_fn = reranker_fn
        self.top_k = top_k

    def retrieve(self, query: str) -> list[Document]:
        docs = self.hybrid.retrieve(query)
        return self.reranker_fn(query, docs, top_k=self.top_k)


def compare_strategies(
    vectorstore,
    documents: list[Document],
    reranker_fn=None,
    golden_path=None,
) -> dict[str, dict[str, float]]:
    """Compare 4 retrieval strategies using golden dataset hit_rate@5.

    Returns {strategy_name: {hit_rate_at_5: float}} for each strategy.
    """
    golden = load_golden_dataset(golden_path) if golden_path else load_golden_dataset()
    kb_items = [item for item in golden if item["category"] == "knowledge_base"]
    questions = [item["question"] for item in kb_items]
    keywords = [item["expected_answer"].split()[:5] for item in kb_items]

    strategies: dict[str, Any] = {}

    # 1. Dense only
    dense_ret = DenseOnlyRetriever(vectorstore)
    strategies["dense_only"] = {
        "hit_rate_at_5": evaluate_hit_rate(dense_ret, questions, keywords, k=5),
    }
    logger.info("Dense-only: %.4f", strategies["dense_only"]["hit_rate_at_5"])

    # 2. BM25 only
    bm25_ret = BM25OnlyRetriever(documents)
    strategies["bm25_only"] = {
        "hit_rate_at_5": evaluate_hit_rate(bm25_ret, questions, keywords, k=5),
    }
    logger.info("BM25-only: %.4f", strategies["bm25_only"]["hit_rate_at_5"])

    # 3. Hybrid (Dense + BM25 + RRF)
    hybrid_ret = HybridRetriever(vectorstore, documents)
    strategies["hybrid"] = {
        "hit_rate_at_5": evaluate_hit_rate(hybrid_ret, questions, keywords, k=5),
    }
    logger.info("Hybrid: %.4f", strategies["hybrid"]["hit_rate_at_5"])

    # 4. Hybrid + Reranking
    if reranker_fn is not None:
        hybrid_rerank_ret = HybridPlusRerankRetriever(hybrid_ret, reranker_fn)
        strategies["hybrid_rerank"] = {
            "hit_rate_at_5": evaluate_hit_rate(hybrid_rerank_ret, questions, keywords, k=5),
        }
        logger.info("Hybrid+Rerank: %.4f", strategies["hybrid_rerank"]["hit_rate_at_5"])
    else:
        # Reranker not available — use hybrid results as fallback
        strategies["hybrid_rerank"] = strategies["hybrid"].copy()
        logger.info("Hybrid+Rerank: same as Hybrid (no reranker configured)")

    return strategies


def render_comparison_report(strategy_results: dict[str, dict[str, float]]):
    """Return (table_fig, chart_fig) for the strategy comparison."""
    table_fig = render_metrics_table(
        {name: vals for name, vals in strategy_results.items()},
        title="Strategy Comparison — Hit Rate@5",
    )
    chart_fig = render_strategy_comparison(
        strategy_results,
        title="Retrieval Strategy Comparison — Hit Rate@5",
    )
    return table_fig, chart_fig
