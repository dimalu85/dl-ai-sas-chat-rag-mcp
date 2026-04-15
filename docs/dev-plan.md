# Plan: Natural Disaster Chat App — Sequential Developer Tasks

Build a chat application from scratch that composes a RAG module (PDF knowledge retrieval) with an MCP module (CSV disaster data querying) via a LangGraph agent. 25 tasks across 7 phases, kept minimal to hit all rubric categories (target 8.5+).

## Architecture

```
User → Jupyter Notebook (Chat UI)
         ↓
    LangGraph Agent (ReAct routing)
         ├── RAG Path: Hybrid Retriever (Dense+BM25) → Reranker → LLM
         └── MCP Path: MCP Server → Pandas CSV Query → LLM

Storage: ChromaDB (vectors), CSV (disaster data), PDF (knowledge base)
```

---

## Phase 1: Project Scaffolding (Tasks 1–3)

### Task 1 — Create project structure & config files
- Create `src/` with subfolders: `ingestion/`, `retrieval/`, `agent/`, `mcp_server/`, `evaluation/`, `visualization/` — each with `__init__.py`
- Create `tests/` with `unit/`, `contract/`, `integration/` subfolders + `conftest.py`
- Create `requirements.txt` (langchain, langgraph, chromadb, rank-bm25, plotly, networkx, ragas, pytest, mcp, etc.)
- Create `.env.example` (`OPENAI_API_KEY`, `COHERE_API_KEY`)
- Create `src/config.py` — centralized paths, model names, chunk sizes

### Task 2 — Prepare dataset
- Choose `data/1970-2021_DISASTERS.xlsx - emdat data.csv` as primary
- Define path constants in config; verify CSV loads cleanly with required columns (`Year`, `Country`, `Disaster Type`, `Total Deaths`, `Total Affected`)

### Task 3 — Create Pydantic response models → `src/mcp_server/models.py`
- `McpResponseMeta` (schema_version, request_id, timing_ms)
- `McpResponse` (ok, data, error, meta) + factory helpers `build_success_response()`, `build_error_response()`

---

## Phase 2: MCP Server — CSV Query Tool (Tasks 4–7)

### Task 4 — CSV validation → `src/mcp_server/validation.py`
- `validate_csv(path) -> list[str]`: file exists, required columns present, numeric types correct

### Task 5 — CSV query logic → `src/mcp_server/csv_tool.py`
- `query_disasters(csv_path, country=None, disaster_type=None, year=None, year_range=None, min_deaths=None, sort_by=None, limit=20) -> McpResponse`
- Cache DataFrame; apply Pandas filters; measure timing; never raise raw exceptions

### Task 6 — MCP server → `src/mcp_server/server.py`
- FastMCP server with one tool `query_natural_disasters` delegating to `query_disasters()`
- stdio transport

### Task 7 — Tests for MCP module
- `tests/unit/test_csv_tool.py` — filter by country, year, year_range; empty result; invalid schema
- `tests/unit/test_validation.py` — valid CSV, missing columns, bad types
- `tests/contract/test_mcp_envelope.py` — success/error envelope invariants, meta fields
- Small fixture CSV in `conftest.py`

---

## Phase 3: RAG Pipeline — Ingestion & Retrieval (Tasks 8–13)

### Task 8 — Document loaders → `src/ingestion/loaders.py`
- `load_pdfs(pdf_dir) -> list[Document]` via `PyPDFLoader` + metadata
- `load_csv_as_docs(csv_path) -> list[Document]` — serialize key columns per row

### Task 9 — Hierarchical chunking → `src/ingestion/chunking.py`
- Parent chunks (~2048 tokens) + child chunks (~512 tokens, 10% overlap)
- Assign `parent_chunk_id`, `chunk_id`, `filename`, `doc_type` metadata

### Task 10 — Embedding + vector store → `src/retrieval/vectorstore.py`
- `HuggingFaceEmbeddings("BAAI/bge-m3")` with OpenAI fallback
- `create_vectorstore(chunks, persist_dir) -> Chroma`, `load_vectorstore(persist_dir) -> Chroma`

### Task 11 — Hybrid retriever → `src/retrieval/hybrid.py`
- `HybridRetriever` combining ChromaDB (dense, top-20) + BM25 (sparse, top-20)
- Reciprocal Rank Fusion → top-15 candidates

### Task 12 — Reranker → `src/retrieval/reranker.py`
- `rerank(query, docs, top_k=5) -> list[Document]` via `CohereRerank`
- Graceful fallback: skip reranking if no Cohere key

### Task 13 — Tests for RAG components
- `tests/unit/test_chunking.py` — parent-child relationship, size limits, metadata
- `tests/unit/test_hybrid_retriever.py` — RRF fusion logic with mocked stores

---

## Phase 4: Agent & Integration (Tasks 14–18)

### Task 14 — Prompt templates → `src/agent/prompts.py`
- `SYSTEM_PROMPT`: role, grounding, citation format `[Source: filename, page X]`, token budget, special terms, date injection, fallback
- `ROUTING_PROMPT`: classify intent → `{disaster_data, knowledge_base, mixed, general}`

### Task 15 — Query routing → `src/agent/routing.py`
- `classify_intent(query, llm) -> str` — LLM-based classification using ROUTING_PROMPT

### Task 16 — LangGraph agent → `src/agent/graph.py`
- `AgentState(TypedDict)`: question, intent, context, answer, chat_history, sources
- `StateGraph` nodes: `classify` → `retrieve_rag` / `query_csv` / both → `generate`
- Conditional edges by intent; conversation memory via `RunnableWithMessageHistory`

### Task 17 — Contract + integration tests
- `tests/contract/test_module_composition.py` — agent with stubbed retriever; agent with stubbed CSV tool
- `tests/integration/test_rag_pipeline.py` — end-to-end: ingest → embed → retrieve → answer
- `tests/integration/test_mcp_e2e.py` — MCP server processes query correctly

### Task 18 — Routing unit test
- `tests/unit/test_routing.py` — mock LLM, verify disaster/knowledge/general classification

---

## Phase 5: RAG Evaluation (Tasks 19–20)

### Task 19 — Golden dataset + evaluator
- Create `data/golden_dataset.json` — 50 Q&A pairs (~20 disaster, ~20 knowledge, ~10 mixed/general)
- `src/evaluation/evaluator.py`: RAGAS metrics (faithfulness, relevancy, precision, recall) + custom (hit_rate@5, CSV query correctness)
- `src/evaluation/dashboard.py`: render metrics as Plotly tables/charts

### Task 20 — Strategy comparison
- Evaluate golden dataset against 4 strategies: dense-only, BM25-only, hybrid, hybrid+reranking
- Output comparison table + chart

---

## Phase 6: Visualization (Tasks 21–23)

### Task 21 — Charts → `src/visualization/charts.py`
- 5 Plotly charts: disaster type pie, disasters-by-year line, top countries bar, deaths-vs-affected scatter, monthly heatmap

### Task 22 — Diagrams → `src/visualization/diagrams.py`
- NetworkX + Plotly force-directed graph: countries connected by shared disaster types
- Mermaid architecture diagrams in notebook markdown cells

### Task 23 — HTML report
- Combine all Plotly figures into styled HTML → save to `output/report.html`

---

## Phase 7: Notebook Assembly & Docs (Tasks 24–25)

### Task 24 — Build the notebook → `natural-disaster-chat-app.ipynb`
- 8 sections: Setup → Ingestion → Retrieval Demo → MCP Demo → Agent Chat → Evaluation → Visualizations → Architecture Diagrams
- Notebook is a thin orchestrator — all logic imported from `src/`

### Task 25 — Write README → `README.md`
- Architecture (Mermaid), setup instructions, dataset links (EM-DAT/Kaggle), usage guide, tech stack, testing instructions

---

## Verification
1. `pytest tests/ --cov=src` — all pass, ≥85% coverage
2. Notebook runs top-to-bottom without errors
3. Agent routes disaster question → MCP → correct CSV response
4. Agent routes knowledge question → RAG → answer with citations
5. Evaluation dashboard renders metrics for 4 strategies
6. 5+ charts + 1+ diagram render correctly
7. `output/report.html` generated
8. README setup instructions work from a fresh clone

## Key Decisions
- Single CSV file (`1970-2021`) for simplicity
- Notebook as thin orchestrator; all logic in `src/` modules
- HuggingFace embeddings preferred (cost); OpenAI as fallback
- Cohere reranker with graceful fallback if no key
- FastMCP with stdio transport
- No web UI — Jupyter notebook per task spec
