"""Hybrid retriever combining dense (ChromaDB) and sparse (BM25) search with RRF."""

import logging

from langchain_core.documents import Document
from rank_bm25 import BM25Okapi

from src.config import BM25_TOP_K, DENSE_TOP_K, RRF_TOP_K

logger = logging.getLogger(__name__)


def _tokenize(text: str) -> list[str]:
    """Simple whitespace + lowercase tokenizer for BM25."""
    return text.lower().split()


def reciprocal_rank_fusion(
    ranked_lists: list[list[Document]],
    k: int = 60,
) -> list[Document]:
    """Merge multiple ranked document lists using Reciprocal Rank Fusion.

    RRF score for document d = sum(1 / (k + rank_i)) across all lists.
    """
    scores: dict[str, float] = {}
    doc_map: dict[str, Document] = {}

    for ranked in ranked_lists:
        for rank, doc in enumerate(ranked):
            doc_id = doc.metadata.get("chunk_id", doc.page_content[:100])
            if doc_id not in doc_map:
                doc_map[doc_id] = doc
                scores[doc_id] = 0.0
            scores[doc_id] += 1.0 / (k + rank + 1)

    sorted_ids = sorted(scores, key=scores.get, reverse=True)
    return [doc_map[did] for did in sorted_ids]


class HybridRetriever:
    """Combines ChromaDB dense retrieval with BM25 sparse retrieval via RRF.

    Parameters
    ----------
    vectorstore : a LangChain-compatible vectorstore (must have similarity_search)
    documents : the corpus of Documents used to build BM25 index
    dense_top_k : number of dense results to fetch
    bm25_top_k : number of BM25 results to fetch
    rrf_top_k : final number of fused results to return
    """

    def __init__(
        self,
        vectorstore,
        documents: list[Document],
        dense_top_k: int = DENSE_TOP_K,
        bm25_top_k: int = BM25_TOP_K,
        rrf_top_k: int = RRF_TOP_K,
    ):
        self.vectorstore = vectorstore
        self.documents = documents
        self.dense_top_k = dense_top_k
        self.bm25_top_k = bm25_top_k
        self.rrf_top_k = rrf_top_k

        # Build BM25 index
        corpus = [_tokenize(doc.page_content) for doc in documents]
        self.bm25 = BM25Okapi(corpus)
        logger.info("Built BM25 index over %d documents", len(documents))

    def retrieve(self, query: str) -> list[Document]:
        """Run hybrid retrieval: dense + sparse + RRF fusion."""
        # Dense retrieval
        dense_results = self.vectorstore.similarity_search(
            query, k=self.dense_top_k
        )

        # Sparse retrieval (BM25)
        tokenized_query = _tokenize(query)
        bm25_scores = self.bm25.get_scores(tokenized_query)

        # Get top-k BM25 indices
        top_indices = sorted(
            range(len(bm25_scores)),
            key=lambda i: bm25_scores[i],
            reverse=True,
        )[: self.bm25_top_k]
        bm25_results = [self.documents[i] for i in top_indices]

        # Fuse with RRF
        fused = reciprocal_rank_fusion([dense_results, bm25_results])
        result = fused[: self.rrf_top_k]

        logger.info(
            "Hybrid retrieval: %d dense + %d BM25 → %d fused",
            len(dense_results),
            len(bm25_results),
            len(result),
        )
        return result
