
import json
import re
import sys
from pathlib import Path

# Allow imports from the project root.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.retrieval.retriever import DocumentRetriever


DATASET_PATH = Path(__file__).parent / "retrieval_dataset.json"
DOCUMENTS_PATH = PROJECT_ROOT / "data" / "raw"
TOP_K = 3


def extract_source(result: str) -> str | None:
    """Extract the source filename from a retrieved passage."""
    match = re.search(r"\[Source:\s*(.*?)\]", result)
    return match.group(1).strip() if match else None


def main() -> None:
    with DATASET_PATH.open("r", encoding="utf-8") as file:
        dataset = json.load(file)

    retriever = DocumentRetriever()

    print("Indexing evaluation documents...")
    chunk_count = retriever.index_directory(DOCUMENTS_PATH)
    print(f"Indexed {chunk_count} chunks.\n")

    precision_scores = []
    recall_scores = []

    for item in dataset:
        question = item["question"]
        relevant_sources = set(item["relevant_sources"])

        results = retriever.search(question, top_k=TOP_K)

        retrieved_sources = [
            source
            for result in results
            if (source := extract_source(result)) is not None
        ]

        # Source-level Precision@K: relevant retrieved passages / K.
        relevant_hits = sum(
            source in relevant_sources
            for source in retrieved_sources
        )
        precision = relevant_hits / TOP_K if TOP_K else 0.0

        # Source-level Recall: relevant source files retrieved /
        # all source files labelled relevant for this question.
        unique_retrieved_relevant = (
            set(retrieved_sources) & relevant_sources
        )
        recall = (
            len(unique_retrieved_relevant) / len(relevant_sources)
            if relevant_sources
            else 0.0
        )

        precision_scores.append(precision)
        recall_scores.append(recall)

        print(f"Question: {question}")
        print(f"Expected sources: {sorted(relevant_sources)}")
        print(f"Retrieved sources: {retrieved_sources}")
        print(f"Precision@{TOP_K}: {precision:.2f}")
        print(f"Source Recall: {recall:.2f}")
        print("-" * 60)

    if dataset:
        print("\nOVERALL RESULTS")
        print(f"Queries evaluated: {len(dataset)}")
        print(
            f"Mean Precision@{TOP_K}: "
            f"{sum(precision_scores) / len(precision_scores):.2f}"
        )
        print(
            f"Mean Source Recall: "
            f"{sum(recall_scores) / len(recall_scores):.2f}"
        )

    print(
        "\nNote: These results are only meaningful after you verify "
        "the relevant_sources labels against the actual documents."
    )


if __name__ == "__main__":
    main()
