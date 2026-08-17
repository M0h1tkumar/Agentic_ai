# LLM vs SLM — a summary

**Manish Prakash · Team Mohit**

---

## The distinction

**LLM (Large Language Model)** — tens of billions to trillions of parameters.
Frontier models: GPT-5 family, Claude, Gemini, Llama 70B+.

**SLM (Small Language Model)** — roughly **under 10 billion parameters**, often
1–8B, small enough to run on a laptop, a phone, or a single modest GPU. Examples:
Phi (Microsoft), Gemma 2B/9B (Google), Llama 3.x 1B/3B/8B (Meta), Qwen small
variants, Mistral 7B.

The boundary is fuzzy and moves every year. **The useful definition is not a
parameter count — it is where the model can run.** An SLM runs on hardware you
already own. An LLM needs a datacentre or an API.

---

## Why SLMs got good

Three developments, in order of importance:

1. **Data quality over data quantity.** The Phi series demonstrated that carefully
   curated, textbook-quality training data produces small models that outperform much
   larger models trained on scraped web text. This was the key insight and it
   generalised.
2. **Distillation.** Training a small model on a large model's outputs transfers a
   surprising amount of capability.
3. **Quantisation.** 4-bit quantisation cuts memory roughly 4× for a modest quality
   cost — see [`06_model_formats_and_gguf.md`](06_model_formats_and_gguf.md). A 7B
   model at Q4 needs about 4 GB and runs on a laptop.

The result: a 2026-era 7B model comfortably outperforms a 2022-era 175B model on
most practical tasks. **"Small" is a statement about resources, not about quality.**

---

## Can you actually train one yourself?

"You cannot train an LLM" is true of one activity and false of two others, and the
distinction decides what is realistic for a small team.

| Activity | LLM (70B+) | SLM (1–8B) |
|---|---|---|
| **Pretraining from scratch** | No. Thousands of GPUs, months, millions of dollars, and a curated trillion-token corpus. Not a small-team activity in any sense. | Expensive but genuinely attainable for a funded team |
| **Full fine-tuning** (all weights) | Needs serious multi-GPU infrastructure | Achievable on a handful of GPUs |
| **LoRA / QLoRA** (adapters, base frozen) | **Feasible for an individual**, up to 13B–70B depending on quantisation | Easy — often a laptop-class GPU or free Colab |

So the honest position: **individuals cannot pretrain an LLM, but they can
absolutely fine-tune one.** LoRA is what collapsed the gap, by training a small set
of low-rank adapter matrices while the base weights stay frozen and quantised.

This is exactly the path taken in
[`../Master_Tasks/04_unsloth_finetuning/`](../Master_Tasks/04_unsloth_finetuning/) —
a 7B model, 4-bit base, LoRA adapters, single consumer GPU.

---

## Comparison

| Dimension | LLM | SLM |
|---|---|---|
| Parameters | 70B – 1T+ | ~1B – 10B |
| Hardware | Multi-GPU cluster / API | Laptop, phone, single GPU |
| Memory (4-bit) | 40 GB+ | 1–6 GB |
| Latency | Higher; network round trip | Low; often faster than the network |
| Cost per token | Meaningful | Near zero after hardware |
| Offline | No (unless self-hosted at scale) | **Yes** |
| Privacy | Data leaves your machine | **Data never leaves** |
| General reasoning | **Strong** | Limited |
| Long, multi-step tasks | **Strong** | Degrades |
| Broad world knowledge | **Extensive** | Thin |
| Narrow task after fine-tuning | Strong | **Competitive, often equal** |
| Fine-tuning cost | High | **Low — hours on one GPU** |
| Hallucination | Present | More frequent, especially on facts |
| Context window | Very large | Smaller, and quality degrades sooner |

---

## Where each one wins

**Use an LLM for:**
- Open-ended reasoning and analysis.
- Long multi-step agentic work — the planning step in
  [`../30_July_2026/multi_agent_team.md`](../30_July_2026/multi_agent_team.md) is
  exactly this.
- Tasks needing broad world knowledge.
- Complex code generation.
- Anything where you cannot predict the input.

**Use an SLM for:**
- **Classification, extraction, routing, tagging** — narrow, high-volume,
  well-defined. An SLM fine-tuned on your labels will match or beat a general LLM
  and cost a fraction.
- **On-device work** — phones, embedded systems, offline laptops.
- **Privacy-critical data** — medical, legal, financial. Nothing leaves the machine,
  and no privacy policy applies at all
  ([`02_privacy_policies_llm_providers.md`](02_privacy_policies_llm_providers.md)).
- **Latency-critical paths** where a network round trip is already too slow.
- **High-volume, low-complexity** work where per-token cost dominates.
- **Air-gapped environments.**

---

## The hybrid pattern — the practically important one

Real systems increasingly use both, and this is where most of the value is:

```
Request → SLM (local)
            ├─ simple / routine  → answer directly
            └─ complex           → escalate to LLM (API)
```

Routing cheap work to a local SLM and reserving the LLM for hard cases can remove a
large share of API spend and latency without a noticeable quality drop. The catch is
that **the router itself must be accurate** — a bad escalation decision is worse
than never escalating.

The same structural idea appears throughout this program: strong model for the
orchestrator, cheap model for the workers; router in front of both
([`../03_August_2026/omniroute_notes.md`](../03_August_2026/omniroute_notes.md)).

---

## Trade-offs to be honest about

**SLM downsides that matter:**
- **Thin factual knowledge.** A small model has genuinely memorised less. RAG is not
  optional here, it is the fix.
- **Weaker instruction following**, especially for complex or multi-part
  instructions.
- **Degrades on long chains** — the failure mode in agent loops is losing the thread
  a few steps in.
- **More hallucination on facts**, precisely because knowledge is thin.
- **You own the infrastructure**, the updates, and the safety behaviour.

**LLM downsides that matter:**
- **Cost scales with success** — the better your product does, the larger the bill.
- **Data leaves your control.**
- **Network dependency** and provider rate limits.
- **Overkill for narrow tasks.** Using a frontier model to classify support tickets
  is paying for reasoning you discard.

---

## Summary

- **Size is about deployment, not quality.** An SLM is a model that runs where you
  need it to.
- **SLMs are now genuinely capable** because of data quality, distillation, and
  quantisation — a 7B model today beats a 175B model from a few years ago.
- **For narrow, well-defined, high-volume tasks, a fine-tuned SLM is usually the
  right answer** and often the better one, at a fraction of the cost.
- **For open-ended reasoning and long agentic chains, LLMs remain clearly ahead**,
  and this gap is real rather than a matter of tuning.
- **The hybrid — local SLM with LLM escalation — is where most production systems
  are heading**, and it captures most of the cost saving with most of the capability.
- **Pair an SLM with RAG.** Small models are thin on facts; retrieval is the
  correction, and it is cheaper than trying to fine-tune knowledge in.
