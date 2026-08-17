# Master Tasks

**Manish Prakash · Team Mohit**

The "List of All Tasks" from the program README — the ongoing track that runs
alongside the date-wise assignments.

| # | Task | Deliverable | Status |
|---|---|---|---|
| 1 | AnythingLLM setup | [`01_anythingllm_setup/`](01_anythingllm_setup/) | Configuration reference |
| 2 | .md conversion, connected to AnythingLLM | [`02_doc_to_markdown/`](02_doc_to_markdown/) | **Working package, 58 tests** |
| 3 | LM Studio / Jan / Open Hands | [`03_local_model_runtimes/`](03_local_model_runtimes/) | Evaluation |
| 4 | Unsloth fine-tuning | [`04_unsloth_finetuning/`](04_unsloth_finetuning/) | **Dataset tool: 48 tests. Training script: Colab-ready** |
| 5 | Skill Spector | [`05_skill_spector/`](05_skill_spector/) | **Working scanner, 57 tests** |
| 6 | Sandbox / VM | [`06_sandbox_vm/`](06_sandbox_vm/) | Reference |

**163 tests passing across the three code deliverables.**

```bash
cd 02_doc_to_markdown     && python3 -m pytest tests/ -q   # 58 passed
cd 04_unsloth_finetuning  && python3 -m pytest tests/ -q   # 48 passed
cd 05_skill_spector       && python3 -m pytest tests/ -q   # 57 passed
```

---

## The three programs

### docmd — documents to markdown, ingested into AnythingLLM
[`02_doc_to_markdown/`](02_doc_to_markdown/)

Walks a directory, converts every recognised document to markdown with provenance
frontmatter, and uploads and embeds the result. Runs on the standard library alone;
MarkItDown and Docling are optional extras for PDF and Office formats. Incremental
via a content-hash manifest, so re-runs are nearly free.

```bash
python3 -m docmd convert -i samples -o output
python3 -m docmd ingest  -i docs -o output -w research
```

### skillscan — static security scanner for agent skills
[`05_skill_spector/`](05_skill_spector/)

32 rules across nine risk families, applied to both the code in a skill and the
prose of its `SKILL.md` — because a skill description is read by the model as
instruction, so prompt-injection text is an attack surface a conventional code
scanner cannot see. Correlates findings, scores risk, exits non-zero for CI.

```bash
python3 -m skillscan samples/note-sync
```

### prepare_dataset — instruction dataset validation
[`04_unsloth_finetuning/`](04_unsloth_finetuning/)

Validates, deduplicates, and formats instruction data before it reaches a training
run. Catches refusals, truncated responses, duplicate prompts, and silent length
overflow — four failures that produce no error and a quietly worse model.

```bash
python3 prepare_dataset.py samples/finetune_qa.jsonl -o data/
```

---

## How these connect

The master tasks are not independent; they compose into one pipeline.

```
documents
   |
   v
docmd (task 2) ......... convert, attach provenance, upload
   |
   v
AnythingLLM (task 1) ... chunk, embed, store
   |
   v
MCP server (5 Aug) ..... expose retrieval as tools
   |
   v
agents (OpenClaw, Multica)
   ^
   |
skillscan (task 5) ..... audit skills before they reach an agent
   |
runtime (tasks 3, 6) ... local models, inside a sandbox
   |
fine-tuned model (task 4) ... trained on validated data, exported as GGUF
```

Three ideas recur across all six:

**Standardise the interface, then swap the implementation.** An OpenAI-compatible
endpoint for models, MCP for tools, markdown for documents. Every integration in
this folder works because something upstream agreed on a format.

**Ingestion is a privileged operation.** Documents, skills, and MCP servers all end
up inside the model's trust boundary. `docmd` and `skillscan` are the two gates on
that boundary, and they exist for the same reason.

**Fine-tune for behaviour, retrieve for facts.** Task 4 and tasks 1–2 solve
different problems, and choosing wrongly between them is the most common wasted
effort in this space.
