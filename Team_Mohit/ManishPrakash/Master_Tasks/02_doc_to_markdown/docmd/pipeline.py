"""Orchestration: discover, triage, convert, write, upload, embed.

The pipeline is deliberately resumable. Every converted file is written to
disk with a content hash in its frontmatter, and a manifest records what has
been processed. Re-running skips unchanged inputs, so an interrupted run of
a thousand documents costs only the remainder.
"""

from __future__ import annotations

import json
from collections.abc import Iterator
from dataclasses import asdict, dataclass, field
from pathlib import Path

from .anythingllm import AnythingLLMClient, AnythingLLMError
from .config import Config
from .converters import ConversionError, Converter, select_engine
from .markdown import Document, looks_empty, normalise
from .triage import Action, content_hash, discover, slugify, triage

MANIFEST_NAME = ".docmd-manifest.json"


@dataclass
class FileResult:
    """What happened to one input file."""

    source: str
    status: str           # converted | skipped | unchanged | failed | empty
    detail: str = ""
    output: str = ""
    engine: str = ""
    words: int = 0


@dataclass
class RunReport:
    """Aggregate outcome of a pipeline run."""

    results: list[FileResult] = field(default_factory=list)
    uploaded: int = 0
    embedded: int = 0

    def count(self, status: str) -> int:
        return sum(1 for r in self.results if r.status == status)

    @property
    def failures(self) -> list[FileResult]:
        return [r for r in self.results if r.status == "failed"]

    def summary(self) -> str:
        parts = [
            f"converted={self.count('converted')}",
            f"unchanged={self.count('unchanged')}",
            f"skipped={self.count('skipped')}",
            f"empty={self.count('empty')}",
            f"failed={self.count('failed')}",
        ]
        if self.uploaded:
            parts.append(f"uploaded={self.uploaded}")
        if self.embedded:
            parts.append(f"embedded={self.embedded}")
        return "  ".join(parts)


class Manifest:
    """Records source path -> content hash, so unchanged files are skipped."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self._entries: dict[str, str] = {}
        if path.exists():
            try:
                self._entries = json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                # A corrupt manifest is not worth failing over. Losing it
                # costs one redundant conversion pass, nothing more.
                self._entries = {}

    def unchanged(self, source: Path, digest: str) -> bool:
        return self._entries.get(str(source)) == digest

    def record(self, source: Path, digest: str) -> None:
        self._entries[str(source)] = digest

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(self._entries, indent=2, sort_keys=True), encoding="utf-8"
        )


def convert_file(path: Path, engine: Converter) -> Document:
    """Convert one file to a Document. Raises ConversionError on failure."""
    raw = engine.convert(path)
    body = normalise(raw)
    return Document(
        source=path,
        slug=slugify(path.stem),
        body=body,
        engine=engine.name,
        sha256=content_hash(path),
    )


def run(config: Config, *, upload: bool = False, dry_run: bool = False) -> RunReport:
    """Execute a full pipeline run and return a report.

    `dry_run` performs discovery and triage but no conversion, which is the
    fast way to check what a directory would produce before committing CPU
    to it.
    """
    report = RunReport()
    engine = select_engine(config.engine)
    manifest = Manifest(config.output_dir / MANIFEST_NAME)
    pending_uploads: list[tuple[str, str, str]] = []

    for verdict in _triaged(config):
        source = verdict.path

        if not verdict.accepted:
            report.results.append(
                FileResult(str(source), "skipped", verdict.reason)
            )
            continue

        if dry_run:
            report.results.append(
                FileResult(str(source), "converted", "dry run", engine=engine.name)
            )
            continue

        digest = content_hash(source)
        target = config.output_dir / f"{slugify(source.stem)}.md"

        if not config.overwrite and target.exists() and manifest.unchanged(source, digest):
            report.results.append(FileResult(str(source), "unchanged", output=str(target)))
            continue

        try:
            if verdict.action is Action.PASSTHROUGH:
                body = normalise(source.read_text(encoding="utf-8", errors="replace"))
                doc = Document(source, slugify(source.stem), body, "passthrough", digest)
            else:
                doc = convert_file(source, engine)
        except (ConversionError, OSError) as exc:
            report.results.append(FileResult(str(source), "failed", str(exc)))
            continue

        if looks_empty(doc.body):
            # Most often a scanned PDF with no OCR layer. Report it rather
            # than letting a contentless document into the knowledge base.
            report.results.append(
                FileResult(
                    str(source),
                    "empty",
                    "conversion produced almost no text (scanned document without OCR?)",
                    engine=doc.engine,
                )
            )
            continue

        rendered = doc.render()
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(rendered, encoding="utf-8")
        manifest.record(source, digest)

        report.results.append(
            FileResult(
                source=str(source),
                status="converted",
                output=str(target),
                engine=doc.engine,
                words=len(doc.body.split()),
            )
        )
        pending_uploads.append((doc.source.stem, rendered, str(source)))

    if not dry_run:
        manifest.save()

    if upload and pending_uploads and not dry_run:
        _upload_all(config, pending_uploads, report)

    return report


def _triaged(config: Config) -> Iterator:
    for path in discover(config.input_dir, recursive=config.recursive):
        yield triage(
            path,
            max_bytes=config.max_bytes,
            skip_extensions=config.skip_extensions,
        )


def _upload_all(
    config: Config,
    documents: list[tuple[str, str, str]],
    report: RunReport,
) -> None:
    """Upload converted documents and embed them into the workspace."""
    config.require_upload()
    client = AnythingLLMClient(config.base_url, config.api_key)

    if not client.workspace_exists(config.workspace):
        raise AnythingLLMError(
            f"workspace {config.workspace!r} not found; create it in AnythingLLM first"
        )

    locations: list[str] = []
    for title, body, source in documents:
        try:
            result = client.upload_markdown(title, body, source=source)
        except AnythingLLMError as exc:
            for entry in report.results:
                if entry.source == source:
                    entry.status = "failed"
                    entry.detail = f"upload failed: {exc}"
            continue
        locations.append(result.location)
        report.uploaded += 1

    client.embed(config.workspace, locations)
    report.embedded = len(locations)


def report_as_json(report: RunReport) -> str:
    """Serialise a run report for scripting or CI."""
    return json.dumps(
        {
            "summary": {
                "converted": report.count("converted"),
                "unchanged": report.count("unchanged"),
                "skipped": report.count("skipped"),
                "empty": report.count("empty"),
                "failed": report.count("failed"),
                "uploaded": report.uploaded,
                "embedded": report.embedded,
            },
            "files": [asdict(r) for r in report.results],
        },
        indent=2,
    )
