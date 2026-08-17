# Top 3 tools for model training and tuning — a one-page summary

**Manish Prakash · Team Mohit**

---

## Scope

Full pre-training costs millions and is not a decision most teams make. The real
question is **fine-tuning**: adapting an existing open-weight model to your task,
your domain, or your format. These three tools dominate that space.

All three build on the same foundations — Hugging Face `transformers`, PEFT/LoRA,
and quantisation — so the comparison is about **ergonomics, speed, and memory**, not
about fundamentally different capabilities.

---

## The three

### 1. Unsloth — fastest, lightest, single-GPU

Custom Triton kernels and a manually optimised backward pass replace the standard
implementations. The claim is roughly **2× faster training and ~50–70% less VRAM**
with no loss in accuracy, and it holds up in practice.

- **Strength:** fits models on hardware that otherwise cannot train them. A 7–8B
  model becomes tunable on a free Colab T4; a 13B on a single consumer card.
- **Weakness:** single-GPU focus (multi-GPU is a paid/less mature path), and a
  supported-architecture list rather than universal coverage.
- **Interface:** a Python API that drop-in replaces the usual `transformers` +
  `trl` loading code. Small diff from a standard script.
- **Exports to GGUF directly**, which closes the loop to Ollama and LM Studio — see
  [`06_model_formats_and_gguf.md`](06_model_formats_and_gguf.md).

### 2. Axolotl — most configurable, production-oriented

A YAML-driven training framework. You describe the run — base model, dataset,
LoRA/QLoRA/full fine-tune, sequence length, distributed strategy — and it executes.

- **Strength:** reproducibility and breadth. The config file *is* the experiment
  record, which is exactly what you want when tuning is a repeated activity rather
  than a one-off. Broad model support, mature multi-GPU via DeepSpeed/FSDP.
- **Weakness:** steepest learning curve. The configuration surface is large and the
  failure messages assume you know the stack.
- **Best fit:** teams running many experiments and needing to reproduce them.

### 3. LLaMA-Factory — broadest coverage, gentlest on-ramp

Supports the widest range of models and training methods (SFT, LoRA, QLoRA, DPO,
PPO, reward modelling) and ships a **web UI** alongside its CLI.

- **Strength:** you can run a real fine-tune without writing code, and the method
  coverage means you rarely outgrow it. The best tool for learning what the knobs do.
- **Weakness:** the abstraction hides mechanics, which is fine until something
  breaks. Slower and heavier than Unsloth on identical hardware.
- **Best fit:** learning, evaluation, and comparing methods.

---

## Comparison

| | Unsloth | Axolotl | LLaMA-Factory |
|---|---|---|---|
| Primary strength | Speed & VRAM | Configurability | Coverage & ease |
| Interface | Python API | YAML config | Web UI + CLI |
| Learning curve | Low | High | Lowest |
| Single consumer GPU | **Excellent** | Workable | Good |
| Multi-GPU | Limited (free tier) | **Excellent** | Good |
| Model coverage | Curated list | Broad | **Broadest** |
| Method coverage | SFT, LoRA, QLoRA, DPO | Broad | **Broadest** |
| Reproducibility | Script-based | **Config-as-record** | UI state, less rigorous |
| GGUF export | **Built in** | Via conversion | Via conversion |
| Free Colab viable | **Yes** | Tight | Yes |

---

## Honourable mentions

**Hugging Face TRL + PEFT** — the layer all three sit on. Use it directly when you
need control the wrappers do not expose. **Torchtune** — PyTorch-native, clean, and
worth watching. **Cloud services** (Vertex, Bedrock, OpenAI fine-tuning) — trade
control and cost for zero infrastructure, and only work with that vendor's models.

---

## Recommendation

**For this program and for most small teams: start with Unsloth.**

The reasoning:

1. **Hardware is the actual constraint.** Not knowledge, not tooling — VRAM.
   Unsloth's memory reduction is what makes fine-tuning possible at all on a single
   consumer GPU or a free Colab session. A tool you can run beats a better tool you
   cannot.
2. **Fast iteration teaches more.** Fine-tuning is empirical; you learn by running
   many experiments. Halving the training time doubles the number of experiments per
   day, and that compounds.
3. **The GGUF export closes the loop.** Train, quantise, and run in Ollama or LM
   Studio without a separate conversion step. Seeing your own model answer in a chat
   window is what makes the work concrete.
4. **The exit cost is low.** It is a thin optimised layer over standard
   `transformers`/`peft`, so the concepts and much of the code transfer directly to
   Axolotl or TRL later.

**Then:**
- **Move to Axolotl** when you have multiple GPUs, or when reproducing an experiment
  from three weeks ago starts to matter. Config-as-record is worth the learning curve
  at that point and not before.
- **Use LLaMA-Factory** to explore a method you have not tried — DPO, reward
  modelling — because comparing approaches in a UI is faster than wiring each one up.

**And the point that outranks all three:** tool choice is the least important
decision in a fine-tune. **Dataset quality dominates everything.** A thousand
carefully curated, correctly formatted examples beat a hundred thousand noisy ones,
regardless of which tool trains them. If you have limited time, spend it on the data.

Finally: **confirm fine-tuning is the right answer at all.** For adding knowledge,
RAG is usually cheaper, faster, and easier to update — the AnythingLLM work in
[`../05_August_2026/06_anythingllm_rag_as_mcp.md`](../05_August_2026/06_anythingllm_rag_as_mcp.md).
Fine-tune to change *behaviour, format, and style*; retrieve to add *facts*.
