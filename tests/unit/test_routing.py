"""Unit tests for src.agent.routing — intent classification with mock LLM."""

from unittest.mock import MagicMock

from src.agent.routing import classify_intent


def _mock_llm(response_text: str) -> MagicMock:
    mock = MagicMock()
    mock.invoke.return_value = MagicMock(content=response_text)
    return mock


class TestClassifyIntent:
    def test_disaster_data(self):
        llm = _mock_llm("disaster_data")
        assert classify_intent("How many earthquakes in Japan?", llm) == "disaster_data"

    def test_knowledge_base(self):
        llm = _mock_llm("knowledge_base")
        assert classify_intent("What causes tsunamis?", llm) == "knowledge_base"

    def test_mixed(self):
        llm = _mock_llm("mixed")
        assert classify_intent("Why was Haiti 2010 so deadly?", llm) == "mixed"

    def test_general(self):
        llm = _mock_llm("general")
        assert classify_intent("Hello!", llm) == "general"

    def test_whitespace_handling(self):
        llm = _mock_llm("  disaster_data  \n")
        assert classify_intent("earthquakes?", llm) == "disaster_data"

    def test_case_insensitive(self):
        llm = _mock_llm("Knowledge_Base")
        assert classify_intent("explain sendai", llm) == "knowledge_base"

    def test_fallback_on_garbage(self):
        llm = _mock_llm("I think this is about data analysis")
        assert classify_intent("test", llm) == "mixed"

    def test_partial_match_disaster_data(self):
        llm = _mock_llm("This is disaster_data related")
        assert classify_intent("count floods", llm) == "disaster_data"

    def test_partial_match_knowledge_base(self):
        llm = _mock_llm("Probably knowledge_base category")
        assert classify_intent("explain concept", llm) == "knowledge_base"

    def test_llm_called_with_question(self):
        llm = _mock_llm("general")
        classify_intent("test question", llm)
        args = llm.invoke.call_args[0][0]
        assert any("test question" in str(msg) for msg in args)
