# Local model runtimes — LM Studio, Jan, Ollama, Open Hands

**Master task 3:** LM Studio / Jan / Open Hands.

Three of these solve the same problem — run a model on your own hardware — and one
solves a different one. Grouping them together is worth correcting up front, because
Open Hands is not a runtime.

| Tool | What it actually is |
|---|---|
| **LM Studio** | GUI for downloading and running GGUF models locally, plus an OpenAI-compatible server |
| **Jan** | Open-source equivalent of the above, privacy-first |
| **Ollama** | CLI/daemon for local models; the one other tools integrate against |
| **Open Hands** | An autonomous **software-engineering agent**. Uses a model, is not one |

---

## Why run models locally at all

1. **Privacy.** Nothing leaves the machine, and no provider privacy policy applies —
   the strongest possible answer to the concerns in
   [`../../GitHub_Tasks/02_privacy_policies_llm_providers.md`](../../GitHub_Tasks/02_privacy_policies_llm_providers.md).
2. **Cost.** No per-token charge. For high-volume, low-complexity work this is the
   whole argument.
3. **Offline and air-gapped operation.**
4. **Version stability.** The weights on your disk do not change under you.
5. **Latency.** For a small model, local inference often beats the network round
   trip to a frontier API.

The trade is capability. A 7B local model is not a frontier model, and pretending
otherwise leads to disappointment — see
[`../../GitHub_Tasks/05_llm_vs_slm.md`](../../GitHub_Tasks/05_llm_vs_slm.md).

---

## Ollama

The one to install first. CLI-driven, minimal, and the runtime other tools assume.

```bash
curl -fsSL https://ollama.com/install.sh | sh     # or: brew install ollama
ollama serve

ollama pull qwen2.5:7b
ollama run qwen2.5:7b
ollama list
```

**It exposes an OpenAI-compatible endpoint at `http://localhost:11434/v1`**, which
is the single most useful fact about it. Any tool that accepts a custom base URL —
AnythingLLM, a router, your own code — works against it unchanged:

```python
from openai import OpenAI
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
```

From inside a Docker container, that host is `host.docker.internal`, not
`localhost`.

**Modelfiles** let you commit a system prompt and parameters alongside a model:

```
FROM qwen2.5:7b
PARAMETER temperature 0.3
SYSTEM "You answer concisely and say when you do not know."
```

```bash
ollama create tutor -f Modelfile
```

This is also the export target for the fine-tuning work in
[`../04_unsloth_finetuning/`](../04_unsloth_finetuning/): train, export GGUF,
`ollama create`, done.

**Note on that install command:** `curl … | sh` is exactly the pattern flagged as
`EXEC001` by [`../05_skill_spector/`](../05_skill_spector/). It is the vendor's own
documented installer, which is a reason to accept it, not a reason it stops being
what it is. Reading the script first costs nothing.

---

## LM Studio

A desktop GUI. Its real value is **discovery and experimentation**, not serving.

- Browse and download GGUF models from Hugging Face with a visible quantisation
  picker and a "will this fit in your RAM?" indicator. That indicator is genuinely
  the fastest way to build intuition for the size/quality trade-off in
  [`../../GitHub_Tasks/06_model_formats_and_gguf.md`](../../GitHub_Tasks/06_model_formats_and_gguf.md).
- Chat interface for immediate testing.
- **GPU offload slider** — the clearest illustration anywhere of GGUF's partial
  offload: put as many layers on the GPU as fit, run the rest on the CPU. Watching
  tokens-per-second change as you move it teaches more than reading about it.
- Local server mode exposes the same OpenAI-compatible API.

**Closed source**, which matters if that is a requirement.

**Use it to:** try five quantisations of the same model in ten minutes and decide
what your hardware can actually run.

---

## Jan

Open-source alternative to LM Studio. Similar GUI, similar model browser, similar
local server. Privacy-first positioning and an extension system.

**Choose Jan over LM Studio when** open source is a requirement. Otherwise they are
close enough that the choice is preference.

---

## Open Hands

Different category. An autonomous software-engineering agent: give it an issue, it
plans, writes code, runs tests, and iterates in a sandboxed environment.

```bash
docker run -it --rm --pull=always \
  -e SANDBOX_RUNTIME_CONTAINER_IMAGE=docker.all-hands.dev/all-hands-ai/runtime:latest \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -p 3000:3000 \
  docker.all-hands.dev/all-hands-ai/openhands:latest
```

It is model-agnostic, so it can be pointed at Ollama and run entirely locally —
which is the interesting combination and the reason it belongs in the same
discussion.

**The architectural point worth taking from it:** Open Hands runs the agent's work
inside a **dedicated container**, not on your host. That is the sandbox principle
from [`../06_sandbox_vm/`](../06_sandbox_vm/) built into the product rather than
left to the user. Compare with a terminal agent run directly on a laptop, where the
same autonomy operates on your real filesystem and real credentials.

Note the `docker.sock` mount above: that grants container-management rights, which
is close to host root. It is the price of the runtime spawning its own sandboxes,
and it is worth being conscious of rather than pasting past.

---

## Comparison

| | Ollama | LM Studio | Jan | Open Hands |
|---|---|---|---|---|
| Interface | CLI + API | GUI | GUI | Web UI |
| Open source | Yes | No | Yes | Yes |
| OpenAI-compatible server | Yes | Yes | Yes | n/a (consumer) |
| Model discovery | CLI registry | Excellent browser | Good browser | n/a |
| Scriptable | **Yes** | Limited | Limited | Yes |
| Category | Runtime | Runtime | Runtime | **Agent** |
| Best for | Serving, integration | Experimentation | Open-source experimentation | Autonomous coding |

---

## Hardware guidance

Practical VRAM/RAM requirements at `Q4_K_M`:

| Model size | Memory | Runs on |
|---|---|---|
| 1–3B | 1–3 GB | Any modern laptop, CPU acceptable |
| 7–8B | 4–6 GB | 8 GB GPU, or 16 GB system RAM on CPU |
| 13–14B | 8–10 GB | 12 GB GPU |
| 30B+ | 20 GB+ | 24 GB GPU or partial offload with patience |

**Prefer a larger model at lower precision over a smaller model at higher
precision.** A 13B at `Q4_K_M` generally beats a 7B at `Q8_0` at a similar file size.

---

## What I would use

- **Ollama** as the actual runtime. Scriptable, integrates with everything, and it
  is what AnythingLLM and the fine-tuning export path both target.
- **LM Studio** for the first hour with any new model, to find the largest
  quantisation that fits.
- **Open Hands** as the reference for how agent sandboxing should be arranged, and
  as a genuinely useful coding agent when pointed at a capable model.

The theme running through all of it is the same as MCP and LLM routers: **an
OpenAI-compatible endpoint is the interface everything agrees on.** Standardise the
interface, then swap the implementation freely.
