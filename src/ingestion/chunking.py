"""Hierarchical chunking: parent chunks for context, child chunks for retrieval."""

import uuid

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import CHILD_CHUNK_SIZE, CHUNK_OVERLAP_RATIO, PARENT_CHUNK_SIZE


def _make_splitter(chunk_size: int, overlap: int) -> RecursiveCharacterTextSplitter:
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
        length_function=len,
    )


def build_parent_child_chunks(
    docs: list[Document],
    parent_size: int = PARENT_CHUNK_SIZE,
    child_size: int = CHILD_CHUNK_SIZE,
    overlap_ratio: float = CHUNK_OVERLAP_RATIO,
) -> tuple[list[Document], list[Document]]:
    """Split documents into parent and child chunks.

    Parameters
    ----------
    docs : raw LangChain Documents (e.g. from loaders)
    parent_size : target size for parent chunks (characters)
    child_size : target size for child chunks (characters)
    overlap_ratio : overlap as fraction of child_size

    Returns
    -------
    (parent_chunks, child_chunks) — child chunks reference their parent
    via ``parent_chunk_id`` in metadata.
    """
    child_overlap = int(child_size * overlap_ratio)

    parent_splitter = _make_splitter(parent_size, overlap=0)
    child_splitter = _make_splitter(child_size, overlap=child_overlap)

    parent_chunks: list[Document] = []
    child_chunks: list[Document] = []

    for doc in docs:
        parents = parent_splitter.split_documents([doc])

        for parent in parents:
            parent_id = uuid.uuid4().hex[:12]
            parent.metadata["parent_chunk_id"] = parent_id
            parent.metadata["chunk_id"] = parent_id
            parent.metadata.setdefault("filename", parent.metadata.get("source", ""))
            parent.metadata.setdefault("doc_type", "unknown")
            parent_chunks.append(parent)

            children = child_splitter.split_documents([parent])
            for i, child in enumerate(children):
                child.metadata["parent_chunk_id"] = parent_id
                child.metadata["chunk_id"] = f"{parent_id}_c{i}"
                child.metadata["filename"] = parent.metadata["filename"]
                child.metadata["doc_type"] = parent.metadata["doc_type"]
                child_chunks.append(child)

    return parent_chunks, child_chunks
