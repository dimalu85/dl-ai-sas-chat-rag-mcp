"""Document reranker using Cohere, with graceful fallback."""

import logging
import os

from langchain_core.documents import Document

from src.config import RERANK_TOP_K

logger = logging.getLogger(__name__)


def rerank(
    query: str,
    docs: list[Document],
    top_k: int = RERANK_TOP_K,
) -> list[Document]:
    """Rerank documents using Cohere; fall back to truncation if unavailable.

    Parameters
    ----------
    query : the user query
    docs : candidate documents to rerank
    top_k : number of top results to return

    Returns
    -------
    Reranked (or truncated) list of Documents.
    """
    if not docs:
        return []

    cohere_key = os.environ.get("COHERE_API_KEY", "")
    if not cohere_key:
        logger.warning("No COHERE_API_KEY set — skipping reranking, returning top-%d by position", top_k)
        return docs[:top_k]

    try:
        from langchain_cohere import CohereRerank

        reranker = CohereRerank(
            model="rerank-v3.5",
            cohere_api_key=cohere_key,
            top_n=top_k,
        )

        reranked = reranker.compress_documents(docs, query)
        logger.info("Cohere reranked %d → %d documents", len(docs), len(reranked))
        return list(reranked)

    except Exception as exc:
        logger.warning("Cohere reranking failed (%s) — falling back to top-%d by position", exc, top_k)
        return docs[:top_k]
