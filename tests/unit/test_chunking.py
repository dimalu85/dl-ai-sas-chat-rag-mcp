"""Unit tests for src.ingestion.chunking — hierarchical parent/child chunking."""

from langchain_core.documents import Document

from src.ingestion.chunking import build_parent_child_chunks


def _make_doc(text: str, **meta) -> Document:
    defaults = {"source": "test.pdf", "filename": "test.pdf", "doc_type": "pdf"}
    defaults.update(meta)
    return Document(page_content=text, metadata=defaults)


class TestBuildParentChildChunks:
    def test_produces_parents_and_children(self):
        doc = _make_doc("word " * 1000)  # ~5000 chars
        parents, children = build_parent_child_chunks([doc])
        assert len(parents) > 0
        assert len(children) > 0
        assert len(children) >= len(parents)

    def test_parent_size_within_bounds(self):
        doc = _make_doc("word " * 2000)
        parents, _ = build_parent_child_chunks([doc], parent_size=2048)
        for p in parents:
            # Allow some slack for splitter boundary
            assert len(p.page_content) <= 2048 + 100

    def test_child_size_within_bounds(self):
        doc = _make_doc("word " * 2000)
        _, children = build_parent_child_chunks([doc], child_size=512)
        for c in children:
            assert len(c.page_content) <= 512 + 100

    def test_child_references_parent(self):
        doc = _make_doc("word " * 2000)
        parents, children = build_parent_child_chunks([doc])
        parent_ids = {p.metadata["parent_chunk_id"] for p in parents}
        for child in children:
            assert child.metadata["parent_chunk_id"] in parent_ids

    def test_metadata_fields_present(self):
        doc = _make_doc("word " * 500)
        parents, children = build_parent_child_chunks([doc])
        for p in parents:
            assert "parent_chunk_id" in p.metadata
            assert "chunk_id" in p.metadata
            assert "filename" in p.metadata
            assert "doc_type" in p.metadata
        for c in children:
            assert "parent_chunk_id" in c.metadata
            assert "chunk_id" in c.metadata
            assert c.metadata["chunk_id"] != c.metadata["parent_chunk_id"]

    def test_child_chunk_id_format(self):
        doc = _make_doc("word " * 1000)
        _, children = build_parent_child_chunks([doc])
        for c in children:
            assert "_c" in c.metadata["chunk_id"]

    def test_preserves_doc_type_metadata(self):
        doc = _make_doc("word " * 500, doc_type="csv")
        parents, children = build_parent_child_chunks([doc])
        for p in parents:
            assert p.metadata["doc_type"] == "csv"
        for c in children:
            assert c.metadata["doc_type"] == "csv"

    def test_empty_input(self):
        parents, children = build_parent_child_chunks([])
        assert parents == []
        assert children == []

    def test_small_doc_single_parent(self):
        doc = _make_doc("Short text.")
        parents, children = build_parent_child_chunks([doc])
        assert len(parents) == 1
        assert len(children) >= 1
        assert children[0].metadata["parent_chunk_id"] == parents[0].metadata["parent_chunk_id"]
