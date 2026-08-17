"""Conversion engines: document bytes in, markdown text out.

Three engines, tried in order when `engine="auto"`:

  markitdown  Microsoft's converter. Fast, broad format coverage, good
              enough for most office documents.
  docling     IBM's converter. Slower, but far better at tables, reading
              order, and complex layout. Worth it for real PDFs.
  plaintext   Built-in fallback with no third-party dependency. Handles
              text-like formats only, so the tool degrades instead of
              failing when nothing is installed.

Engines are imported lazily. Installing this package pulls in nothing
heavy; you add markitdown or docling only if you need them.
"""

from __future__ import annotations

import csv
import html.parser
import io
import json
from abc import ABC, abstractmethod
from pathlib import Path


class ConversionError(RuntimeError):
    """Raised when an engine cannot produce markdown for a document."""


class Converter(ABC):
    """A document-to-markdown engine."""

    name: str = "abstract"

    @abstractmethod
    def available(self) -> bool:
        """Whether this engine can run in the current environment."""

    @abstractmethod
    def convert(self, path: Path) -> str:
        """Return markdown for `path`, or raise ConversionError."""


class MarkItDownConverter(Converter):
    name = "markitdown"

    def available(self) -> bool:
        try:
            import markitdown  # noqa: F401
        except ImportError:
            return False
        return True

    def convert(self, path: Path) -> str:
        try:
            from markitdown import MarkItDown
        except ImportError as exc:  # pragma: no cover - guarded by available()
            raise ConversionError("markitdown is not installed") from exc
        try:
            result = MarkItDown().convert(str(path))
        except Exception as exc:
            raise ConversionError(f"markitdown failed on {path.name}: {exc}") from exc
        text = getattr(result, "text_content", "") or ""
        if not text.strip():
            raise ConversionError(f"markitdown produced no text for {path.name}")
        return text


class DoclingConverter(Converter):
    name = "docling"

    def available(self) -> bool:
        try:
            import docling  # noqa: F401
        except ImportError:
            return False
        return True

    def convert(self, path: Path) -> str:
        try:
            from docling.document_converter import DocumentConverter
        except ImportError as exc:  # pragma: no cover - guarded by available()
            raise ConversionError("docling is not installed") from exc
        try:
            result = DocumentConverter().convert(str(path))
            text = result.document.export_to_markdown()
        except Exception as exc:
            raise ConversionError(f"docling failed on {path.name}: {exc}") from exc
        if not text.strip():
            raise ConversionError(f"docling produced no text for {path.name}")
        return text


class PlainTextConverter(Converter):
    """Dependency-free fallback for text-shaped formats.

    Deliberately narrow. It will not pretend to parse a PDF; it raises
    instead, so a missing dependency produces an honest error rather than
    an empty document silently entering the knowledge base.
    """

    name = "plaintext"
    HANDLED = frozenset({".txt", ".md", ".rst", ".csv", ".json", ".html", ".htm", ".xml"})

    def available(self) -> bool:
        return True

    def convert(self, path: Path) -> str:
        suffix = path.suffix.lower()
        if suffix not in self.HANDLED:
            raise ConversionError(
                f"no engine available for {suffix}; install markitdown or docling"
            )
        raw = path.read_text(encoding="utf-8", errors="replace")

        if suffix == ".csv":
            return _csv_to_markdown(raw)
        if suffix == ".json":
            return _json_to_markdown(raw)
        if suffix in {".html", ".htm"}:
            return _html_to_text(raw)
        return raw


def _csv_to_markdown(raw: str) -> str:
    """Render CSV as a markdown table.

    Tables survive retrieval far better as markdown than as raw comma-
    separated text, because the header travels with every row visually.
    """
    rows = list(csv.reader(io.StringIO(raw)))
    if not rows:
        return ""
    width = max(len(r) for r in rows)
    padded = [r + [""] * (width - len(r)) for r in rows]
    header, *body = padded
    lines = [
        "| " + " | ".join(_escape_cell(c) for c in header) + " |",
        "| " + " | ".join("---" for _ in header) + " |",
    ]
    lines += ["| " + " | ".join(_escape_cell(c) for c in row) + " |" for row in body]
    return "\n".join(lines)


def _escape_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def _json_to_markdown(raw: str) -> str:
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ConversionError(f"invalid JSON: {exc}") from exc
    return "```json\n" + json.dumps(parsed, indent=2, ensure_ascii=False) + "\n```"


class _TextExtractor(html.parser.HTMLParser):
    """Strip tags, keeping headings and paragraph breaks meaningful."""

    SKIP = frozenset({"script", "style", "head", "meta", "link"})
    BLOCK = frozenset({"p", "div", "br", "li", "tr", "section", "article"})

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self._suppress = 0

    def handle_starttag(self, tag: str, attrs: object) -> None:
        if tag in self.SKIP:
            self._suppress += 1
        elif tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.parts.append("\n\n" + "#" * int(tag[1]) + " ")
        elif tag in self.BLOCK:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in self.SKIP and self._suppress:
            self._suppress -= 1
        elif tag in self.BLOCK or tag.startswith("h"):
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self._suppress and data.strip():
            self.parts.append(data.strip() + " ")

    def text(self) -> str:
        joined = "".join(self.parts)
        while "\n\n\n" in joined:
            joined = joined.replace("\n\n\n", "\n\n")
        return joined.strip()


def _html_to_text(raw: str) -> str:
    parser = _TextExtractor()
    parser.feed(raw)
    return parser.text()


ENGINES: tuple[type[Converter], ...] = (
    MarkItDownConverter,
    DoclingConverter,
    PlainTextConverter,
)


def select_engine(name: str = "auto") -> Converter:
    """Return an engine by name, or the best available one for "auto".

    Raises ConversionError for an unknown name so a typo in configuration
    fails loudly instead of silently falling back.
    """
    if name != "auto":
        for cls in ENGINES:
            if cls.name == name:
                engine = cls()
                if not engine.available():
                    raise ConversionError(
                        f"engine '{name}' is selected but not installed"
                    )
                return engine
        raise ConversionError(f"unknown engine '{name}'")

    for cls in ENGINES:
        engine = cls()
        if engine.available():
            return engine
    raise ConversionError("no conversion engine available")  # pragma: no cover
