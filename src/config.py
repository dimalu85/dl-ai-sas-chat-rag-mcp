"""Centralized configuration for the Natural Disaster Chat App."""

from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────
ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
OUTPUT_DIR = ROOT_DIR / "output"
PDF_DIR = DATA_DIR / "pdfs"

CSV_PATH = DATA_DIR / "1970-2021_DISASTERS.xlsx - emdat data.csv"
CHROMA_PERSIST_DIR = ROOT_DIR / "chroma_db"

# ── CSV Schema ─────────────────────────────────────────────────────────
REQUIRED_CSV_COLUMNS = [
    "Year",
    "Country",
    "Disaster Type",
    "Total Deaths",
    "Total Affected",
]

# ── Chunking ───────────────────────────────────────────────────────────
PARENT_CHUNK_SIZE = 2048
CHILD_CHUNK_SIZE = 512
CHUNK_OVERLAP_RATIO = 0.10  # 10 % overlap for child chunks

# ── Embeddings ─────────────────────────────────────────────────────────
HF_EMBEDDING_MODEL = "BAAI/bge-m3"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"

# ── Retrieval ──────────────────────────────────────────────────────────
DENSE_TOP_K = 20
BM25_TOP_K = 20
RRF_TOP_K = 15
RERANK_TOP_K = 5

# ── LLM ────────────────────────────────────────────────────────────────
LLM_MODEL = "gpt-4o-mini"
LLM_TEMPERATURE = 0.0
LLM_MAX_TOKENS = 1024

# ── MCP Server ─────────────────────────────────────────────────────────
MCP_SERVER_NAME = "natural-disaster-mcp"
CSV_QUERY_DEFAULT_LIMIT = 20
