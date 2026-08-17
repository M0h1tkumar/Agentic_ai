"""Decide what to do with a file before spending money or CPU on it.

Triage is deliberately pure and dependency-free: it looks at the path, the
extension, and the size, and returns a decision. Everything expensive
(parsing, OCR, network) happens later, only for files that survive this.
"""

from __future__ import annotations

import hashlib
import re
import unicodedata
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from .config import PASSTHROUGH_EXTENSIONS, SUPPORTED_EXTENSIONS


class Action(str, Enum):
    """What the pipeline should do with a candidate file."""

    CONVERT = "convert"        # run a conversion engine
    PASSTHROUGH = "passthrough"  # already text/markdown, copy with frontmatter
    SKIP = "skip"              # not a document we handle
    TOO_LARGE = "too_large"    # over the configured byte limit


@dataclass(frozen=True)
class Verdict:
    """The outcome of triaging one path."""

    path: Path
    action: Action
    reason: str = ""

    @property
    def accepted(self) -> bool:
        return self.action in (Action.CONVERT, Action.PASSTHROUGH)


def triage(path: Path, *, max_bytes: int, skip_extensions: frozenset[str] = frozenset()) -> Verdict:
    """Classify a single path.

    Hidden files and anything under a dot-directory are skipped: those are
    almost always editor state, VCS internals, or sync artifacts, and
    ingesting them pollutes a knowledge base with noise.
    """
    suffix = path.suffix.lower()

    if any(part.startswith(".") for part in path.parts):
        return Verdict(path, Action.SKIP, "hidden file or dot-directory")

    if suffix in skip_extensions:
        return Verdict(path, Action.SKIP, f"{suffix} excluded by configuration")

    if suffix not in SUPPORTED_EXTENSIONS:
        return Verdict(path, Action.SKIP, f"unsupported extension {suffix or '(none)'}")

    try:
        size = path.stat().st_size
    except OSError as exc:
        return Verdict(path, Action.SKIP, f"unreadable: {exc}")

    if size == 0:
        return Verdict(path, Action.SKIP, "empty file")

    if size > max_bytes:
        return Verdict(path, Action.TOO_LARGE, f"{size} bytes exceeds limit {max_bytes}")

    if suffix in PASSTHROUGH_EXTENSIONS:
        return Verdict(path, Action.PASSTHROUGH, "already plain text")

    return Verdict(path, Action.CONVERT, "needs conversion")


def discover(root: Path, *, recursive: bool = True) -> list[Path]:
    """List candidate files under `root`, sorted for deterministic runs.

    Sorting matters more than it looks: a stable order makes a failed run
    resumable and makes two runs comparable.
    """
    if root.is_file():
        return [root]
    pattern = "**/*" if recursive else "*"
    return sorted(p for p in root.glob(pattern) if p.is_file())


def slugify(name: str) -> str:
    """Turn an arbitrary filename into a safe, stable output stem.

    Unicode is normalised to ASCII where possible so that the same document
    produces the same slug regardless of how its name was encoded.
    """
    decomposed = unicodedata.normalize("NFKD", name)
    ascii_only = decomposed.encode("ascii", "ignore").decode("ascii")
    lowered = ascii_only.lower()
    cleaned = re.sub(r"[^a-z0-9]+", "-", lowered).strip("-")
    return cleaned or "document"


def content_hash(path: Path, *, chunk_size: int = 1 << 20) -> str:
    """SHA-256 of the file contents, streamed so large files stay cheap.

    Used to skip re-converting a document whose bytes have not changed,
    which is what makes `--watch` and repeated runs affordable.
    """
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(chunk_size), b""):
            digest.update(block)
    return digest.hexdigest()
