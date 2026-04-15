"""Query intent classification for routing to RAG vs MCP vs both."""

from langchain_core.language_models import BaseLanguageModel
from langchain_core.messages import HumanMessage, SystemMessage

from src.agent.prompts import ROUTING_PROMPT

VALID_INTENTS = {"disaster_data", "knowledge_base", "mixed", "general"}


def classify_intent(query: str, llm: BaseLanguageModel) -> str:
    """Classify a user query into one of the routing intents.

    Returns one of: disaster_data, knowledge_base, mixed, general.
    Falls back to 'mixed' if the LLM response is unexpected.
    """
    prompt = ROUTING_PROMPT.format(question=query)
    response = llm.invoke([HumanMessage(content=prompt)])

    intent = response.content.strip().lower().replace(" ", "_")

    if intent in VALID_INTENTS:
        return intent

    # Fallback: try to find a valid intent in the response
    for valid in VALID_INTENTS:
        if valid in intent:
            return valid

    return "mixed"
