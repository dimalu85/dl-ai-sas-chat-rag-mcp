"""Contract tests: agent with stubbed retriever and stubbed CSV tool."""

from unittest.mock import MagicMock

from langchain_core.documents import Document

from src.agent.graph import build_agent


def _mock_llm(intent: str = "knowledge_base", answer: str = "Test answer"):
    """Create a mock LLM that returns the intent on first call and answer on second."""
    mock = MagicMock()
    call_count = {"n": 0}

    def side_effect(messages):
        call_count["n"] += 1
        if call_count["n"] == 1:
            return MagicMock(content=intent)
        return MagicMock(content=answer)

    mock.invoke.side_effect = side_effect
    return mock


def _mock_retriever(docs=None):
    """Create a mock retriever."""
    retriever = MagicMock()
    if docs is None:
        docs = [
            Document(
                page_content="Earthquakes cause ground shaking.",
                metadata={"filename": "guide.pdf", "page": 3, "chunk_id": "c1"},
            )
        ]
    retriever.retrieve.return_value = docs
    return retriever


class TestAgentWithStubbedRetriever:
    def test_knowledge_base_routing(self):
        llm = _mock_llm(intent="knowledge_base", answer="Earthquakes are caused by tectonic plates.")
        retriever = _mock_retriever()

        agent = build_agent(llm, retriever=retriever)
        result = agent.invoke(
            {
                "question": "What causes earthquakes?",
                "intent": "",
                "context": "",
                "answer": "",
                "chat_history": [],
                "sources": [],
            }
        )

        assert result["intent"] == "knowledge_base"
        assert len(result["answer"]) > 0
        retriever.retrieve.assert_called_once()

    def test_no_retriever_graceful(self):
        llm = _mock_llm(intent="knowledge_base", answer="I have limited context.")
        agent = build_agent(llm, retriever=None)
        result = agent.invoke(
            {
                "question": "What causes floods?",
                "intent": "",
                "context": "",
                "answer": "",
                "chat_history": [],
                "sources": [],
            }
        )
        assert result["intent"] == "knowledge_base"
        assert len(result["answer"]) > 0


class TestAgentWithStubbedCSV:
    def test_disaster_data_routing(self):
        llm = _mock_llm(intent="disaster_data", answer="Based on the data...")

        # The second LLM call in query_csv_node extracts filters,
        # and the third generates the answer. Adjust mock accordingly.
        call_count = {"n": 0}

        def side_effect(messages):
            call_count["n"] += 1
            if call_count["n"] == 1:
                return MagicMock(content="disaster_data")
            elif call_count["n"] == 2:
                return MagicMock(content='{"country": "Japan", "disaster_type": "Earthquake"}')
            else:
                return MagicMock(content="Japan had 272 earthquake records.")

        llm.invoke.side_effect = side_effect

        agent = build_agent(llm)
        result = agent.invoke(
            {
                "question": "How many earthquakes in Japan?",
                "intent": "",
                "context": "",
                "answer": "",
                "chat_history": [],
                "sources": [],
            }
        )

        assert result["intent"] == "disaster_data"
        assert len(result["answer"]) > 0
        assert len(result["sources"]) > 0

    def test_general_routing_skips_tools(self):
        llm = _mock_llm(intent="general", answer="Hello! I can help with disasters.")
        agent = build_agent(llm)
        result = agent.invoke(
            {
                "question": "Hello!",
                "intent": "",
                "context": "",
                "answer": "",
                "chat_history": [],
                "sources": [],
            }
        )
        assert result["intent"] == "general"
        assert len(result["answer"]) > 0
