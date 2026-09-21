from app.rag.citation_validator import validate_citations


def main():
    examples = [
        "Revenue declined because of lower orders [1] and higher costs [3].",
        "Revenue declined because of lower orders [1] and higher costs [7].",
        "The evidence does not contain enough information.",
    ]

    for answer in examples:
        result = validate_citations(
            answer=answer,
            evidence_count=3,
        )

        print("\n" + "=" * 60)
        print(f"Answer: {answer}")
        print(f"Validation: {result}")


if __name__ == "__main__":
    main()
