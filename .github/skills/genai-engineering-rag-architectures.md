## Purpose

This skill provides production-grade guidance for building, deploying, and operating Generative AI systems. It covers the full stack from prompt engineering through production deployment across major frameworks, databases, and cloud platforms.

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

# RAG Architectures Reference

## Table of Contents
1. [RAG Taxonomy](#rag-taxonomy)
2. [Chunking Strategies](#chunking-strategies)
3. [Embedding Selection](#embedding-selection)
4. [Retrieval Strategies](#retrieval-strategies)
5. [Reranking](#reranking)
6. [Advanced RAG Patterns](#advanced-rag-patterns)
7. [Evaluation](#evaluation)
8. [Failure Modes & Debugging](#failure-modes--debugging)

---

## RAG Taxonomy

### Naive RAG
```
Query → Embed → Vector Search (top-k) → Stuff into prompt → LLM → Answer
```
Simple but limited. Issues: irrelevant retrieval, lost context, no source validation.

### Advanced RAG
Adds pre-retrieval, retrieval, and post-retrieval optimizations:
```
Query → [Query Transform] → [Multi-Strategy Retrieval] → [Reranking] → [Compression] → LLM → Answer
```

### Modular RAG
Composable pipeline with swappable components:
```
Query → Router → [Strategy A: Dense + Rerank]  ──┐
                 [Strategy B: Hybrid + Filter]   ──├→ Fusion → LLM → Answer
                 [Strategy C: Graph Retrieval]   ──┘
```

### Agentic RAG
Agent decides retrieval strategy dynamically:
```
Query → Agent → [Decide: need retrieval?]
                    ├─ Yes → [Which index?] → Retrieve → [Sufficient?]
                    │                                        ├─ No → Reformulate → Retry
                    │                                        └─ Yes → Generate
                    └─ No → Generate from knowledge
```

---

## Chunking Strategies

### Strategy Selection Guide

| Document Type | Recommended Strategy | Chunk Size | Overlap |
|--------------|---------------------|------------|---------|
| General prose | RecursiveCharacter / Sentence | 512-1024 tokens | 10-20% |
| Academic papers | Section-aware + Sentence | 512-768 tokens | 10% |
| Legal documents | Clause-level + hierarchical | 256-512 tokens | 15% |
| Code | AST-based / function-level | Whole functions | 0% |
| Markdown/HTML | Header-based hierarchy | Natural sections | 0% |
| Conversations | Message-boundary | Per message/turn | 0% |
| Tables | Row-serialize or structured | Full table or row groups | 0% |

### Implementation Patterns

**Semantic Chunking** (split at topic boundaries):
```python
# LlamaIndex
from llama_index.core.node_parser import SemanticSplitterNodeParser
parser = SemanticSplitterNodeParser(
    embed_model=embed_model,
    breakpoint_percentile_threshold=95,
    buffer_size=1,
)

# LangChain (experimental)
from langchain_experimental.text_splitter import SemanticChunker
splitter = SemanticChunker(
    embeddings=OpenAIEmbeddings(),
    breakpoint_threshold_type="percentile",
    breakpoint_threshold_amount=95,
)
```

**Hierarchical Chunking** (parent-child with different granularities):
```python
from llama_index.core.node_parser import HierarchicalNodeParser

parser = HierarchicalNodeParser.from_defaults(
    chunk_sizes=[2048, 512, 128],  # Parent → Child → Leaf
)
# Enables auto-merging retrieval: retrieve leaves, merge to parent if many match
```

**Document-Aware Chunking**:
```python
# Preserve document structure
from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    HTMLHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)

# Stage 1: Split by headers (preserves structure)
md_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=[("#", "h1"), ("##", "h2"), ("###", "h3")]
)
header_chunks = md_splitter.split_text(markdown_doc)

# Stage 2: Further split large sections
char_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=64)
final_chunks = char_splitter.split_documents(header_chunks)
# Metadata includes h1, h2, h3 headers → enables hierarchical filtering
```

### Metadata Enrichment

Always attach rich metadata to chunks:

```python
# Essential metadata per chunk
{
    "source": "path/to/file.pdf",
    "page": 5,
    "section": "3.2 Methodology",
    "doc_title": "Q3 2024 Report",
    "doc_type": "report",
    "date": "2024-10-15",
    "chunk_index": 12,
    "total_chunks": 45,
    # LLM-generated metadata (at ingestion time)
    "summary": "Describes the experimental setup...",
    "questions_answered": ["What methodology was used?", "How was data collected?"],
    "entities": ["BERT", "GPT-4", "ImageNet"],
}
```

---

## Embedding Selection

### Model Comparison (2025)

| Model | Dims | Multilingual | MRL | Cost | Notes |
|-------|------|-------------|-----|------|-------|
| OpenAI text-embedding-3-large | 3072 (adjustable) | Yes | Yes | ~$0.13/1M tokens | Best commercial all-rounder |
| OpenAI text-embedding-3-small | 1536 (adjustable) | Yes | Yes | ~$0.02/1M tokens | Cost-effective |
| Cohere embed-v4 | 1024 | Yes (100+ langs) | Yes | ~$0.10/1M tokens | Excellent multilingual, binary support |
| Google text-embedding-005 | 768 | Yes | Yes | Free tier available | Good quality, Vertex AI native |
| BAAI/bge-m3 | 1024 | Yes (100+ langs) | Yes | Free (open) | Best open-source multilingual |
| nomic-embed-text-v1.5 | 768 | English-focused | Yes | Free (open) | Strong English, long context (8192) |
| Jina embeddings-v3 | 1024 | Yes | Yes | Free (open) | Task-specific prefixes |

### Matryoshka Representation Learning (MRL)

Models supporting MRL allow dimension reduction without retraining:

```python
# OpenAI: just specify dimensions
from openai import OpenAI
client = OpenAI()
response = client.embeddings.create(
    model="text-embedding-3-large",
    input="Hello world",
    dimensions=512,  # Reduce from 3072 to 512
)
```

Typical quality retention: 1024d retains ~99% of 3072d quality; 256d retains ~95%.

### Embedding Best Practices

1. **Same model for indexing and querying** — always
2. **Prefix/instruction-based models**: Some models need task prefixes
   ```python
   # bge-m3, Jina, E5
   query = "query: What is HNSW?"        # For queries
   doc = "passage: HNSW is an algorithm..."  # For documents
   ```
3. **Batch processing**: Embed in batches of 100-1000 for throughput
4. **Normalize**: If your DB doesn't auto-normalize, normalize for cosine similarity
5. **Cache embeddings**: Don't re-embed the same text

---

## Retrieval Strategies

### Dense Retrieval (Vector Search)

Standard semantic similarity search. Good for meaning-based queries.

### Sparse Retrieval (BM25 / Keyword)

Term-frequency based. Good for exact matches, names, acronyms, codes.

```python
# BM25 with rank_bm25
from rank_bm25 import BM25Okapi

tokenized_corpus = [doc.split() for doc in corpus]
bm25 = BM25Okapi(tokenized_corpus)
scores = bm25.get_scores(query.split())

# Learned sparse: SPLADE, SPLADEv3
# Generates sparse vectors that capture semantic term expansion
```

### Hybrid Search (Dense + Sparse)

Consistently outperforms either alone. Combine via RRF or weighted fusion.

```python
# Pattern: Hybrid retriever
class HybridRetriever:
    def __init__(self, dense_retriever, sparse_retriever, weights=(0.7, 0.3)):
        self.dense = dense_retriever
        self.sparse = sparse_retriever
        self.weights = weights

    def retrieve(self, query, k=10):
        dense_results = self.dense.retrieve(query, k=k * 2)
        sparse_results = self.sparse.retrieve(query, k=k * 2)
        return reciprocal_rank_fusion([dense_results, sparse_results])[:k]
```

### Multi-Query Retrieval

Generate multiple query reformulations to improve recall:

```python
# LangChain
from langchain.retrievers import MultiQueryRetriever

multi_retriever = MultiQueryRetriever.from_llm(
    retriever=base_retriever,
    llm=ChatOpenAI(temperature=0.3),
)
# Generates 3+ query variants, retrieves for each, deduplicates
```

### HyDE (Hypothetical Document Embeddings)

Generate a hypothetical answer, embed it, search with that:

```python
def hyde_retrieve(query, llm, retriever):
    # Step 1: Generate hypothetical answer
    hypothetical = llm.invoke(f"Write a passage that answers: {query}")
    # Step 2: Embed the hypothetical answer
    # Step 3: Search with that embedding
    return retriever.invoke(hypothetical.content)
```

### Contextual Retrieval (Anthropic pattern)

Prepend document-level context to each chunk before embedding:

```python
def add_contextual_header(chunk, document):
    context = llm.invoke(
        f"Given the full document:\n{document[:3000]}\n\n"
        f"Provide 1-2 sentences of context for this chunk:\n{chunk}"
    )
    return f"{context}\n\n{chunk}"
```

This reduces retrieval failure by 35-49% when combined with BM25 (per Anthropic research).

### Parent Document Retrieval

Embed small chunks for precision, return parent chunks for context:

```python
from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore

parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000)
child_splitter = RecursiveCharacterTextSplitter(chunk_size=400)

retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=InMemoryStore(),
    child_splitter=child_splitter,
    parent_splitter=parent_splitter,
)
```

---

## Reranking

Reranking is the single highest-impact improvement for most RAG systems. It re-scores retrieved documents using a cross-encoder (sees query + document together).

### Cross-Encoder Reranking

```python
# Cohere Rerank (API)
from langchain_cohere import CohereRerank
reranker = CohereRerank(model="rerank-v3.5", top_n=5)

# Open-source: BAAI/bge-reranker-v2-m3
from sentence_transformers import CrossEncoder
reranker = CrossEncoder("BAAI/bge-reranker-v2-m3", max_length=1024)
scores = reranker.predict([(query, doc) for doc in documents])

# Jina Reranker
from langchain_community.document_compressors import JinaRerank
reranker = JinaRerank(model="jina-reranker-v2-base-multilingual", top_n=5)
```

### ColBERT (Late Interaction)

Token-level similarity for fine-grained matching. Better than cross-encoders for long documents.

```python
# RAGatouille (ColBERT wrapper)
from ragatouille import RAGPretrainedModel

colbert = RAGPretrainedModel.from_pretrained("colbert-ir/colbertv2.0")
colbert.index(collection=texts, index_name="my_index")
results = colbert.search(query="What is HNSW?", k=10)
```

### Reranking Pipeline Pattern

```python
# Two-stage retrieval: broad recall → precise reranking
def two_stage_retrieve(query, k_initial=50, k_final=5):
    # Stage 1: Fast ANN retrieval (high recall)
    candidates = vector_retriever.retrieve(query, k=k_initial)

    # Stage 2: Cross-encoder reranking (high precision)
    reranked = reranker.rerank(query, candidates, top_n=k_final)

    return reranked
```

---

## Advanced RAG Patterns

### Corrective RAG (CRAG)

Evaluates retrieval quality and falls back to web search if poor:

```python
# LangGraph implementation
def grade_documents(state):
    """Grade retrieved documents for relevance."""
    query = state["question"]
    docs = state["documents"]
    graded = []
    for doc in docs:
        score = relevance_grader.invoke({"question": query, "document": doc.page_content})
        if score.relevant:
            graded.append(doc)
    if len(graded) < 2:
        return {"documents": graded, "next": "web_search"}  # Fallback
    return {"documents": graded, "next": "generate"}
```

### Self-RAG

LLM decides: (1) whether to retrieve, (2) if retrieved docs are relevant, (3) if answer is supported:

```python
# Decision points in the pipeline
def self_rag_pipeline(query):
    # Step 1: Does this need retrieval?
    needs_retrieval = llm.invoke(f"Does this query need external knowledge? {query}")
    if not needs_retrieval:
        return llm.invoke(query)

    # Step 2: Retrieve and grade
    docs = retriever.invoke(query)
    relevant_docs = [d for d in docs if grade_relevance(query, d)]

    # Step 3: Generate
    answer = llm.invoke(prompt.format(context=relevant_docs, question=query))

    # Step 4: Hallucination check
    if not is_grounded(answer, relevant_docs):
        return regenerate_with_stricter_prompt(query, relevant_docs)

    return answer
```

### Adaptive RAG

Routes queries to different strategies based on complexity:

```python
def route_query(query):
    classification = classifier.invoke(query)
    if classification == "simple_factual":
        return direct_retrieval_pipeline(query)
    elif classification == "multi_step":
        return decompose_and_retrieve(query)
    elif classification == "analytical":
        return full_document_analysis(query)
    elif classification == "conversational":
        return chat_with_history_pipeline(query)
```

### Graph RAG

Combines knowledge graphs with vector retrieval:

```python
# Entity extraction → Graph construction → Graph + Vector retrieval
# LlamaIndex PropertyGraphIndex is the easiest implementation
# Microsoft GraphRAG for community summarization approach

# Pattern: Query both graph and vector, fuse results
def graph_rag_retrieve(query):
    # Vector retrieval for semantic matches
    vector_results = vector_retriever.retrieve(query, k=10)

    # Graph retrieval for structural/relational matches
    entities = extract_entities(query)
    graph_results = knowledge_graph.get_subgraph(entities, hops=2)

    # Fuse
    context = merge_contexts(vector_results, graph_results)
    return context
```

### Query Decomposition

Break complex queries into sub-queries:

```python
def decompose_query(complex_query):
    sub_queries = llm.invoke(
        f"Break this complex question into 2-4 simpler sub-questions:\n{complex_query}"
    )
    results = []
    for sq in sub_queries:
        results.append(retriever.invoke(sq))
    # Synthesize across all sub-results
    return synthesize(complex_query, results)
```

### Step-Back Prompting

Ask a more general question first, then use that context:

```python
def step_back_retrieve(query):
    step_back_query = llm.invoke(f"What is a more general question that would help answer: {query}")
    general_context = retriever.invoke(step_back_query)
    specific_context = retriever.invoke(query)
    return generate(query, general_context + specific_context)
```

---

## Evaluation

### Metrics

**Retrieval Metrics**:
- **Recall@K**: Fraction of relevant docs in top-K results
- **Precision@K**: Fraction of top-K that are relevant
- **MRR (Mean Reciprocal Rank)**: 1/rank of first relevant result
- **nDCG (Normalized Discounted Cumulative Gain)**: Position-weighted relevance
- **Hit Rate**: Fraction of queries where at least one relevant doc is in top-K

**Generation Metrics**:
- **Faithfulness/Groundedness**: Is the answer supported by retrieved context?
- **Answer Relevance**: Does the answer address the query?
- **Answer Correctness**: Is the answer factually correct?

### Evaluation Frameworks

```python
# RAGAS
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall

result = evaluate(
    dataset=eval_dataset,  # HF Dataset with question, answer, contexts, ground_truth
    metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
)

# DeepEval
from deepeval.metrics import GEval, FaithfulnessMetric
from deepeval.test_case import LLMTestCase

metric = FaithfulnessMetric(threshold=0.7)
test_case = LLMTestCase(input=query, actual_output=answer, retrieval_context=contexts)
metric.measure(test_case)
```

---

## Failure Modes & Debugging

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Irrelevant results | Embedding mismatch, bad chunks | Check embedding model consistency, adjust chunk size |
| Missing obvious docs | Low recall, bad query | Add hybrid search, multi-query, increase top-k |
| Hallucinated answers | Poor grounding | Add reranking, faithfulness checking, cite sources |
| "I don't know" for answerable queries | Over-filtered, low top-k | Relax filters, increase k, check metadata |
| Slow queries | Large top-k, no index, no caching | Optimize index, reduce k, add semantic cache |
| Inconsistent answers | Non-deterministic retrieval | Set temperature=0, fix random seeds, increase k |
| Context window overflow | Too many/large chunks | Reduce chunk size, reduce k, compress context |
| Wrong document selected (multi-index) | Bad routing | Improve index descriptions, add routing evaluation |

### Debugging Checklist

1. **Inspect retrieved chunks**: Always log and review what's actually retrieved
2. **Check embedding similarity scores**: Are scores reasonable? (>0.7 for cosine usually indicates relevance)
3. **Test retrieval independently**: Separate retrieval quality from generation quality
4. **Compare with BM25 baseline**: If BM25 finds it but vector search doesn't, the embedding may be inappropriate
5. **Evaluate on golden dataset**: 50-100 query-answer pairs with expected source documents
6. **A/B test changes**: Never change chunking + embedding + retrieval simultaneously

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

---

