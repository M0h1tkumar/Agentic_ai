"""Tests for docmd.

These cover the pure logic - triage, slugging, normalisation, frontmatter,
the CSV/HTML/JSON fallback converters, and the pipeline end to end using the
built-in engine. Network calls to AnythingLLM are exercised against a stub
transport rather than a live server.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from docmd import cli  # noqa: E402
from docmd.anythingllm import AnythingLLMClient, _extract_location  # noqa: E402
from docmd.config import Config, ConfigError  # noqa: E402
from docmd.converters import (  # noqa: E402
    ConversionError,
    PlainTextConverter,
    select_engine,
)
from docmd.markdown import Document, frontmatter, looks_empty, normalise  # noqa: E402
from docmd.pipeline import Manifest, run  # noqa: E402
from docmd.triage import Action, content_hash, discover, slugify, triage  # noqa: E402


# --------------------------------------------------------------------------
# triage
# --------------------------------------------------------------------------

def test_triage_accepts_pdf(tmp_path: Path) -> None:
    target = tmp_path / "report.pdf"
    target.write_bytes(b"%PDF-1.4 fake")
    verdict = triage(target, max_bytes=1000)
    assert verdict.action is Action.CONVERT
    assert verdict.accepted


def test_triage_passthrough_for_markdown(tmp_path: Path) -> None:
    target = tmp_path / "notes.md"
    target.write_text("# hello")
    assert triage(target, max_bytes=1000).action is Action.PASSTHROUGH


def test_triage_rejects_unsupported_extension(tmp_path: Path) -> None:
    target = tmp_path / "binary.exe"
    target.write_bytes(b"MZ")
    verdict = triage(target, max_bytes=1000)
    assert verdict.action is Action.SKIP
    assert "unsupported" in verdict.reason


def test_triage_rejects_empty_file(tmp_path: Path) -> None:
    target = tmp_path / "empty.txt"
    target.touch()
    assert triage(target, max_bytes=1000).reason == "empty file"


def test_triage_enforces_size_limit(tmp_path: Path) -> None:
    target = tmp_path / "big.pdf"
    target.write_bytes(b"x" * 500)
    verdict = triage(target, max_bytes=100)
    assert verdict.action is Action.TOO_LARGE
    assert not verdict.accepted


def test_triage_skips_hidden_paths(tmp_path: Path) -> None:
    hidden = tmp_path / ".git" / "config.txt"
    hidden.parent.mkdir()
    hidden.write_text("data")
    assert triage(hidden, max_bytes=1000).action is Action.SKIP


def test_triage_honours_skip_extensions(tmp_path: Path) -> None:
    target = tmp_path / "sheet.csv"
    target.write_text("a,b")
    verdict = triage(target, max_bytes=1000, skip_extensions=frozenset({".csv"}))
    assert verdict.action is Action.SKIP


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("Annual Report 2026", "annual-report-2026"),
        ("  spaces  everywhere  ", "spaces-everywhere"),
        ("Ünïcödé Näme", "unicode-name"),
        ("!!!", "document"),
        ("multi___under__scores", "multi-under-scores"),
    ],
)
def test_slugify(raw: str, expected: str) -> None:
    assert slugify(raw) == expected


def test_discover_is_sorted_and_recursive(tmp_path: Path) -> None:
    (tmp_path / "sub").mkdir()
    (tmp_path / "b.txt").write_text("b")
    (tmp_path / "a.txt").write_text("a")
    (tmp_path / "sub" / "c.txt").write_text("c")

    names = [p.name for p in discover(tmp_path)]
    assert names == ["a.txt", "b.txt", "c.txt"]

    shallow = [p.name for p in discover(tmp_path, recursive=False)]
    assert shallow == ["a.txt", "b.txt"]


def test_content_hash_is_stable_and_sensitive(tmp_path: Path) -> None:
    target = tmp_path / "f.txt"
    target.write_text("hello")
    first = content_hash(target)
    assert first == content_hash(target)
    target.write_text("hello!")
    assert content_hash(target) != first


# --------------------------------------------------------------------------
# markdown post-processing
# --------------------------------------------------------------------------

def test_normalise_collapses_blank_lines_and_strips_trailing_space() -> None:
    assert normalise("a   \n\n\n\n\nb") == "a\n\nb"


def test_normalise_handles_crlf_and_null_bytes() -> None:
    assert normalise("a\r\nb\x00c") == "a\nbc"


def test_normalise_strips_toc_dot_leaders() -> None:
    assert normalise("Chapter One ........... 7") == "Chapter One"


def test_frontmatter_contains_provenance(tmp_path: Path) -> None:
    doc = Document(
        source=tmp_path / "Quarterly Report.pdf",
        slug="quarterly-report",
        body="content",
        engine="markitdown",
        sha256="abc123",
    )
    header = frontmatter(doc)
    assert header.startswith("---\n")
    assert "source_file: Quarterly Report.pdf" in header
    assert "source_type: pdf" in header
    assert "converted_by: markitdown" in header
    assert "sha256: abc123" in header


def test_frontmatter_quotes_ambiguous_titles(tmp_path: Path) -> None:
    doc = Document(tmp_path / "true.md", "true", "b", "e", "h")
    assert 'title: "true"' in frontmatter(doc)


def test_render_produces_frontmatter_then_body(tmp_path: Path) -> None:
    doc = Document(tmp_path / "x.md", "x", "# Title\n\ntext", "e", "h")
    rendered = doc.render()
    assert rendered.count("---") >= 2
    assert rendered.rstrip().endswith("text")


def test_looks_empty_flags_thin_conversions() -> None:
    assert looks_empty("page 1 page 2")
    assert not looks_empty(" ".join(["word"] * 50))


# --------------------------------------------------------------------------
# converters
# --------------------------------------------------------------------------

def test_plaintext_converter_csv_to_table(tmp_path: Path) -> None:
    target = tmp_path / "data.csv"
    target.write_text("name,role\nManish,engineer\n")
    out = PlainTextConverter().convert(target)
    assert "| name | role |" in out
    assert "| --- | --- |" in out
    assert "| Manish | engineer |" in out


def test_plaintext_converter_csv_escapes_pipes(tmp_path: Path) -> None:
    target = tmp_path / "data.csv"
    target.write_text('a,b\n"x|y",z\n')
    assert r"x\|y" in PlainTextConverter().convert(target)


def test_plaintext_converter_json_is_fenced(tmp_path: Path) -> None:
    target = tmp_path / "d.json"
    target.write_text('{"b":1,"a":2}')
    out = PlainTextConverter().convert(target)
    assert out.startswith("```json")
    assert out.endswith("```")


def test_plaintext_converter_rejects_invalid_json(tmp_path: Path) -> None:
    target = tmp_path / "d.json"
    target.write_text("{nope}")
    with pytest.raises(ConversionError):
        PlainTextConverter().convert(target)


def test_plaintext_converter_html_strips_tags_and_scripts(tmp_path: Path) -> None:
    target = tmp_path / "page.html"
    target.write_text(
        "<html><head><style>p{color:red}</style></head>"
        "<body><h2>Heading</h2><p>Body text</p>"
        "<script>alert(1)</script></body></html>"
    )
    out = PlainTextConverter().convert(target)
    assert "## Heading" in out
    assert "Body text" in out
    assert "alert" not in out
    assert "color:red" not in out


def test_plaintext_converter_refuses_pdf(tmp_path: Path) -> None:
    target = tmp_path / "scan.pdf"
    target.write_bytes(b"%PDF")
    with pytest.raises(ConversionError, match="no engine available"):
        PlainTextConverter().convert(target)


def test_select_engine_rejects_unknown_name() -> None:
    with pytest.raises(ConversionError, match="unknown engine"):
        select_engine("nope")


def test_select_engine_auto_always_resolves() -> None:
    assert select_engine("auto").available()


# --------------------------------------------------------------------------
# config
# --------------------------------------------------------------------------

def test_config_require_upload_lists_all_missing_fields() -> None:
    with pytest.raises(ConfigError) as excinfo:
        Config().require_upload()
    message = str(excinfo.value)
    assert "ANYTHINGLLM_BASE_URL" in message
    assert "ANYTHINGLLM_API_KEY" in message
    assert "ANYTHINGLLM_WORKSPACE" in message


def test_config_require_upload_passes_when_complete() -> None:
    Config(base_url="http://x", api_key="k", workspace="w").require_upload()


def test_config_from_env_reads_and_overrides(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DOCMD_ENGINE", "plaintext")
    monkeypatch.setenv("ANYTHINGLLM_BASE_URL", "http://host:3001/")
    monkeypatch.setenv("DOCMD_RECURSIVE", "false")

    config = Config.from_env()
    assert config.engine == "plaintext"
    assert config.base_url == "http://host:3001"
    assert config.recursive is False

    assert Config.from_env(engine="docling").engine == "docling"
    # None overrides are ignored, so unset CLI flags do not clobber env.
    assert Config.from_env(engine=None).engine == "plaintext"


# --------------------------------------------------------------------------
# pipeline
# --------------------------------------------------------------------------

@pytest.fixture()
def workspace(tmp_path: Path) -> tuple[Path, Path]:
    source = tmp_path / "in"
    dest = tmp_path / "out"
    source.mkdir()
    return source, dest


def test_run_converts_and_writes_markdown(workspace: tuple[Path, Path]) -> None:
    source, dest = workspace
    (source / "Notes File.txt").write_text(" ".join(["content"] * 40))

    report = run(Config(input_dir=source, output_dir=dest, engine="plaintext"))

    assert report.count("converted") == 1
    written = dest / "notes-file.md"
    assert written.exists()
    assert "source_file: Notes File.txt" in written.read_text()


def test_run_skips_unsupported_files(workspace: tuple[Path, Path]) -> None:
    source, dest = workspace
    (source / "app.exe").write_bytes(b"MZ")
    report = run(Config(input_dir=source, output_dir=dest, engine="plaintext"))
    assert report.count("skipped") == 1
    assert report.count("converted") == 0


def test_run_flags_thin_conversions_as_empty(workspace: tuple[Path, Path]) -> None:
    source, dest = workspace
    (source / "scan.txt").write_text("1 2 3")
    report = run(Config(input_dir=source, output_dir=dest, engine="plaintext"))
    assert report.count("empty") == 1
    assert not (dest / "scan.md").exists()


def test_run_is_incremental_on_second_pass(workspace: tuple[Path, Path]) -> None:
    source, dest = workspace
    (source / "doc.txt").write_text(" ".join(["word"] * 40))
    config = Config(input_dir=source, output_dir=dest, engine="plaintext")

    assert run(config).count("converted") == 1
    assert run(config).count("unchanged") == 1


def test_run_reconverts_when_content_changes(workspace: tuple[Path, Path]) -> None:
    source, dest = workspace
    target = source / "doc.txt"
    target.write_text(" ".join(["word"] * 40))
    config = Config(input_dir=source, output_dir=dest, engine="plaintext")

    run(config)
    target.write_text(" ".join(["changed"] * 40))
    assert run(config).count("converted") == 1


def test_run_overwrite_forces_reconversion(workspace: tuple[Path, Path]) -> None:
    source, dest = workspace
    (source / "doc.txt").write_text(" ".join(["word"] * 40))
    config = Config(input_dir=source, output_dir=dest, engine="plaintext")
    run(config)
    forced = run(config.replace(overwrite=True))
    assert forced.count("converted") == 1


def test_run_dry_run_writes_nothing(workspace: tuple[Path, Path]) -> None:
    source, dest = workspace
    (source / "doc.txt").write_text(" ".join(["word"] * 40))
    report = run(
        Config(input_dir=source, output_dir=dest, engine="plaintext"), dry_run=True
    )
    assert report.count("converted") == 1
    assert not dest.exists() or not list(dest.glob("*.md"))


def test_run_records_failures_without_aborting(workspace: tuple[Path, Path]) -> None:
    source, dest = workspace
    (source / "good.txt").write_text(" ".join(["word"] * 40))
    (source / "bad.json").write_text("{invalid")

    report = run(Config(input_dir=source, output_dir=dest, engine="plaintext"))
    assert report.count("converted") == 1
    assert report.count("failed") == 1
    assert report.failures[0].source.endswith("bad.json")


def test_report_as_json_is_parseable(workspace: tuple[Path, Path]) -> None:
    from docmd.pipeline import report_as_json

    source, dest = workspace
    (source / "doc.txt").write_text(" ".join(["word"] * 40))
    payload = json.loads(report_as_json(run(Config(input_dir=source, output_dir=dest, engine="plaintext"))))
    assert payload["summary"]["converted"] == 1
    assert len(payload["files"]) == 1


def test_manifest_survives_corruption(tmp_path: Path) -> None:
    path = tmp_path / "manifest.json"
    path.write_text("{not json")
    manifest = Manifest(path)
    assert not manifest.unchanged(Path("a"), "hash")
    manifest.record(Path("a"), "hash")
    manifest.save()
    assert Manifest(path).unchanged(Path("a"), "hash")


# --------------------------------------------------------------------------
# AnythingLLM client
# --------------------------------------------------------------------------

@pytest.mark.parametrize(
    ("payload", "expected"),
    [
        ({"documents": [{"location": "custom/a.json"}]}, "custom/a.json"),
        ({"document": {"location": "custom/b.json"}}, "custom/b.json"),
        ({"location": "custom/c.json"}, "custom/c.json"),
        ({"documents": [{"name": "d.json"}]}, "d.json"),
        ({}, ""),
        ("not a dict", ""),
    ],
)
def test_extract_location_handles_response_shapes(payload: object, expected: str) -> None:
    assert _extract_location(payload) == expected


def test_client_requires_base_url() -> None:
    from docmd.anythingllm import AnythingLLMError

    with pytest.raises(AnythingLLMError):
        AnythingLLMClient("", "key")


def test_client_repr_redacts_api_key() -> None:
    text = repr(AnythingLLMClient("http://x", "super-secret-key"))
    assert "super-secret-key" not in text
    assert "redacted" in text


def test_client_upload_and_embed_use_expected_endpoints(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[tuple[str, str, dict | None]] = []

    def fake_request(self, method, path, payload=None):  # type: ignore[no-untyped-def]
        calls.append((method, path, payload))
        if path == "/api/v1/document/raw-text":
            return {"documents": [{"location": "custom/doc.json"}]}
        return {}

    monkeypatch.setattr(AnythingLLMClient, "_request", fake_request)
    client = AnythingLLMClient("http://x", "k")

    result = client.upload_markdown("Title", "# body", source="a.pdf")
    client.embed("research", [result.location])

    assert calls[0][0] == "POST"
    assert calls[0][1] == "/api/v1/document/raw-text"
    assert calls[0][2]["textContent"] == "# body"
    assert calls[1][1] == "/api/v1/workspace/research/update-embeddings"
    assert calls[1][2] == {"adds": ["custom/doc.json"], "deletes": []}


def test_client_embed_noop_on_empty_list(monkeypatch: pytest.MonkeyPatch) -> None:
    called = False

    def fake_request(self, *a, **k):  # type: ignore[no-untyped-def]
        nonlocal called
        called = True
        return {}

    monkeypatch.setattr(AnythingLLMClient, "_request", fake_request)
    AnythingLLMClient("http://x", "k").embed("w", [])
    assert called is False


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def test_cli_engines_lists_all(capsys: pytest.CaptureFixture[str]) -> None:
    assert cli.main(["engines"]) == cli.EXIT_OK
    out = capsys.readouterr().out
    assert "plaintext" in out
    assert "markitdown" in out


def test_cli_convert_reports_success(
    workspace: tuple[Path, Path], capsys: pytest.CaptureFixture[str]
) -> None:
    source, dest = workspace
    (source / "doc.txt").write_text(" ".join(["word"] * 40))

    code = cli.main(
        ["convert", "-i", str(source), "-o", str(dest), "-e", "plaintext"]
    )
    assert code == cli.EXIT_OK
    assert "converted=1" in capsys.readouterr().out


def test_cli_convert_json_output(
    workspace: tuple[Path, Path], capsys: pytest.CaptureFixture[str]
) -> None:
    source, dest = workspace
    (source / "doc.txt").write_text(" ".join(["word"] * 40))
    cli.main(["convert", "-i", str(source), "-o", str(dest), "-e", "plaintext", "--json"])
    assert json.loads(capsys.readouterr().out)["summary"]["converted"] == 1


def test_cli_missing_input_is_a_config_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    code = cli.main(["convert", "-i", str(tmp_path / "nope"), "-o", str(tmp_path)])
    assert code == cli.EXIT_CONFIG
    assert "does not exist" in capsys.readouterr().err


def test_cli_returns_failure_exit_code(
    workspace: tuple[Path, Path], capsys: pytest.CaptureFixture[str]
) -> None:
    source, dest = workspace
    (source / "bad.json").write_text("{invalid")
    code = cli.main(["convert", "-i", str(source), "-o", str(dest), "-e", "plaintext"])
    assert code == cli.EXIT_FAILURES


def test_cli_check_without_credentials_is_config_error(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    for var in ("ANYTHINGLLM_BASE_URL", "ANYTHINGLLM_API_KEY", "ANYTHINGLLM_WORKSPACE"):
        monkeypatch.delenv(var, raising=False)
    assert cli.main(["check"]) == cli.EXIT_CONFIG
