# docmd — document to markdown, ingested into AnythingLLM

**Master task 2:** convert doc/pdf/etc to `.md` with MarkItDown or Docling, then
connect the result to AnythingLLM.

A command-line tool and Python package that walks a directory, converts every
document it recognises to markdown with provenance frontmatter, and optionally
uploads and embeds the result into an AnythingLLM workspace.

**Status:** 58 tests passing, CLI verified end to end against real files. The
AnythingLLM upload path is covered by tests against a stub transport; it has not
been run against a live AnythingLLM instance from this machine.

---

## Why it is built this way

**The standard library alone is enough to run it.** With no third-party package
installed, `docmd` still converts text, markdown, CSV, JSON, HTML, and XML using a
built-in engine. MarkItDown and Docling are optional extras that add PDF and Office
formats. A tool that cannot start until you have resolved a dependency tree is a
tool people abandon.

**Conversion is separated from ingestion.** `docmd convert` needs no credentials
and no network. You can inspect the markdown, fix what the converter got wrong, and
only then ingest. Pipelines that upload as a side effect of converting give you no
opportunity to look at what you are about to embed.

**Provenance is attached at conversion time.** Every output file carries YAML
frontmatter with the source filename, path, type, engine, timestamp, and SHA-256.
When an agent later retrieves a passage, "where did this come from?" has an answer.
That metadata cannot be reconstructed afterwards, so it is written at the only
moment it is available.

**Runs are incremental.** A manifest maps each source path to its content hash.
Re-running skips files whose bytes have not changed, so an interrupted run over a
thousand documents costs only the remainder.

**Thin conversions are reported, not ingested.** A scanned PDF with no OCR layer
converts "successfully" into a handful of page numbers. `docmd` flags that as
`empty` and refuses to upload it. A contentless document in a knowledge base is
worse than a visible failure, because retrieval will still match it and the agent
will still cite it.

---

## Install

```bash
cd Master_Tasks/02_doc_to_markdown
pip install -e .                 # or: pip install -r requirements.txt
```

For PDF and Office formats, add an engine:

```bash
pip install -e ".[markitdown]"   # broad coverage, fast
pip install -e ".[docling]"      # better tables and PDF layout, slower
```

Check what is available:

```bash
python3 -m docmd engines
```

```
Conversion engines:
  markitdown   not installed
  docling      not installed
  plaintext    available
```

---

## Usage

### Convert locally

```bash
python3 -m docmd convert -i samples -o output
```

```
  ok       samples/page.html -> output/page.md (62 words)
  ok       samples/team.csv -> output/team.md (31 words)

converted=2  unchanged=0  skipped=0  empty=0  failed=0
```

Run it again and nothing is reconverted:

```
  cached   samples/page.html
  cached   samples/team.csv

converted=0  unchanged=2  skipped=0  empty=0  failed=0
```

### Ingest into AnythingLLM

```bash
cp .env.example .env      # fill in base URL, API key, workspace
set -a; source .env; set +a

python3 -m docmd check                       # verify credentials and workspace
python3 -m docmd ingest -i docs -o output -w research
```

### Other commands

```bash
python3 -m docmd workspaces                  # list AnythingLLM workspaces
python3 -m docmd convert -i docs --dry-run   # triage only, no conversion
python3 -m docmd convert -i docs --json      # machine-readable report
python3 -m docmd convert -i docs --overwrite # ignore the manifest
```

Exit codes: `0` success, `1` one or more files failed, `2` configuration error.
The failure code makes it usable in CI.

---

## Output format

```markdown
---
title: team
source_file: team.csv
source_path: samples/team.csv
source_type: csv
converted_by: plaintext
converted_at: 2026-08-07T15:39:20Z
sha256: 1a150f8b4b72f70e4c9012e36073d9b78d9b50afca59c6c3f8b5317ae73132e0
---

| name | role | focus |
| --- | --- | --- |
| Manish Prakash | Engineer | Agentic AI |
| Ada Lovelace | Analyst | Algorithms |
```

CSV becomes a markdown table rather than raw comma-separated text, because a table
survives chunking far better: the header stays visually attached to its rows.

---

## Architecture

```
discover  ->  triage  ->  convert  ->  normalise  ->  write  ->  upload  ->  embed
             (cheap)    (expensive)                          (network)
```

| Module | Responsibility |
|---|---|
| `config.py` | Environment-driven settings; validates upload credentials lazily |
| `triage.py` | Pure decisions: supported? too large? hidden? Plus slugging and hashing |
| `converters.py` | Three engines behind one interface, imported lazily |
| `markdown.py` | Normalisation and provenance frontmatter |
| `anythingllm.py` | REST client over `urllib`, no HTTP dependency |
| `pipeline.py` | Orchestration, manifest, run report |
| `cli.py` | Argument parsing and output formatting |

Triage is deliberately pure and runs before anything expensive. Deciding not to
process a file should never cost the price of opening it.

---

## Two things that are easy to get wrong

**1. Upload and embed are separate operations.** A document can exist in
AnythingLLM's storage without belonging to any workspace, in which case it is never
retrieved. `POST /api/v1/document/raw-text` uploads;
`POST /api/v1/workspace/{slug}/update-embeddings` attaches and embeds. Skipping the
second call is the most common reason ingestion appears to succeed while search
finds nothing. `docmd` always does both.

**2. Upload the markdown, not the original file.** Sending the source document
would make AnythingLLM re-parse it with its own extractor, discarding both the
conversion and the provenance frontmatter. That is why this uses the raw-text
endpoint rather than file upload.

---

## Tests

```bash
python3 -m pytest tests/ -q
```

```
58 passed
```

Coverage includes triage decisions, unicode slugging, content hashing, markdown
normalisation, frontmatter and YAML quoting, all three fallback converters,
configuration precedence, incremental re-runs, failure isolation, response-shape
handling for the AnythingLLM API, API-key redaction in `repr`, and CLI exit codes.

Network calls are tested against a stub transport rather than a live server, so the
suite runs offline in well under a second.

---

## Relationship to the rest of this repository

This is the ingestion half of the RAG story. The retrieval half is
[`../../05_August_2026/anythingllm_mcp_server/`](../../05_August_2026/anythingllm_mcp_server/),
which exposes the same AnythingLLM workspace to agents over MCP.

Together they form the full path:

```
documents -> docmd -> AnythingLLM (chunk, embed, store) -> MCP server -> agents
```

One note that connects the two: ingestion is a privileged operation. Anything
`docmd` uploads becomes retrievable by any agent connected to that workspace, and
retrieved text enters the model's context. A poisoned document is a prompt-injection
vector, so what you ingest is part of your trust boundary.
