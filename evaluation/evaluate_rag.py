
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.generation.guardrails import GuardrailService
from app.generation.rag_service import RAGService
from app.retrieval.retriever import DocumentRetriever
from app.api.chat import extract_sources


DATASET_PATH = Path(__file__).parent / "answer_quality_dataset.json"
RESULTS_PATH = Path(__file__).parent / "automated_rag_results.json"
DOCUMENTS_PATH = PROJECT_ROOT / "data" / "raw"
TOP_K = 3


def calculate_fact_coverage(
    answer: str,
    expected_facts: list[str],
) -> dict:
    """Measure how many expected phrases appear in the answer."""
    normalized_answer = answer.casefold()

    matched_facts = [
        fact
        for fact in expected_facts
        if fact.casefold() in normalized_answer
    ]

    missing_facts = [
        fact
        for fact in expected_facts
        if fact.casefold() not in normalized_answer
    ]

    coverage = (
        len(matched_facts) / len(expected_facts)
        if expected_facts
        else 1.0
    )

    return {
        "expected_fact_count": len(expected_facts),
        "matched_facts": matched_facts,
        "missing_facts": missing_facts,
        "fact_coverage": round(coverage, 4),
    }


def main() -> None:
    with DATASET_PATH.open("r", encoding="utf-8") as file:
        dataset = json.load(file)

    print("Indexing evaluation documents...")
    retriever = DocumentRetriever()
    chunk_count = retriever.index_directory(DOCUMENTS_PATH)
    print(f"Indexed {chunk_count} chunks.")

    guardrails = GuardrailService()
    rag_service = RAGService()
    results = []

    for index, item in enumerate(dataset, start=1):
        question = item["question"]
        expected_sources = set(item["expected_sources"])

        print(f"\n[{index}/{len(dataset)}] {question}")

        try:
            classification = guardrails.classify_question(question)

            if classification != "IN_SCOPE":
                result = {
                    "question": question,
                    "status": "SKIPPED",
                    "reason": (
                        f"Guardrail classification: {classification}"
                    ),
                }
                results.append(result)
                print(f"Skipped: {classification}")
                continue

            # Retrieve relevant evidence.
            chunks = retriever.search(question, top_k=TOP_K)

            if not chunks:
                answer = (
                    "I could not find sufficient evidence to answer "
                    "this question in the available documents."
                )
                sources = []
            else:
                # Generate an answer from retrieved evidence.
                answer = rag_service.answer_question(question, chunks)
                sources = extract_sources(chunks)

            # Extract document names from the retrieved evidence.
            retrieved_documents = {
                source.document for source in sources
            }

            missing_sources = sorted(
                expected_sources - retrieved_documents
            )

            source_coverage = (
                len(expected_sources & retrieved_documents)
                / len(expected_sources)
                if expected_sources
                else 1.0
            )

            # Evaluate whether expected phrases appear in the answer.
            fact_metrics = calculate_fact_coverage(
                answer,
                item.get("expected_facts", []),
            )

            result = {
                "question": question,
                "status": "COMPLETED",
                "answer": answer,
                "expected_sources": sorted(expected_sources),
                "retrieved_source_documents": sorted(
                    retrieved_documents
                ),
                "missing_expected_sources": missing_sources,
                "source_coverage": round(source_coverage, 4),
                "expected_fact_count": (
                    fact_metrics["expected_fact_count"]
                ),
                "matched_facts": fact_metrics["matched_facts"],
                "missing_facts": fact_metrics["missing_facts"],
                "fact_coverage": fact_metrics["fact_coverage"],
                "expected_facts_for_manual_review": item.get(
                    "expected_facts", []
                ),
                "manual_answer_correctness": None,
                "manual_citation_support": None,
            }

            results.append(result)

            print(f"Answer: {answer}")
            print(
                "Retrieved source documents: "
                f"{sorted(retrieved_documents)}"
            )
            print(f"Missing expected sources: {missing_sources}")
            print(f"Source coverage: {source_coverage:.2%}")
            print(
                "Expected-fact coverage: "
                f"{fact_metrics['fact_coverage']:.2%}"
            )
            print(f"Missing expected facts: {fact_metrics['missing_facts']}")

        except Exception as exc:
            results.append(
                {
                    "question": question,
                    "status": "ERROR",
                    "error": str(exc),
                }
            )
            print(f"Evaluation error: {exc}")

    completed = [
        result
        for result in results
        if result["status"] == "COMPLETED"
    ]

    mean_source_coverage = (
        sum(result["source_coverage"] for result in completed)
        / len(completed)
        if completed
        else None
    )

    mean_fact_coverage = (
        sum(result["fact_coverage"] for result in completed)
        / len(completed)
        if completed
        else None
    )

    report = {
        "queries_total": len(dataset),
        "queries_completed": len(completed),
        "queries_skipped_or_failed": len(dataset) - len(completed),
        "top_k": TOP_K,
        "mean_source_coverage": (
            round(mean_source_coverage, 4)
            if mean_source_coverage is not None
            else None
        ),
        "mean_expected_fact_coverage": (
            round(mean_fact_coverage, 4)
            if mean_fact_coverage is not None
            else None
        ),
        "results": results,
        "limitations": [
            (
                "Source coverage measures whether expected source "
                "filenames appear in retrieved evidence. It does not "
                "prove that citations support individual claims."
            ),
            (
                "Expected-fact coverage uses exact, case-insensitive "
                "phrase matching. It can miss correct paraphrases and "
                "cannot independently verify factual correctness."
            ),
            (
                "The dataset is small. Results should not be treated "
                "as a reliable general accuracy benchmark."
            ),
        ],
    }

    with RESULTS_PATH.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=2, ensure_ascii=False)

    print("\n" + "=" * 60)
    print("EVALUATION SUMMARY")
    print(f"Total questions: {len(dataset)}")
    print(f"Completed: {len(completed)}")
    print(
        f"Skipped or failed: {len(dataset) - len(completed)}"
    )

    if mean_source_coverage is not None:
        print(f"Mean source coverage: {mean_source_coverage:.2%}")
    else:
        print("Mean source coverage: N/A")

    if mean_fact_coverage is not None:
        print(f"Mean expected-fact coverage: {mean_fact_coverage:.2%}")
    else:
        print("Mean expected-fact coverage: N/A")

    print(f"Report saved to: {RESULTS_PATH}")


if __name__ == "__main__":
    main()
