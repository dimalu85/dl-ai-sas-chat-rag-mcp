"""Unit tests for src.retrieval.hybrid — RRF fusion and HybridRetriever with mocked stores."""

from unittest.mock import MagicMock

from langchain_core.documents import Document

from src.retrieval.hybrid import HybridRetriever, reciprocal_rank_fusion


def _doc(doc_id: str, content: str = "") -> Document:
    return Document(page_content=content or f"content of {doc_id}", metadata={"chunk_id": doc_id})


class TestReciprocalRankFusion:
    def test_basic_fusion(self):
        list1 = [_doc("a"), _doc("b"), _doc("c")]
        list2 = [_doc("c"), _doc("a"), _doc("d")]
        fused = reciprocal_rank_fusion([list1, list2])
        ids = [d.metadata["chunk_id"] for d in fused]
        # 'a' appears at rank 0 and 1 → highest combined score
        assert ids[0] == "a"
        # 'c' appears at rank 2 and 0
        assert ids[1] == "c"
        assert set(ids) == {"a", "b", "c", "d"}

    def test_single_list(self):
        docs = [_doc("x"), _doc("y")]
        fused = reciprocal_rank_fusion([docs])
        assert len(fused) == 2
        assert fused[0].metadata["chunk_id"] == "x"

    def test_empty_lists(self):
        fused = reciprocal_rank_fusion([[], []])
        assert fused == []

    def test_no_duplicates_in_output(self):
        list1 = [_doc("a"), _doc("b")]
        list2 = [_doc("a"), _doc("b")]
        fused = reciprocal_rank_fusion([list1, list2])
        ids = [d.metadata["chunk_id"] for d in fused]
        assert len(ids) == len(set(ids))

    def test_document_in_one_list_still_appears(self):
        list1 = [_doc("a")]
        list2 = [_doc("b")]
        fused = reciprocal_rank_fusion([list1, list2])
        ids = {d.metadata["chunk_id"] for d in fused}
        assert ids == {"a", "b"}


class TestHybridRetriever:
    def _make_retriever(self, dense_results, corpus_docs):
        mock_vs = MagicMock()
        mock_vs.similarity_search.return_value = dense_results
        return HybridRetriever(
            vectorstore=mock_vs,
            documents=corpus_docs,
            dense_top_k=len(dense_results),
            bm25_top_k=3,
            rrf_top_k=5,
        )

    def test_retrieve_combines_dense_and_sparse(self):
        corpus = [
            _doc("d1", "earthquake damage japan"),
            _doc("d2", "flood warning system"),
            _doc("d3", "earthquake prediction model"),
            _doc("d4", "hurricane season atlantic"),
        ]
        dense = [corpus[0], corpus[2]]  # dense finds earthquake docs
        retriever = self._make_retriever(dense, corpus)

        results = retriever.retrieve("earthquake")
        ids = [d.metadata["chunk_id"] for d in results]
        # Both earthquake docs should be in results (from both dense and BM25)
        assert "d1" in ids
        assert "d3" in ids

    def test_retrieve_respects_rrf_top_k(self):
        corpus = [_doc(f"d{i}", f"some content {i}") for i in range(10)]
        dense = corpus[:5]
        retriever = self._make_retriever(dense, corpus)
        retriever.rrf_top_k = 3

        results = retriever.retrieve("content")
        assert len(results) <= 3

    def test_retrieve_with_empty_dense(self):
        corpus = [_doc("d1", "flood river overflow")]
        retriever = self._make_retriever([], corpus)

        results = retriever.retrieve("flood")
        # Should still get BM25 results
        assert len(results) > 0
