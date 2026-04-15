"""Embedding model and ChromaDB vector store management."""

import logging
from pathlib import Path

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from src.config import CHROMA_PERSIST_DIR, HF_EMBEDDING_MODEL, OPENAI_EMBEDDING_MODEL

logger = logging.getLogger(__name__)


def get_embeddings(prefer_hf: bool = True) -> Embeddings:
    """Return an embedding model, preferring HuggingFace; fallback to OpenAI.

    Parameters
    ----------
    prefer_hf : if True (default), try HuggingFace first.
    """
    if prefer_hf:
        try:
            from langchain_huggingface import HuggingFaceEmbeddings

            emb = HuggingFaceEmbeddings(model_name=HF_EMBEDDING_MODEL)
            logger.info("Using HuggingFace embeddings: %s", HF_EMBEDDING_MODEL)
            return emb
        except Exception as exc:
            logger.warning("HuggingFace embeddings unavailable (%s), falling back to OpenAI", exc)

    from langchain_openai import OpenAIEmbeddings

    emb = OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL)
    logger.info("Using OpenAI embeddings: %s", OPENAI_EMBEDDING_MODEL)
    return emb


def create_vectorstore(
    chunks: list[Document],
    persist_dir: str | Path = CHROMA_PERSIST_DIR,
    embeddings: Embeddings | None = None,
):
    """Create (or overwrite) a ChromaDB vector store from document chunks.

    Returns a Chroma instance.
    """
    from langchain_community.vectorstores import Chroma

    if embeddings is None:
        embeddings = get_embeddings()

    persist_dir = str(Path(persist_dir))

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_dir,
    )
    logger.info("Created vectorstore with %d chunks at %s", len(chunks), persist_dir)
    return vectorstore


def load_vectorstore(
    persist_dir: str | Path = CHROMA_PERSIST_DIR,
    embeddings: Embeddings | None = None,
):
    """Load an existing ChromaDB vector store from disk.

    Returns a Chroma instance.
    """
    from langchain_community.vectorstores import Chroma

    if embeddings is None:
        embeddings = get_embeddings()

    persist_dir = str(Path(persist_dir))

    vectorstore = Chroma(
        persist_directory=persist_dir,
        embedding_function=embeddings,
    )
    logger.info("Loaded vectorstore from %s", persist_dir)
    return vectorstore
