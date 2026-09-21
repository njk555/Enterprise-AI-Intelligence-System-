def extract_citations(answer: str) -> list[int]:
    """
    Extract numeric citations in ASCII [1] and Unicode ?1? forms.
    """

    citations = []

    ASCII_OPEN = chr(91)
    ASCII_CLOSE = chr(93)

    UNICODE_OPEN = chr(0x3010)
    UNICODE_CLOSE = chr(0x3011)

    i = 0

    while i < len(answer):
        if answer[i] == ASCII_OPEN:
            end = answer.find(ASCII_CLOSE, i + 1)

            if end != -1:
                value = answer[i + 1:end]

                if value.isdigit():
                    citations.append(int(value))
                    i = end + 1
                    continue

        elif answer[i] == UNICODE_OPEN:
            end = answer.find(UNICODE_CLOSE, i + 1)

            if end != -1:
                value = answer[i + 1:end]

                if value.isdigit():
                    citations.append(int(value))
                    i = end + 1
                    continue

        i += 1

    return citations


def validate_citations(
    answer: str,
    evidence_count: int,
    require_citation: bool = True,
) -> dict:
    """
    Validate citations against the number of evidence items.
    """

    citations = extract_citations(answer)

    valid = [
        citation
        for citation in citations
        if 1 <= citation <= evidence_count
    ]

    invalid = [
        citation
        for citation in citations
        if citation < 1 or citation > evidence_count
    ]

    has_citations = len(citations) > 0

    return {
        "citations": citations,
        "valid_citations": valid,
        "invalid_citations": invalid,
        "has_citations": has_citations,
        "all_valid": len(invalid) == 0,
        "citation_required": require_citation,
        "citation_complete": (
            has_citations
            if require_citation
            else True
        ),
        "valid": (
            (has_citations and len(invalid) == 0)
            if require_citation
            else len(invalid) == 0
        ),
    }


if __name__ == "__main__":
    tests = [
        "This is supported [1] and [2].",
        "This is supported "
        + chr(0x3010) + "1"
        + chr(0x3011)
        + chr(0x3010) + "2"
        + chr(0x3011)
        + ".",
        "This has an invalid citation [7].",
        "This has no citation.",
    ]

    for test in tests:
        print(test)
        print(" ->", validate_citations(test, 3))
        print()
