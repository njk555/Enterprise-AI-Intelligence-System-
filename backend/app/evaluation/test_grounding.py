from app.evaluation.grounding import answer_supported_by_evidence


def main():
    evidence = [
        {
            "content": (
                "Revenue Performance\n\n"
                "Several large customers reduced their purchase volumes. "
                "Customer demand shifted toward smaller deployment sizes. "
                "Infrastructure costs increased significantly."
            )
        }
    ]

    supported_answer = (
        "Revenue declined because several large customers "
        "reduced their purchase volumes and infrastructure "
        "costs increased."
    )

    unsupported_answer = (
        "Revenue declined because the company lost its largest "
        "government contract and expanded into five new countries."
    )

    for answer in [
        supported_answer,
        unsupported_answer,
    ]:
        result = answer_supported_by_evidence(
            answer=answer,
            evidence=evidence,
        )

        print("\n" + "=" * 70)
        print(f"Answer: {answer}")
        print(f"Supported: {result['supported']}")
        print(f"Overlap: {result['overlap']:.2%}")


if __name__ == "__main__":
    main()
