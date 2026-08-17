# Closed, open-source, and open-weight models

**Manish Prakash · Team Mohit**

---

## The confusion this clears up

"Open source AI" is used loosely, and the looseness hides a real distinction.
**Llama is not open source.** Neither is Gemma. They are **open weight** — you can
download and run them, but you did not get the training data, you did not get the
training code, and the licence restricts what you may do.

Three categories, not two:

| | Weights | Training code | Training data | Licence |
|---|---|---|---|---|
| **Closed** | No | No | No | API terms of service |
| **Open weight** | Yes | Partial or none | No | Custom, often restricted |
| **Open source** | Yes | Yes | Yes | OSI-approved (Apache 2.0, MIT) |

---

## 1. Closed models

The weights never leave the provider. You access the model through an API.

**Examples:** GPT-4/5 family (OpenAI), Claude family (Anthropic), Gemini (Google).

**Positives**
- Usually the frontier of capability.
- Zero infrastructure — no GPUs, no serving stack, no ops.
- Managed safety, updates, and scaling.
- Commercial support, SLAs, indemnification.
- Access to provider-specific features (prompt caching, extended thinking,
  computer use) that generic interfaces do not expose.

**Negatives**
- **Your data goes to a third party** — see
  [`02_privacy_policies_llm_providers.md`](02_privacy_policies_llm_providers.md).
- **No offline or air-gapped use.**
- **The model can change or be retired underneath you.** A version deprecation can
  silently alter your product's behaviour.
- **Ongoing per-token cost** that scales with success.
- **Vendor lock-in** and no ability to inspect, audit, or deeply customise.
- **Rate limits** you do not control.

---

## 2. Open-weight models

The trained parameters are published. You can download, run, fine-tune, and deploy
them. What is **not** published: the training dataset, and usually the full training
pipeline. The licence is typically custom rather than OSI-approved.

**Examples:** Llama (Meta), Gemma (Google), Mistral's released models, Qwen
(Alibaba), DeepSeek releases.

**Positives**
- **Run locally or on-premise** — data never leaves your infrastructure. The
  decisive advantage for regulated or sensitive work.
- **Fine-tunable** on your own data (the Unsloth track in this program).
- **No per-token cost** — you pay for compute you already control.
- **Version stability.** The weights on your disk do not change under you.
- **Quantisable** to run on modest hardware — see
  [`06_model_formats_and_gguf.md`](06_model_formats_and_gguf.md).
- **Offline capable.**
- **Inspectable** — you can examine activations, probe behaviour, and study the
  model in ways an API forbids.

**Negatives**
- **Licence restrictions are real.** Llama's community licence imposes conditions
  above a user threshold and restricts some uses. Read it — "downloadable" is not
  "unrestricted".
- **Not reproducible.** Without the data and pipeline you cannot rebuild or audit
  the model's origins.
- **You own the infrastructure**: GPUs, serving, scaling, monitoring, security.
- **Generally behind the frontier**, though the gap has narrowed considerably.
- **You own safety.** Guardrails are your problem now.
- **Unknown training data** — a genuine legal and bias risk, since you cannot check
  what went in.

---

## 3. Open-source models

Weights, training code, **and** dataset published under an OSI-approved licence.
Fully reproducible: in principle you could retrain the model yourself.

**Examples:** OLMo (AI2), Pythia (EleutherAI), BLOOM, and other research-lab
releases. This category is much smaller than the other two.

**Positives**
- **Full reproducibility** and genuine auditability of the training data.
- **Permissive licence** with no usage restrictions.
- **The only category suitable for rigorous safety and bias research**, because you
  can trace behaviour back to data.
- **No legal ambiguity** about provenance.

**Negatives**
- **Capability lags** — these come from research labs with smaller compute budgets
  than frontier labs.
- **Fewer options**, less tooling, smaller ecosystems.
- **Reproducing training is theoretically possible and practically expensive.**
- Less commercial polish and support.

---

## 4. Why the distinction matters

**Legally.** "Open source" carries a specific meaning (the OSI definition:
freedom to use, study, modify, and redistribute without field-of-use restriction).
Llama's licence fails that test. Procurement, compliance, and legal review care
about this, and calling an open-weight model "open source" in a compliance document
is a factual error.

**For auditing.** You cannot check a model for bias, memorised personal data, or
copyrighted training material without the dataset. Open weight gives you the
artifact; only open source gives you the provenance.

**For risk.** Unknown training data is unquantified legal exposure. Most
organisations accept it, but they should do so knowingly.

**For the ecosystem.** The Open Source Initiative published a definition of Open
Source AI in 2024 precisely because the term was being applied to models that do not
meet it. The debate is ongoing and worth being accurate about.

---

## 5. Choosing

| Situation | Choice |
|---|---|
| Need maximum capability, data can leave your network | **Closed** |
| Prototyping fast | **Closed** — no infrastructure |
| Sensitive or regulated data | **Open weight**, self-hosted |
| Air-gapped or offline | **Open weight** |
| Fine-tuning on proprietary data | **Open weight** |
| High volume, cost-sensitive | **Open weight** — fixed compute beats per-token |
| Need version stability guarantees | **Open weight** |
| Auditing training data, safety research | **Open source** |
| Licence must be unrestricted | **Open source** |

**A hybrid is common and sensible:** a closed frontier model for hard reasoning, a
self-hosted open-weight model for bulk or sensitive work. A router makes that a
config decision rather than an architectural one — see
[`../03_August_2026/omniroute_notes.md`](../03_August_2026/omniroute_notes.md).

---

## 6. Summary

- **Closed** — best capability, least control, your data leaves.
- **Open weight** — the practical middle ground and where most self-hosting happens.
  Downloadable, fine-tunable, but not reproducible and not licence-free.
- **Open source** — fully reproducible and auditable, smaller and less capable.
- **Most models called "open source" are open weight.** The difference is the
  training data and the licence, and it matters legally and for auditability.
- Choose on **data sensitivity and control requirements first**, capability second.
  The capability gap keeps narrowing; the privacy and licence differences do not.
