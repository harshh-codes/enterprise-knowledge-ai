
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = Path(__file__).parent / "answer_quality_dataset.json"
RESULTS_PATH = Path(__file__).parent / "answer_quality_results.json"


def main() -> None:
    with DATASET_PATH.open("r", encoding="utf-8") as file:
        dataset = json.load(file)

    results = []

    print("Answer Quality Evaluation")
    print("=" * 60)
    print("Score each answer against the reference points.")
    print("Correctness: 1 = supported and complete, 0 = otherwise.")
    print("Citation support: 1 = all required sources cited correctly,")
    print("                 0 = missing or incorrect citations.")
    print()

    for index, item in enumerate(dataset, start=1):
        print(f"\nTest {index}: {item['question']}")
        print("\nExpected answer points:")

        for point in item["expected_answer_points"]:
            print(f"  - {point}")

        print("\nExpected sources:")
        for source in item["expected_sources"]:
            print(f"  - {source}")

        while True:
            correctness = input(
                "\nIs the answer correct and complete? (1/0): "
            ).strip()
            if correctness in {"0", "1"}:
                break
            print("Enter 1 or 0.")

        while True:
            citation_support = input(
                "Are all required citations present and supported? (1/0): "
            ).strip()
            if citation_support in {"0", "1"}:
                break
            print("Enter 1 or 0.")

        results.append(
            {
                "question": item["question"],
                "correctness": int(correctness),
                "citation_support": int(citation_support),
                "expected_sources": item["expected_sources"],
            }
        )

    count = len(results)

    if count == 0:
        print("No evaluation questions found.")
        return

    correctness_rate = (
        sum(result["correctness"] for result in results) / count
    )
    citation_support_rate = (
        sum(result["citation_support"] for result in results) / count
    )

    report = {
        "queries_evaluated": count,
        "answer_correctness_rate": round(correctness_rate, 4),
        "citation_support_rate": round(citation_support_rate, 4),
        "results": results,
        "note": (
            "Scores are manually judged and reflect only this test dataset. "
            "They are not an independently validated benchmark."
        ),
    }

    with RESULTS_PATH.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=2, ensure_ascii=False)

    print("\n" + "=" * 60)
    print("SUMMARY")
    print(f"Questions evaluated: {count}")
    print(f"Answer correctness rate: {correctness_rate:.2%}")
    print(f"Citation support rate: {citation_support_rate:.2%}")
    print(f"Results saved to: {RESULTS_PATH}")


if __name__ == "__main__":
    main()
