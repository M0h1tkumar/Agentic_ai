# Unsloth fine-tuning — dataset preparation and LoRA training

**Master task 4:** dataset selection, model selection, model fine-tuning (Colab or
Unsloth Studio).

Two programs:

| File | What it does | Status |
|---|---|---|
| [`prepare_dataset.py`](prepare_dataset.py) | Validate, deduplicate, and format an instruction dataset | **48 tests passing, verified end to end** |
| [`train.py`](train.py) | LoRA fine-tune with Unsloth, evaluate, export GGUF | Compiles and is Colab-ready; **not run here** — no CUDA GPU on this machine |

That split is honest and deliberate. The claim "I ran a fine-tune" is not one I can
support from this environment, so the training script is presented as reviewable
code with its parameter choices explained, while the part that can be proven —
dataset preparation — is fully tested and demonstrated below.

---

## Why the dataset tool came first

From [`../../GitHub_Tasks/04_model_training_tools.md`](../../GitHub_Tasks/04_model_training_tools.md):

> Tool choice is the least important decision in a fine-tune. Dataset quality
> dominates everything.

Writing the dataset tool first is that conclusion applied rather than asserted.
Most failed fine-tunes are failed datasets wearing a training script, and the
specific failure is rarely exotic:

- **Refusals in the training data.** A dataset scraped from chat logs is full of
  "As an AI language model, I cannot…". Train on those and you get a model that
  refuses.
- **Duplicated prompts with different answers.** Not two examples — one
  contradiction in the training signal.
- **Truncated responses.** Teaches the model to stop mid-sentence.
- **Silent length overflow.** Examples longer than `max_seq_length` are cut off,
  so the model learns from answers whose endings it never saw.

None of these produce an error. They produce a model that is quietly worse, and you
find out after paying for the training run. `prepare_dataset.py` catches all four
before that.

---

## Dataset preparation

### Run it

```bash
python3 prepare_dataset.py samples/finetune_qa.jsonl -o data/ --val-split 0.1 \
    --system "You are a concise machine learning tutor."
```

### Actual output

```
Source:   samples/finetune_qa.jsonl  (65 records)
Accepted: 60
Rejected: 5

Rejections by reason:
      2  response is a refusal or placeholder
      1  missing instruction field
      1  response looks truncated
      1  duplicate prompt

First 5 rejected records:
  [13] missing instruction field
  [27] response is a refusal or placeholder  > As an AI language model, I cannot help with that.
  [28] response looks truncated  > The main reasons are...
  [46] duplicate prompt  > What is LoRA and why is it used? (variant 0)
  [51] response is a refusal or placeholder  > N/A

Statistics:
  examples                 60
  prompt_chars_mean        48.4
  output_chars_mean        164.9
  combined_chars_max       246
  estimated_tokens_p95     61

Warning: Only 60 examples. LoRA can work from a few hundred, but below ~100
expect the adapter to memorise rather than generalise.

Wrote 54 examples to data/train.jsonl
Wrote 6 examples to data/validation.jsonl
```

The sample dataset in [`samples/finetune_qa.jsonl`](samples/finetune_qa.jsonl)
contains five deliberately broken records, one of each failure type, so the
detection above is demonstrable rather than claimed.

### What it handles

- **Input formats:** JSON, JSONL, CSV. Field-name aliases are normalised
  (`instruction`/`question`/`prompt`/`query`, `output`/`answer`/`response`/
  `completion`), because public instruction datasets are inconsistent about this
  and fixing it once here is cheaper than special-casing it everywhere downstream.
- **Deduplication by prompt**, not by prompt-and-response, for the contradiction
  reason above. Normalised for case and whitespace first.
- **Deterministic splitting.** Seeded, so two runs give the same split. Without
  that, a validation score is not comparable between runs and holding data out
  achieves nothing.
- **Length statistics in characters**, with a token estimate. A real token count
  needs the target model's tokeniser, which is a heavy dependency for a
  preprocessing step; characters divided by four is close enough to choose
  `max_seq_length`.
- **Warnings that predict training problems:** dataset too small, rejection rate
  too high, examples longer than a typical sequence limit, responses suspiciously
  terse.

### Tests

```bash
python3 -m pytest tests/ -q
```

```
48 passed
```

One test caught a real ordering bug: `"N/A"` was being rejected as "response too
short" because the length check ran before the refusal check. That sends a reviewer
looking for a formatting problem instead of the actual one, which is that the source
data is full of non-answers. Refusal detection now runs first.

---

## Training

```bash
pip install unsloth trl peft accelerate bitsandbytes datasets

python3 train.py --data data/ --model unsloth/Qwen2.5-7B-Instruct-bnb-4bit
python3 train.py --data data/ --export-gguf Q4_K_M
```

The script refuses to start without a CUDA GPU and says so plainly, rather than
failing deep inside a library call twenty seconds later.

### Parameter choices and why

| Setting | Default | Reasoning |
|---|---|---|
| `load_in_4bit` | True | The single change that makes a 7B model trainable on a 16 GB card at all |
| `lora_r` | 16 | Adapter rank. 8 is often enough for style; 32+ for genuinely new capability. Higher r means more memory and more overfitting risk |
| `lora_alpha` | 16 | Scaling. Keeping it equal to `r` is the safe default |
| `lora_dropout` | 0.0 | Unsloth's optimised path is fastest at zero; add dropout only if overfitting |
| Target modules | attention + MLP | Adapting attention alone trains fewer parameters and consistently underperforms on instruction following |
| `batch_size` × `grad_accum` | 2 × 4 = 8 | Effective batch of 8 without the memory cost of actually holding one |
| `optim` | `adamw_8bit` | 8-bit optimiser states; a large saving for no measurable quality cost |
| `use_gradient_checkpointing` | `"unsloth"` | Trades compute for memory. Without it, activations for a 2048-token sequence do not fit alongside the model |
| `packing` | False | Packing concatenates short examples and corrupts instruction-tuning boundaries |
| `lr_scheduler` | cosine | Standard for short fine-tuning runs |
| `max_seq_length` | 2048 | Set it above your dataset's p95, which `prepare_dataset.py` reports |

### The setting that matters most

`format_dataset()` uses the tokeniser's own `apply_chat_template` rather than a
hand-written prompt string. A mismatch between how you format at training time and
how the model is prompted at inference time is the most common cause of a fine-tune
that trains cleanly, shows a falling loss, and then behaves badly when actually
used. The loss curve will not warn you.

---

## Model selection

For a single consumer GPU or free Colab:

| Model | Size | Fits on | Use for |
|---|---|---|---|
| `unsloth/Qwen2.5-7B-Instruct-bnb-4bit` | 7B | T4 16 GB | Good general default, strong multilingual |
| `unsloth/llama-3.2-3B-Instruct-bnb-4bit` | 3B | T4, comfortably | Faster iteration, narrow tasks |
| `unsloth/mistral-7b-instruct-v0.3-bnb-4bit` | 7B | T4 16 GB | Permissive licence (Apache 2.0) |
| `unsloth/llama-3.1-8B-Instruct-bnb-4bit` | 8B | T4, tight | Strongest of these, least headroom |

Pick the **smallest model that clears your quality bar**. A 3B that trains in
fifteen minutes lets you run four experiments in the time a 8B runs one, and
iteration count matters more than base capability when you are still learning what
your data does.

---

## The whole loop

```
raw data -> prepare_dataset.py -> train.py -> adapter -> GGUF (Q4_K_M) -> Ollama
```

GGUF export closes the loop, which is one of the better arguments for Unsloth over
Axolotl or LLaMA-Factory: no separate conversion step between finishing training and
running the result locally. Format background:
[`../../GitHub_Tasks/06_model_formats_and_gguf.md`](../../GitHub_Tasks/06_model_formats_and_gguf.md).

---

## Before you fine-tune at all

Worth restating, because it is the most common wasted effort in this space:

**Fine-tune to change behaviour, format, and style. Retrieve to add facts.**

If the goal is for the model to know your documents, RAG is cheaper, faster, and
updatable without retraining — that is
[`../02_doc_to_markdown/`](../02_doc_to_markdown/) plus
[`../../05_August_2026/anythingllm_mcp_server/`](../../05_August_2026/anythingllm_mcp_server/),
and it beats a fine-tune on exactly that job.
