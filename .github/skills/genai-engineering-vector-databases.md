## Purpose

## Quick Decision Frameworks

### Choosing an Orchestration Framework

```
Need complex multi-step agents with cycles, human-in-the-loop, persistence?
  → LangGraph

Need flexible RAG with deep indexing, custom retrievers, property graphs?
  → LlamaIndex

Need simple chains, LCEL composition, broad integrations?
  → LangChain core

Need both retrieval depth + agent complexity?
  → LlamaIndex for indexing/retrieval + LangGraph for orchestration

Deploying as REST API quickly?
  → LangServe (LangChain) or FastAPI wrapper

Need tracing, evaluation, dataset management?
  → LangSmith (LangChain) or custom OpenTelemetry + LLM-as-judge
```

### Choosing a Vector Database

```
Fully managed, zero-ops, serverless?
  → Pinecone

Self-hosted, high performance, rich filtering, Rust-based?
  → Qdrant

Multi-modal, GraphQL API, hybrid search built-in?
  → Weaviate

Lightweight, in-process, prototyping?
  → Chroma

Billion-scale, GPU-accelerated, enterprise?
  → Milvus / Zilliz Cloud

Already using PostgreSQL?
  → pgvector (+ pgvectorscale for performance)

Already using MongoDB?
  → MongoDB Atlas Vector Search
```

### Choosing a Cloud AI Platform

```
AWS-native, multi-model marketplace, fine-tuning, Knowledge Bases?
  → AWS Bedrock

Azure-native, OpenAI models, AI Search integration, enterprise RBAC?
  → Azure AI Foundry + Azure AI Search

GCP-native, Gemini models, Vertex AI Search, grounding, MLOps?
  → Google Vertex AI

Multi-cloud / provider-agnostic?
  → Abstract via LiteLLM or LangChain model adapters
```

---

## Core Architecture Patterns

### Standard RAG Pipeline

```
Documents → Chunking → Embedding → Vector Store → Query
                                                     ↓
User Query → Embedding → Retrieval → [Reranking] → Context Assembly → LLM → Response
```

Key decisions at each stage:
1. **Chunking**: size, overlap, strategy (semantic vs fixed vs recursive)
2. **Embedding model**: dimension, multilingual needs, cost vs quality
3. **Vector store**: scale, latency, filtering, hybrid search
4. **Retrieval**: top-k, MMR, hybrid (dense + sparse)
5. **Reranking**: cross-encoder, Cohere Rerank, ColBERT
6. **Generation**: model, temperature, system prompt, output parsing

### Agent Architecture Patterns

```
Pattern 1: ReAct Agent (reasoning + acting loop)
  Observe → Think → Act → Observe → ... → Final Answer

Pattern 2: Plan-and-Execute
  Plan all steps → Execute sequentially → Replan if needed

Pattern 3: Multi-Agent (LangGraph)
  Supervisor routes to specialist agents → Each has own tools/state

Pattern 4: Reflection/Self-Critique
  Generate → Critique → Revise → ... → Accept
```

### Production Architecture

```
Client → API Gateway → Load Balancer
                            ↓
                    App Server (FastAPI/LangServe)
                    ├── LLM Router (model selection, fallback)
                    ├── Retrieval Layer (vector DB + reranker)
                    ├── Cache Layer (semantic cache / exact cache)
                    ├── Guardrails (input/output filtering)
                    └── Observability (traces, metrics, logs)
                            ↓
              ┌─────────────┼────────────────┐
          Vector DB      LLM Provider     Object Store
        (Qdrant/etc)   (OpenAI/Bedrock)   (S3/GCS/Blob)
```

---

## Essential Patterns & Anti-Patterns

### Embedding Best Practices

- **Match embedding model at index and query time** — mismatched models = garbage results
- **Normalize embeddings** if using cosine similarity (most DBs handle this)
- **Batch embed** for ingestion; single embed for queries
- Leading models (as of 2025): OpenAI `text-embedding-3-large`, Cohere `embed-v4`, Google `text-embedding-005`, open-source `BAAI/bge-m3`, `nomic-embed-text-v1.5`
- Dimension reduction (e.g., Matryoshka/MRL embeddings) saves storage with minimal quality loss

### Chunking Strategy Selection

```
Document type → Strategy:
  Code           → AST-based or function-level splitting
  Markdown/HTML  → Header-based hierarchical splitting
  Legal/Academic → Section-aware + paragraph-level
  Conversations  → Message-boundary splitting
  Tables/CSV     → Row-based or serialize to text
  General prose  → RecursiveCharacterTextSplitter (LangChain) or SentenceSplitter (LlamaIndex)
```

Typical ranges: 256–1024 tokens per chunk, 10–20% overlap.
Larger chunks = more context but diluted relevance.
Smaller chunks = precise retrieval but may lose context.

### Common Anti-Patterns

1. **No reranking** — retrieval without reranking often returns semantically adjacent but irrelevant chunks
2. **Fixed chunk size for all doc types** — code and prose need different strategies
3. **Ignoring metadata filtering** — vector search alone is insufficient; combine with metadata filters
4. **No evaluation pipeline** — flying blind without retrieval metrics (recall@k, MRR, nDCG)
5. **Synchronous embedding at query time** — batch and pre-compute where possible
6. **Single retrieval strategy** — hybrid search (BM25 + dense) consistently outperforms either alone
7. **No prompt versioning** — prompts are code; version and test them
8. **Ignoring token costs** — track cost per query; cache aggressively
9. **Monolithic agents** — decompose into smaller, testable sub-agents
10. **No fallback model** — always have a secondary LLM provider configured

---

## Evaluation Framework

### RAG Evaluation Dimensions

| Dimension | Metric | Tool |
|-----------|--------|------|
| Retrieval quality | Recall@k, MRR, nDCG, Hit Rate | RAGAS, custom |
| Answer faithfulness | Groundedness (no hallucination) | RAGAS, DeepEval, LLM-as-judge |
| Answer relevance | Does it address the query? | LLM-as-judge, human eval |
| Context relevance | Is retrieved context useful? | RAGAS context_precision |
| Latency | E2E, retrieval, generation | OpenTelemetry, LangSmith |
| Cost | $/query, tokens/query | Custom tracking |

### Evaluation Pipeline

```python
# Minimal evaluation pattern
# 1. Create golden dataset: (query, expected_contexts, expected_answer)
# 2. Run pipeline on queries
# 3. Compare retrieved contexts vs expected (retrieval metrics)
# 4. Compare generated answer vs expected (generation metrics)
# 5. Use LLM-as-judge for nuanced assessment
# 6. Track metrics over time in CI/CD
```

---

## Quick Reference: Key APIs

### LangChain LCEL (LangChain Expression Language)

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

chain = ChatPromptTemplate.from_template("Summarize: {text}") | ChatOpenAI(model="gpt-4o") | StrOutputParser()
result = chain.invoke({"text": "..."})
```

### LlamaIndex Core

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine(similarity_top_k=5)
response = query_engine.query("What is...?")
```

### Qdrant with LangChain

```python
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings

vectorstore = QdrantVectorStore.from_documents(
    docs, OpenAIEmbeddings(model="text-embedding-3-large"),
    url="http://localhost:6333", collection_name="my_collection",
)
retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 10})
```

### LangGraph Agent

```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]

graph = StateGraph(State)
graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)
graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", should_continue, {"continue": "tools", "end": END})
graph.add_edge("tools", "agent")
app = graph.compile()
```

# Vector Databases Reference

## Table of Contents
1. [Comparison Matrix](#comparison-matrix)
2. [Index Algorithms](#index-algorithms)
3. [Pinecone](#pinecone)
4. [Qdrant](#qdrant)
5. [Weaviate](#weaviate)
6. [Chroma](#chroma)
7. [Milvus](#milvus)
8. [pgvector](#pgvector)
9. [MongoDB Atlas Vector Search](#mongodb-atlas-vector-search)
10. [Hybrid Search Patterns](#hybrid-search-patterns)
11. [Performance Tuning](#performance-tuning)

---

## Comparison Matrix

| Feature | Pinecone | Qdrant | Weaviate | Chroma | Milvus | pgvector | MongoDB Atlas |
|---------|----------|--------|----------|--------|--------|----------|---------------|
| Hosting | Managed only | Self/Cloud | Self/Cloud | Self/Cloud | Self/Cloud | Self (PG ext) | Managed |
| Language | - | Rust | Go | Python/Rust | Go/C++ | C (PG ext) | - |
| Hybrid search | Yes | Yes | Yes (BM25) | No | Yes | w/ tsvector | Yes (Atlas Search) |
| Filtering | Metadata | Payload filters | Where filters | Where filters | Boolean expr | SQL WHERE | MQL |
| Multi-tenancy | Namespaces | Collection + payload | Multi-tenant class | Collections | Partitions | schemas/RLS | DB per tenant |
| Max dimensions | 20,000 | 65,535 | Unlimited | Unlimited | 32,768 | 16,000 | 4,096 |
| Quantization | Yes | Scalar, PQ, BQ | PQ, BQ, SQ | No | SQ, PQ, IVF | halfvec | No |
| GPU acceleration | No | No | No | No | Yes (Knowhere) | No | No |
| RBAC | Yes | API keys | OIDC/API keys | None | Yes | PostgreSQL | Atlas RBAC |
| License | Proprietary | Apache 2.0 | BSD-3 | Apache 2.0 | Apache 2.0 | PostgreSQL | SSPL |

---

## Index Algorithms

### HNSW (Hierarchical Navigable Small World)
- **Used by**: Qdrant, Weaviate, pgvector (with pgvectorscale), Milvus, Pinecone, MongoDB Atlas
- **Pros**: Excellent recall, fast search, no training needed
- **Cons**: High memory usage, slow index build
- **Key params**: `M` (connections per layer, 16-64), `ef_construction` (build quality, 128-512), `ef` (search quality, 64-512)
- **When**: Default choice for most use cases <10M vectors

### IVF (Inverted File Index)
- **Used by**: Milvus, pgvector (ivfflat)
- **Pros**: Lower memory than HNSW, supports quantization well
- **Cons**: Requires training (clustering), lower recall
- **Key params**: `nlist` (number of clusters), `nprobe` (clusters to search)
- **When**: Large datasets where memory is constrained

### DiskANN
- **Used by**: Pinecone (internal), Milvus (experimental), pgvectorscale
- **Pros**: SSD-based, handles billion-scale, low memory
- **Cons**: Slower than in-memory HNSW
- **When**: Billion-scale datasets that don't fit in RAM

### Quantization Types
- **Scalar Quantization (SQ)**: Float32 → Int8. 4x compression, minimal quality loss
- **Product Quantization (PQ)**: Splits vector into subvectors, quantizes each. 16-64x compression
- **Binary Quantization (BQ)**: Float → binary. 32x compression, best with high-dimensional embeddings (≥1024d)
- **Matryoshka (MRL)**: Trained to allow dimension truncation. Not DB-level but embedding-level

---

## Pinecone

Fully managed, serverless vector database. Zero-ops.

### Setup & Indexing

```python
from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(api_key="...")

# Create index
pc.create_index(
    name="my-index",
    dimension=1536,
    metric="cosine",  # "cosine", "euclidean", "dotproduct"
    spec=ServerlessSpec(cloud="aws", region="us-east-1"),
)

index = pc.Index("my-index")

# Upsert vectors
index.upsert(
    vectors=[
        {"id": "doc-1", "values": [0.1, 0.2, ...], "metadata": {"source": "wiki", "year": 2024}},
    ],
    namespace="production",
)

# Upsert with sparse values (hybrid search)
index.upsert(vectors=[{
    "id": "doc-1",
    "values": dense_vector,
    "sparse_values": {"indices": [10, 45, 312], "values": [0.5, 0.3, 0.8]},
    "metadata": {"source": "wiki"},
}])
```

### Querying

```python
results = index.query(
    vector=[0.1, 0.2, ...],
    top_k=10,
    include_metadata=True,
    include_values=False,
    filter={"year": {"$gte": 2023}, "source": {"$in": ["wiki", "arxiv"]}},
    namespace="production",
)

# Hybrid query (dense + sparse)
results = index.query(
    vector=dense_vector,
    sparse_vector={"indices": [10, 45], "values": [0.5, 0.3]},
    top_k=10,
    alpha=0.5,  # Balance dense vs sparse (via integrated reranking or client-side)
)
```

### LangChain Integration

```python
from langchain_pinecone import PineconeVectorStore

vectorstore = PineconeVectorStore(
    index=index, embedding=embeddings, text_key="text", namespace="production"
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 10, "filter": {"year": 2024}})
```

---

## Qdrant

High-performance, Rust-based vector database with rich filtering and payload support.

### Setup & Collections

```python
from qdrant_client import QdrantClient, models

client = QdrantClient(url="http://localhost:6333")  # or QdrantClient(":memory:")

client.create_collection(
    collection_name="documents",
    vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
    # Named vectors for multi-vector
    # vectors_config={
    #     "title": models.VectorParams(size=384, distance=models.Distance.COSINE),
    #     "content": models.VectorParams(size=1536, distance=models.Distance.COSINE),
    # },
    optimizers_config=models.OptimizersConfigDiff(
        indexing_threshold=20000,  # Build HNSW after N points
    ),
    quantization_config=models.ScalarQuantization(
        scalar=models.ScalarQuantizationConfig(type=models.ScalarType.INT8, always_ram=True),
    ),
)
```

### Upsert & Search

```python
# Upsert
client.upsert(
    collection_name="documents",
    points=[
        models.PointStruct(
            id="doc-1",  # str or int
            vector=[0.1, 0.2, ...],
            payload={"text": "...", "source": "wiki", "year": 2024, "tags": ["ml", "nlp"]},
        ),
    ],
)

# Search with rich filtering
results = client.query_points(
    collection_name="documents",
    query=[0.1, 0.2, ...],
    limit=10,
    query_filter=models.Filter(
        must=[
            models.FieldCondition(key="year", range=models.Range(gte=2023)),
            models.FieldCondition(key="tags", match=models.MatchAny(any=["ml", "nlp"])),
        ],
        must_not=[
            models.FieldCondition(key="source", match=models.MatchValue(value="deprecated")),
        ],
    ),
    with_payload=True,
    score_threshold=0.7,
)

# Batch search (multiple queries at once)
results = client.query_batch_points(
    collection_name="documents",
    requests=[
        models.QueryRequest(query=[0.1, ...], limit=5),
        models.QueryRequest(query=[0.3, ...], limit=5, filter=...),
    ],
)
```

### Hybrid Search with Qdrant (Sparse + Dense)

```python
# Create collection with sparse + dense vectors
client.create_collection(
    collection_name="hybrid",
    vectors_config={"dense": models.VectorParams(size=1536, distance=models.Distance.COSINE)},
    sparse_vectors_config={"sparse": models.SparseVectorParams()},
)

# Query with fusion
from qdrant_client.models import Prefetch, FusionQuery, Fusion

results = client.query_points(
    collection_name="hybrid",
    prefetch=[
        Prefetch(query=dense_vector, using="dense", limit=20),
        Prefetch(query=models.SparseVector(indices=[...], values=[...]), using="sparse", limit=20),
    ],
    query=FusionQuery(fusion=Fusion.RRF),  # Reciprocal Rank Fusion
    limit=10,
)
```

---

## Weaviate

Object-oriented vector database with built-in vectorization modules and BM25.

### Setup

```python
import weaviate
from weaviate.classes.config import Configure, Property, DataType, VectorDistances

client = weaviate.connect_to_local()  # or weaviate.connect_to_weaviate_cloud(...)

collection = client.collections.create(
    name="Document",
    vectorizer_config=Configure.Vectorizer.text2vec_openai(model="text-embedding-3-large"),
    properties=[
        Property(name="text", data_type=DataType.TEXT),
        Property(name="source", data_type=DataType.TEXT, skip_vectorization=True),
        Property(name="year", data_type=DataType.INT),
    ],
    vector_index_config=Configure.VectorIndex.hnsw(
        distance_metric=VectorDistances.COSINE, ef=256, max_connections=32
    ),
)
```

### Hybrid Search (Native BM25 + Vector)

```python
collection = client.collections.get("Document")

# Pure vector search
results = collection.query.near_text(query="machine learning", limit=10)

# Pure BM25
results = collection.query.bm25(query="neural network architecture", limit=10)

# Hybrid (BM25 + vector with fusion)
results = collection.query.hybrid(
    query="transformer attention mechanism",
    alpha=0.75,  # 0=pure BM25, 1=pure vector
    limit=10,
    filters=weaviate.classes.query.Filter.by_property("year").greater_than(2022),
    fusion_type=weaviate.classes.query.HybridFusion.RELATIVE_SCORE,
)
```

---

## Chroma

Lightweight, in-process vector database. Great for prototyping.

```python
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")  # or chromadb.Client() for in-memory

collection = client.get_or_create_collection(
    name="documents",
    metadata={"hnsw:space": "cosine"},  # "l2", "ip", "cosine"
)

# Add documents (Chroma can auto-embed with default model)
collection.add(
    ids=["doc-1", "doc-2"],
    documents=["Text of doc 1", "Text of doc 2"],
    metadatas=[{"source": "wiki"}, {"source": "arxiv"}],
    # embeddings=[[0.1, ...], [0.2, ...]]  # Or provide pre-computed
)

# Query
results = collection.query(
    query_texts=["machine learning"],
    n_results=10,
    where={"source": {"$eq": "wiki"}},
    where_document={"$contains": "neural"},
    include=["documents", "metadatas", "distances"],
)
```

---

## Milvus

Billion-scale vector database with GPU acceleration and advanced indexing.

```python
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility

connections.connect(host="localhost", port="19530")

fields = [
    FieldSchema(name="id", dtype=DataType.VARCHAR, is_primary=True, max_length=128),
    FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=1536),
    FieldSchema(name="sparse_embedding", dtype=DataType.SPARSE_FLOAT_VECTOR),  # For hybrid
    FieldSchema(name="year", dtype=DataType.INT64),
]
schema = CollectionSchema(fields)
collection = Collection("documents", schema)

# Create index
collection.create_index("embedding", {
    "index_type": "HNSW",  # IVF_FLAT, IVF_SQ8, IVF_PQ, HNSW, DISKANN, GPU_IVF_FLAT
    "metric_type": "COSINE",
    "params": {"M": 32, "efConstruction": 256},
})

collection.load()

# Search
results = collection.search(
    data=[query_vector],
    anns_field="embedding",
    param={"metric_type": "COSINE", "params": {"ef": 128}},
    limit=10,
    expr='year >= 2023 and year <= 2025',
    output_fields=["text", "year"],
)

# Hybrid search with RRF
from pymilvus import AnnSearchRequest, RRFRanker

dense_req = AnnSearchRequest(data=[dense_vec], anns_field="embedding", param={"ef": 128}, limit=20)
sparse_req = AnnSearchRequest(data=[sparse_vec], anns_field="sparse_embedding", param={}, limit=20)

results = collection.hybrid_search(
    reqs=[dense_req, sparse_req],
    ranker=RRFRanker(k=60),
    limit=10,
    output_fields=["text"],
)
```

---

## pgvector

Vector similarity search as a PostgreSQL extension. Use existing PostgreSQL infrastructure.

```sql
-- Enable extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create table
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    content TEXT,
    metadata JSONB,
    embedding vector(1536)
);

-- HNSW index (preferred for most cases)
CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 256);

-- IVFFlat index (lower memory, requires training)
CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 1000);  -- sqrt(num_rows) to num_rows/1000

-- Halfvec for reduced storage (float16)
ALTER TABLE documents ADD COLUMN embedding_half halfvec(1536);

-- Query
SELECT id, content, 1 - (embedding <=> query_embedding::vector) AS similarity
FROM documents
WHERE metadata->>'year' >= '2023'
ORDER BY embedding <=> query_embedding::vector
LIMIT 10;

-- Set search params
SET hnsw.ef_search = 128;       -- Higher = better recall, slower
SET ivfflat.probes = 20;        -- More probes = better recall
```

### pgvector with Python

```python
# With SQLAlchemy + pgvector
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, Integer, Text, create_engine
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    embedding = Column(Vector(1536))

# With LangChain
from langchain_postgres import PGVector

vectorstore = PGVector(
    connection="postgresql://user:pass@localhost/db",
    embeddings=OpenAIEmbeddings(),
    collection_name="documents",
    use_jsonb=True,
)
```

### pgvectorscale (TimescaleDB extension)

Adds DiskANN-inspired index (StreamingDiskANN) for better performance at scale:

```sql
CREATE EXTENSION IF NOT EXISTS vectorscale;

CREATE INDEX ON documents USING diskann (embedding vector_cosine_ops)
    WITH (num_neighbors = 50, search_list_size = 100);
```

---

## MongoDB Atlas Vector Search

Vector search integrated into MongoDB Atlas.

```python
from pymongo import MongoClient

client = MongoClient("mongodb+srv://...")
collection = client["mydb"]["documents"]

# Create vector search index via Atlas UI or API
# Index definition:
# {
#   "mappings": {
#     "fields": {
#       "embedding": {"type": "knnVector", "dimensions": 1536, "similarity": "cosine"},
#       "year": {"type": "number"}
#     }
#   }
# }

# Vector search with pre-filter
results = collection.aggregate([
    {
        "$vectorSearch": {
            "index": "vector_index",
            "path": "embedding",
            "queryVector": query_vector,
            "numCandidates": 100,
            "limit": 10,
            "filter": {"year": {"$gte": 2023}},
        }
    },
    {"$project": {"content": 1, "score": {"$meta": "vectorSearchScore"}}},
])

# Hybrid: Combine with Atlas Search (full-text)
pipeline = [
    {"$vectorSearch": {...}},
    {"$unionWith": {
        "coll": "documents",
        "pipeline": [{"$search": {"text": {"query": "machine learning", "path": "content"}}}]
    }},
    # Reciprocal rank fusion or custom scoring
]
```

### LangChain Integration

```python
from langchain_mongodb import MongoDBAtlasVectorSearch

vectorstore = MongoDBAtlasVectorSearch(
    collection=collection,
    embedding=OpenAIEmbeddings(),
    index_name="vector_index",
    text_key="content",
    embedding_key="embedding",
)
```

---

## Hybrid Search Patterns

### Reciprocal Rank Fusion (RRF)

Standard way to combine multiple ranked lists:

```python
def reciprocal_rank_fusion(results_lists: list[list], k: int = 60) -> list:
    """Combine multiple result lists using RRF."""
    scores = {}
    for results in results_lists:
        for rank, doc in enumerate(results):
            doc_id = doc.id
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1)
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)
```

### Convex Combination (Weighted Fusion)

```python
def weighted_fusion(dense_results, sparse_results, alpha=0.7):
    """alpha: weight for dense scores (0=all sparse, 1=all dense)."""
    # Normalize scores to [0, 1]
    dense_scores = normalize(dense_results)
    sparse_scores = normalize(sparse_results)
    combined = alpha * dense_scores + (1 - alpha) * sparse_scores
    return sorted by combined
```

---

## Performance Tuning

### General Guidelines

1. **Right-size dimensions**: Use Matryoshka embeddings or models with selectable dims. 256-1024 often sufficient
2. **Enable quantization**: Scalar quantization (4x savings, <1% recall loss) is almost always worth it
3. **Tune HNSW params**: Higher `ef_construction` at index time; tune `ef_search` at query time
4. **Metadata indexes**: Create indexes on frequently-filtered fields
5. **Batch operations**: Always batch upserts (100-1000 per batch)
6. **Connection pooling**: Reuse clients; don't create per-request
7. **Pre-filter vs post-filter**: Pre-filter (filter before ANN) is faster for selective filters; post-filter for broad queries
8. **Monitoring**: Track p50/p95/p99 latencies, recall estimates, QPS

### Capacity Planning

```
Memory estimate (HNSW, float32, no quantization):
  vectors × dimensions × 4 bytes × 1.5 (HNSW overhead)

Example: 1M vectors × 1536 dims × 4 bytes × 1.5 ≈ 9.2 GB

With scalar quantization (int8): ÷ 4 ≈ 2.3 GB
With binary quantization: ÷ 32 ≈ 0.29 GB (but lower recall)
```