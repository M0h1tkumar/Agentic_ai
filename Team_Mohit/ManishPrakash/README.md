# Manish Prakash — Agentic AI Programme

**Team Mohit**

Assignment and learning log. Date-wise task folders plus the standalone GitHub
papers.

---

## Date-wise tasks

| Date | Topic | Folder |
|---|---|---|
| **6 Aug 2026** | API vs MCP · MCP directories · Bhubaneswar weather predictor | [`06_August_2026/`](06_August_2026/) |
| **5 Aug 2026** | Multica via Docker · Slack · OpenCode · Recorder skills · **AnythingLLM RAG → MCP server** | [`05_August_2026/`](05_August_2026/) |
| **3 Aug 2026** | Multica install · OmniRoute | [`03_August_2026/`](03_August_2026/) |
| **30 Jul 2026** | Sessions 1–2 · OpenClaw multi-agent team · messaging bot | [`30_July_2026/`](30_July_2026/) |
| **29 Jul 2026** | Copilot agents · OAuth vs API keys · OpenClaw setup | [`29_July_2026/`](29_July_2026/) |

## Master tasks

The ongoing track from the program's "List of All Tasks", including three working
programs. Index: [`Master_Tasks/`](Master_Tasks/)

| # | Task | Deliverable |
|---|---|---|
| 1 | AnythingLLM setup | [`Master_Tasks/01_anythingllm_setup/`](Master_Tasks/01_anythingllm_setup/) |
| 2 | .md conversion → AnythingLLM | [`Master_Tasks/02_doc_to_markdown/`](Master_Tasks/02_doc_to_markdown/) — **58 tests** |
| 3 | LM Studio / Jan / Open Hands | [`Master_Tasks/03_local_model_runtimes/`](Master_Tasks/03_local_model_runtimes/) |
| 4 | Unsloth fine-tuning | [`Master_Tasks/04_unsloth_finetuning/`](Master_Tasks/04_unsloth_finetuning/) — **48 tests** |
| 5 | Skill Spector | [`Master_Tasks/05_skill_spector/`](Master_Tasks/05_skill_spector/) — **57 tests** |
| 6 | Sandbox / VM | [`Master_Tasks/06_sandbox_vm/`](Master_Tasks/06_sandbox_vm/) |

## GitHub papers

| # | Paper |
|---|---|
| 1 | [Chatbot vs AI Agent](GitHub_Tasks/01_chatbot_vs_ai_agent.md) |
| 2 | [Privacy policies — OpenAI, Google, Anthropic](GitHub_Tasks/02_privacy_policies_llm_providers.md) |
| 3 | [Closed vs open-source vs open-weight](GitHub_Tasks/03_closed_open_source_open_weight.md) |
| 4 | [Top 3 model training & tuning tools](GitHub_Tasks/04_model_training_tools.md) |
| 5 | [LLM vs SLM](GitHub_Tasks/05_llm_vs_slm.md) |
| 6 | [Model formats and GGUF](GitHub_Tasks/06_model_formats_and_gguf.md) |

Index and summaries: [`GitHub_Tasks/`](GitHub_Tasks/)

---

## Code in this repository

Five working programs, not just writeups. **163 tests passing.**

```bash
cd Master_Tasks/02_doc_to_markdown    && python3 -m pytest tests/ -q   # 58 passed
cd Master_Tasks/04_unsloth_finetuning && python3 -m pytest tests/ -q   # 48 passed
cd Master_Tasks/05_skill_spector      && python3 -m pytest tests/ -q   # 57 passed
```

### docmd — documents to markdown, ingested into AnythingLLM
[`Master_Tasks/02_doc_to_markdown/`](Master_Tasks/02_doc_to_markdown/)

Converts a directory of documents to markdown with provenance frontmatter, then
uploads and embeds into an AnythingLLM workspace. Standard library only by default;
incremental via a content-hash manifest.

### skillscan — static security scanner for agent skills
[`Master_Tasks/05_skill_spector/`](Master_Tasks/05_skill_spector/)

32 rules across nine risk families, scanning both a skill's code and the prose of
its `SKILL.md`. Verified against a benign skill (2/100) and a malicious fixture
(100/100, four correlated attack patterns).

### prepare_dataset — instruction dataset validation
[`Master_Tasks/04_unsloth_finetuning/`](Master_Tasks/04_unsloth_finetuning/)

Catches refusals, truncated responses, duplicate prompts, and length overflow before
they reach a training run. Paired with a Colab-ready Unsloth LoRA training script.

### Bhubaneswar Weather Predictor
[`06_August_2026/weather_predictor/`](06_August_2026/weather_predictor/)

Python CLI producing a real forecast for Bhubaneswar from Open-Meteo. Standard
library only, no API key, no dependencies.

```bash
python3 06_August_2026/weather_predictor/bhubaneswar_weather.py --days 7
```

It doubles as the worked example in the API vs MCP paper — every drawback listed
there is visible in its source.

### AnythingLLM RAG → MCP server
[`05_August_2026/anythingllm_mcp_server/`](05_August_2026/anythingllm_mcp_server/)

The advanced task. ~120 lines exposing AnythingLLM's vector store as four MCP tools,
so OpenClaw and Multica agents can retrieve documents during execution without any
client-side integration code.

---

## Ideas that recur across everything here

**MCP is a wrapper, not a replacement.** Nearly every MCP server sits on top of an
existing API. Its value is turning an M×N connector problem into M+N — one server,
every client, discovered at runtime.

**Context is the budget.** Cost, latency, and quality all degrade as the window
fills. Return references, not payloads. This one constraint explains multi-agent
architecture, RAG, session resets, and most of the tooling choices in these notes.

**Tool descriptions are the product.** In both programs here, the code is plumbing;
the engineering is in the docstrings that tell a model *when* to use each tool.

**Multi-agent systems manage context and permissions — they do not add
intelligence.** They made my output more consistent, not more insightful. Worth
knowing before building one.

**Granting a capability is not the same as using it.** An agent with a RAG tool and
no instruction to search will answer from memory every time.

**Sandbox first.** Every tool in this program executes shell commands. A VM or
container is blast-radius control, and it is also a privacy control — an agent
transmits its whole accessible environment, not just the prompt you typed.

**Match the tool to the constraint.** A fixed workflow instead of an agent when the
steps are known. The API instead of the chat window when privacy matters. An SLM
when the task is narrow. Retrieval instead of fine-tuning when you need facts. The
capability ceiling is rarely what is actually binding.

---

## A note on sourcing

Everything here is written from my own work and reading. Where I could not verify
something end to end on my own machine, the document says so rather than implying
otherwise. External sources are linked at the point they are used.
