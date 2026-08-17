"""Post-processing: clean up engine output and attach provenance metadata.

Conversion engines produce serviceable but noisy markdown. This module
normalises it and prepends YAML frontmatter recording where the document
came from.

The frontmatter is the part that matters for RAG. When an agent retrieves a
passage, the answer "where did this come from?" has to be answerable, and it
is only answerable if provenance was attached at ingestion time. Adding it
later is impossible.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

_TRAILING_WS = re.compile(r"[ \t]+$", re.MULTILINE)
_EXCESS_BLANKS = re.compile(r"\n{3,}")
_NULL_BYTES = re.compile(r"\x00")
# Runs of dot-leaders from a table of contents, e.g. "Chapter 1 ......... 7"
_DOT_LEADERS = re.compile(r"\.{4,}\s*\d*\s*$", re.MULTILINE)


@dataclass(frozen=True)
class Document:
    """A converted document, ready to write or upload."""

    source: Path
    slug: str
    body: str
    engine: str
    sha256: str

    def render(self) -> str:
        """Full markdown text including frontmatter."""
        return frontmatter(self) + "\n" + self.body.strip() + "\n"


def normalise(text: str) -> str:
    """Tidy raw engine output without changing its meaning.

    Only reversible, meaning-preserving cleanups belong here. Anything that
    drops content belongs in the engine, where it can be reasoned about.
    """
    text = _NULL_BYTES.sub("", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = _TRAILING_WS.sub("", text)
    text = _DOT_LEADERS.sub("", text)
    text = _EXCESS_BLANKS.sub("\n\n", text)
    return text.strip()


def frontmatter(doc: Document) -> str:
    """YAML frontmatter carrying provenance for the converted document."""
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    fields = {
        "title": doc.source.stem,
        "source_file": doc.source.name,
        "source_path": str(doc.source),
        "source_type": doc.source.suffix.lstrip(".").lower(),
        "converted_by": doc.engine,
        "converted_at": generated,
        "sha256": doc.sha256,
    }
    lines = ["---"]
    lines += [f"{key}: {_yaml_scalar(value)}" for key, value in fields.items()]
    lines.append("---")
    return "\n".join(lines) + "\n"


def _yaml_scalar(value: str) -> str:
    """Quote a YAML scalar only when it would otherwise be ambiguous."""
    needs_quoting = (
        value == ""
        or value[0] in "&*?|-<>=!%@`{[\"'"
        or ": " in value
        or value.strip() != value
        or value.lower() in {"true", "false", "null", "yes", "no", "on", "off"}
    )
    if needs_quoting:
        return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return value


def word_count(text: str) -> int:
    """Rough word count, used to flag suspiciously thin conversions."""
    return len(text.split())


def looks_empty(text: str, *, minimum_words: int = 20) -> bool:
    """Whether a conversion produced too little text to be useful.

    A scanned PDF with no OCR layer converts "successfully" to a handful of
    page numbers. Without this check it enters the knowledge base as a
    document that exists but says nothing, which is worse than a visible
    failure because retrieval will still match it.
    """
    return word_count(text) < minimum_words
