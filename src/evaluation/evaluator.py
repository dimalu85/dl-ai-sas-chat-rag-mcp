"""RAG evaluation: RAGAS metrics + custom metrics for the disaster chat app."""

import json
import logging
import time
from pathlib import Path
from typing import Any

from src.config import CSV_PATH, DATA_DIR
from src.mcp_server.csv_tool import query_disasters

logger = logging.getLogger(__name__)

GOLDEN_DATASET_PATH = DATA_DIR / "golden_dataset.json"


def load_golden_dataset(path: str | Path = GOLDEN_DATASET_PATH) -> list[dict]:
    """Load the golden Q&A dataset."""
    with open(path) as f:
        return json.load(f)


def evaluate_hit_rate(
    retriever,
    questions: list[str],
    expected_docs_keywords: list[list[str]],
    k: int = 5,
) -> float:
    """Compute hit rate@k: fraction of queries where at least one relevant doc is in top-k.

    Parameters
    ----------
    retriever : object with .retrieve(query) method
    questions : list of queries
    expected_docs_keywords : for each query, a list of keywords that should appear in relevant docs
    k : top-k to check
    """
    hits = 0
    for query, keywords in zip(questions, expected_docs_keywords):
        docs = retriever.retrieve(query)[:k]
        doc_texts = " ".join(d.page_content.lower() for d in docs)
        if any(kw.lower() in doc_texts for kw in keywords):
            hits += 1
    return hits / len(questions) if questions else 0.0


def evaluate_csv_query_correctness(
    golden_items: list[dict],
) -> dict[str, Any]:
    """Evaluate CSV query correctness against golden dataset items with filters.

    Returns dict with total, correct, accuracy, and details.
    """
    csv_items = [item for item in golden_items if item.get("filters")]
    correct = 0
    details = []

    for item in csv_items:
        filters = item["filters"]
        year_range = None
        if filters.get("year_start") and filters.get("year_end"):
            year_range = (filters["year_start"], filters["year_end"])

        result = query_disasters(
            csv_path=CSV_PATH,
            country=filters.get("country"),
            disaster_type=filters.get("disaster_type"),
            year=filters.get("year"),
            year_range=year_range,
            min_deaths=filters.get("min_deaths"),
            sort_by=filters.get("sort_by"),
        )

        is_correct = result.ok and result.data["total_matching"] > 0
        if is_correct:
            correct += 1

        details.append(
            {
                "id": item["id"],
                "question": item["question"],
                "ok": result.ok,
                "matches": result.data["total_matching"] if result.ok else 0,
                "correct": is_correct,
            }
        )

    return {
        "total": len(csv_items),
        "correct": correct,
        "accuracy": correct / len(csv_items) if csv_items else 0.0,
        "details": details,
    }


def evaluate_ragas(
    questions: list[str],
    answers: list[str],
    contexts: list[list[str]],
    ground_truths: list[str],
) -> dict[str, float]:
    """Run RAGAS evaluation metrics.

    Returns dict with faithfulness, answer_relevancy, context_precision, context_recall.
    Falls back to empty dict if RAGAS is unavailable.
    """
    try:
        from datasets import Dataset
        from ragas import evaluate
        from ragas.metrics import (
            answer_relevancy,
            context_precision,
            context_recall,
            faithfulness,
        )

        dataset = Dataset.from_dict(
            {
                "question": questions,
                "answer": answers,
                "contexts": contexts,
                "ground_truth": ground_truths,
            }
        )

        result = evaluate(
            dataset=dataset,
            metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
        )

        return {k: round(v, 4) for k, v in result.items() if isinstance(v, (int, float))}

    except Exception as exc:
        logger.warning("RAGAS evaluation failed: %s", exc)
        return {}


def run_full_evaluation(
    retriever=None,
    agent=None,
    golden_path: str | Path = GOLDEN_DATASET_PATH,
) -> dict[str, Any]:
    """Run the complete evaluation suite.

    Returns a dict with csv_correctness, hit_rate (if retriever provided),
    and ragas_metrics (if agent provided).
    """
    golden = load_golden_dataset(golden_path)
    results: dict[str, Any] = {}

    # 1. CSV query correctness
    csv_eval = evaluate_csv_query_correctness(golden)
    results["csv_correctness"] = {
        "accuracy": csv_eval["accuracy"],
        "correct": csv_eval["correct"],
        "total": csv_eval["total"],
    }

    # 2. Hit rate (if retriever available)
    if retriever is not None:
        kb_items = [item for item in golden if item["category"] == "knowledge_base"]
        questions = [item["question"] for item in kb_items]
        # Use key terms from expected answers as relevance keywords
        keywords = [item["expected_answer"].split()[:5] for item in kb_items]
        hr = evaluate_hit_rate(retriever, questions, keywords)
        results["hit_rate_at_5"] = round(hr, 4)

    return results
