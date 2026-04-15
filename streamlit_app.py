# streamlit_app.py — Streamlit chat UI for Natural Disaster Assistant
import os
import sys
import warnings

warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.abspath("."))

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Natural Disaster Assistant", page_icon="🌍", layout="wide")

# ── Sidebar ──────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("🌍 Natural Disaster Assistant")
    st.caption("EM-DAT Dataset (1970–2021) · RAG + MCP · LangGraph")
    st.markdown("---")
    st.markdown(
        "**Capabilities**\n"
        "- 📊 Query disaster statistics (CSV/MCP)\n"
        "- 📚 Search knowledge base (RAG)\n"
        "- 🔀 Combine both for complex questions\n"
        "- 💬 General disaster-related chat"
    )
    st.markdown("---")
    if st.button("🗑️ Clear chat"):
        st.session_state.messages = []
        st.session_state.agent_history = []
        st.rerun()


# ── Agent initialisation (cached across reruns) ─────────────────────────
@st.cache_resource(show_spinner="Loading models & building agent…")
def _init_agent():
    from pathlib import Path

    from langchain_openai import ChatOpenAI

    from src.agent.graph import build_agent
    from src.config import (
        CHROMA_PERSIST_DIR,
        CSV_PATH,
        HF_EMBEDDING_MODEL,
        LLM_MODEL,
        LLM_TEMPERATURE,
    )
    from src.ingestion.chunking import build_parent_child_chunks
    from src.ingestion.loaders import load_csv_as_docs
    from src.retrieval.hybrid import HybridRetriever
    from src.retrieval.reranker import rerank
    from src.retrieval.vectorstore import (
        create_vectorstore,
        get_embeddings,
        load_vectorstore,
    )

    # Load documents & build chunks
    csv_docs = load_csv_as_docs(CSV_PATH)
    _, child_chunks = build_parent_child_chunks(csv_docs)

    # Vector store
    embeddings = get_embeddings(prefer_hf=True)
    chroma_path = Path(CHROMA_PERSIST_DIR)
    if chroma_path.exists() and any(chroma_path.iterdir()):
        vectorstore = load_vectorstore(chroma_path, embeddings)
    else:
        vectorstore = create_vectorstore(child_chunks, chroma_path, embeddings)

    # Retriever + agent
    retriever = HybridRetriever(vectorstore, child_chunks)
    llm = ChatOpenAI(model=LLM_MODEL, temperature=LLM_TEMPERATURE)
    agent = build_agent(llm, retriever=retriever, reranker_fn=rerank)
    return agent


agent = _init_agent()

# ── Chat state ───────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent_history" not in st.session_state:
    st.session_state.agent_history = []

st.title("🌍 Natural Disaster Chat")

# Render previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Example prompts ──────────────────────────────────────────────────────
EXAMPLES = [
    "How many earthquakes occurred in Japan between 2000 and 2020?",
    "What causes tsunamis and how do early warning systems work?",
    "Why was the 2010 Haiti earthquake so deadly compared to others?",
    "Which country had the most floods in the last decade?",
    "Compare drought impacts across Africa and Asia",
]

if not st.session_state.messages:
    st.info("Try asking:\n" + "\n".join(f"- *{e}*" for e in EXAMPLES))

# ── User input ───────────────────────────────────────────────────────────
if prompt := st.chat_input("Ask about natural disasters…"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            result = agent.invoke(
                {
                    "question": prompt,
                    "intent": "",
                    "context": "",
                    "answer": "",
                    "chat_history": st.session_state.agent_history,
                    "sources": [],
                }
            )
            answer = result["answer"]
            intent = result.get("intent", "")
            st.session_state.agent_history = result.get("chat_history", [])

        st.markdown(answer)

        if intent:
            st.caption(f"🔀 Route: **{intent}**")

    st.session_state.messages.append({"role": "assistant", "content": answer})
