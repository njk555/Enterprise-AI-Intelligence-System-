import re


def split_into_sections(text: str) -> list[dict]:
    """
    Split a business document into logical sections.
    """

    lines = text.splitlines()

    sections = []
    current_heading = None
    current_lines = []

    known_headings = {
        "Executive Summary",
        "Revenue Performance",
        "Customer Trends",
        "Support Trends",
        "Infrastructure Costs",
        "Strategic Recommendations",
        "Conclusion",
        "Support Volume",
        "API and Integration Issues",
        "Dashboard Performance",
        "Data Synchronization",
        "Customer Impact",
        "Recommended Actions",
    }

    for line in lines:
        stripped = line.strip()

        if not stripped:
            continue

        is_heading = (
            len(stripped) <= 80
            and not stripped.endswith(".")
            and (
                stripped.isupper()
                or stripped in known_headings
            )
        )

        if is_heading:
            if current_heading is not None and current_lines:
                sections.append(
                    {
                        "heading": current_heading,
                        "content": "\n".join(current_lines).strip(),
                    }
                )

            current_heading = stripped
            current_lines = []

        else:
            current_lines.append(stripped)

    if current_heading is not None and current_lines:
        sections.append(
            {
                "heading": current_heading,
                "content": "\n".join(current_lines).strip(),
            }
        )

    return sections


def split_long_section(
    heading: str,
    content: str,
    chunk_size: int,
) -> list[dict]:
    """
    Split a single section only when it exceeds chunk_size.
    """

    paragraphs = [
        paragraph.strip()
        for paragraph in re.split(r"\n\s*\n", content)
        if paragraph.strip()
    ]

    chunks = []
    current = ""

    for paragraph in paragraphs:
        candidate = (
            f"{current}\n\n{paragraph}"
            if current
            else paragraph
        )

        if len(candidate) > chunk_size and current:
            chunks.append(
                {
                    "section": heading,
                    "content": f"{heading}\n\n{current}",
                }
            )

            current = paragraph

        else:
            current = candidate

    if current:
        chunks.append(
            {
                "section": heading,
                "content": f"{heading}\n\n{current}",
            }
        )

    return chunks


def chunk_text(
    text: str,
    chunk_size: int = 800,
) -> list[dict]:
    """
    Create one chunk per logical section.

    Long sections are split when necessary, while short
    sections remain independent retrieval units.
    """

    if not text.strip():
        return []

    if chunk_size <= 0:
        raise ValueError(
            "chunk_size must be greater than zero."
        )

    sections = split_into_sections(text)

    chunks = []

    for section in sections:
        section_chunks = split_long_section(
            heading=section["heading"],
            content=section["content"],
            chunk_size=chunk_size,
        )

        chunks.extend(section_chunks)

    return chunks
