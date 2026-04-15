"""LangGraph agent: routes between RAG and MCP paths based on intent."""

from typing import TypedDict

from langchain_core.language_models import BaseLanguageModel
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import END, StateGraph

from src.agent.prompts import SYSTEM_PROMPT
from src.agent.routing import classify_intent
from src.config import CSV_PATH
from src.mcp_server.csv_tool import query_disasters


class AgentState(TypedDict):
    question: str
    intent: str
    context: str
    answer: str
    chat_history: list
    sources: list[str]


def _build_graph(
    llm: BaseLanguageModel,
    retriever=None,
    reranker_fn=None,
) -> StateGraph:
    """Build and compile the LangGraph StateGraph.

    Parameters
    ----------
    llm : language model for generation and routing
    retriever : optional HybridRetriever (or any object with .retrieve(query))
    reranker_fn : optional rerank(query, docs) callable
    """

    def classify_node(state: AgentState) -> dict:
        intent = classify_intent(state["question"], llm)
        return {"intent": intent}

    def retrieve_rag_node(state: AgentState) -> dict:
        if retriever is None:
            return {"context": "No RAG retriever configured.", "sources": []}

        docs = retriever.retrieve(state["question"])

        if reranker_fn is not None:
            docs = reranker_fn(state["question"], docs)

        context_parts = []
        sources = []
        for doc in docs:
            context_parts.append(doc.page_content)
            src = doc.metadata.get("filename", doc.metadata.get("source", "unknown"))
            page = doc.metadata.get("page", "")
            label = f"[Source: {src}" + (f", page {page}]" if page else "]")
            if label not in sources:
                sources.append(label)

        return {"context": "\n\n".join(context_parts), "sources": sources}

    def query_csv_node(state: AgentState) -> dict:
        # Use LLM to extract filter parameters from the question
        extraction_prompt = f"""\
Extract search filters from the user question for a disaster database query.
Return a Python dict with these optional keys (use None if not mentioned):
country, disaster_type, year (int), year_start (int), year_end (int), min_deaths (int), sort_by (str).

Question: {state["question"]}

Return ONLY a valid Python dict, nothing else."""

        response = llm.invoke([HumanMessage(content=extraction_prompt)])
        filters = _parse_filters(response.content)

        result = query_disasters(
            csv_path=CSV_PATH,
            country=filters.get("country"),
            disaster_type=filters.get("disaster_type"),
            year=filters.get("year"),
            year_range=(
                (filters["year_start"], filters["year_end"])
                if filters.get("year_start") and filters.get("year_end")
                else None
            ),
            min_deaths=filters.get("min_deaths"),
            sort_by=filters.get("sort_by", "Total Deaths"),
            limit=20,
        )

        if result.ok:
            context = f"Query results ({result.data['total_matching']} total matches, showing {result.data['count']}):\n"
            for row in result.data["rows"]:
                context += str(row) + "\n"
            sources = [f"[Source: EM-DAT CSV, {result.meta.timing_ms:.1f}ms]"]
        else:
            context = f"CSV query error: {result.error}"
            sources = []

        return {"context": context, "sources": sources}

    def retrieve_both_node(state: AgentState) -> dict:
        rag_result = retrieve_rag_node(state)
        csv_result = query_csv_node(state)

        context = (
            "=== Knowledge Base ===\n"
            + rag_result["context"]
            + "\n\n=== Disaster Data ===\n"
            + csv_result["context"]
        )
        sources = rag_result["sources"] + csv_result["sources"]
        return {"context": context, "sources": sources}

    def generate_node(state: AgentState) -> dict:
        history = state.get("chat_history", [])
        messages = [HumanMessage(content=SYSTEM_PROMPT)]

        for msg in history[-10:]:  # last 10 messages for context window
            if isinstance(msg, (HumanMessage, AIMessage)):
                messages.append(msg)

        user_msg = f"Context:\n{state['context']}\n\nQuestion: {state['question']}"
        messages.append(HumanMessage(content=user_msg))

        response = llm.invoke(messages)
        answer = response.content

        # Append sources if available
        if state.get("sources"):
            answer += "\n\nSources:\n" + "\n".join(state["sources"])

        return {
            "answer": answer,
            "chat_history": history
            + [
                HumanMessage(content=state["question"]),
                AIMessage(content=answer),
            ],
        }

    def general_node(state: AgentState) -> dict:
        messages = [
            HumanMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=state["question"]),
        ]
        response = llm.invoke(messages)
        history = state.get("chat_history", [])
        return {
            "answer": response.content,
            "context": "",
            "sources": [],
            "chat_history": history
            + [
                HumanMessage(content=state["question"]),
                AIMessage(content=response.content),
            ],
        }

    def route_by_intent(state: AgentState) -> str:
        intent = state.get("intent", "general")
        return {
            "disaster_data": "query_csv",
            "knowledge_base": "retrieve_rag",
            "mixed": "retrieve_both",
            "general": "general",
        }.get(intent, "general")

    # Build the graph
    graph = StateGraph(AgentState)

    graph.add_node("classify", classify_node)
    graph.add_node("retrieve_rag", retrieve_rag_node)
    graph.add_node("query_csv", query_csv_node)
    graph.add_node("retrieve_both", retrieve_both_node)
    graph.add_node("generate", generate_node)
    graph.add_node("general", general_node)

    graph.set_entry_point("classify")

    graph.add_conditional_edges(
        "classify",
        route_by_intent,
        {
            "retrieve_rag": "retrieve_rag",
            "query_csv": "query_csv",
            "retrieve_both": "retrieve_both",
            "general": "general",
        },
    )

    graph.add_edge("retrieve_rag", "generate")
    graph.add_edge("query_csv", "generate")
    graph.add_edge("retrieve_both", "generate")
    graph.add_edge("generate", END)
    graph.add_edge("general", END)

    return graph


def _parse_filters(text: str) -> dict:
    """Safely parse LLM-generated filter dict."""
    try:
        # Remove markdown code fence if present
        cleaned = text.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[1] if "\n" in cleaned else cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()
        if cleaned.startswith("python"):
            cleaned = cleaned[6:].strip()

        result = eval(cleaned, {"__builtins__": {}}, {"None": None, "True": True, "False": False})
        if isinstance(result, dict):
            return result
    except Exception:
        pass
    return {}


def build_agent(
    llm: BaseLanguageModel,
    retriever=None,
    reranker_fn=None,
):
    """Build and compile the agent graph. Returns a compiled graph."""
    graph = _build_graph(llm, retriever, reranker_fn)
    return graph.compile()
