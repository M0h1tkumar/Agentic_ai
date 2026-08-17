# Model formats — and what GGUF actually is

**Manish Prakash · Team Mohit**

---

## Why formats exist

A trained model is a large collection of numbered tensors plus the metadata needed
to interpret them. A *format* answers three questions:

1. **How are the tensors stored on disk?**
2. **What metadata travels with them** — architecture, tokeniser, hyperparameters?
3. **How fast and how safely can they be loaded?**

Different formats answer these differently, and the differences matter in practice —
one of them was a widely exploited security hole.

---

## The formats

### `.bin` / `.pt` — PyTorch pickle

The original. A Python `pickle` of the state dict.

- **Pro:** native to PyTorch, universally supported.
- **Con: `pickle` executes arbitrary code on load.** Downloading a `.bin` model from
  an untrusted source and loading it is equivalent to running a stranger's script.
  This is a real, exploited attack vector, not a theoretical one.
- Slow to load, memory-hungry, no memory-mapping.

**Status:** legacy. Avoid for anything downloaded.

### `.safetensors` — the current training/serving standard

Hugging Face's replacement for pickle. A simple layout: a JSON header describing
tensor names, dtypes, and byte offsets, followed by raw tensor data.

- **Safe by construction** — it is data, not code. Nothing to execute.
- **Fast, zero-copy loading** via memory mapping.
- **Framework-neutral** (PyTorch, TensorFlow, JAX).
- **Lazy loading** — read one tensor without reading the file.
- **Con:** stores weights only. The tokeniser and config live in separate files
  alongside it.

**Status: the default for full-precision weights.** If you are fine-tuning or
serving on GPU, this is your format.

### `.gguf` — the local-inference standard

The subject of the second half of this document. See §2.

### `.onnx` — cross-platform inference

Open Neural Network Exchange. A framework-neutral computation graph, so a model
trained in PyTorch can run in a C++, Java, or C# runtime, on CPU, GPU, or NPU.

- **Pro:** genuine portability, strong graph-level optimisation, good hardware
  vendor support.
- **Con:** conversion is fiddly for large transformers; less LLM-specific tooling
  than GGUF.
- **Use for:** embedding models, classifiers, and production inference in non-Python
  environments.

### `.tflite` — mobile and embedded

TensorFlow Lite. Heavily optimised for phones and microcontrollers. Dominant for
small on-device models; less used for LLMs.

### `.mlx` — Apple Silicon

Apple's framework, exploiting unified memory on M-series chips. Excellent on a Mac,
irrelevant elsewhere.

### `.engine` — NVIDIA TensorRT

A compiled, hardware-specific inference plan. Fastest possible NVIDIA inference,
at the cost of being tied to a specific GPU and TensorRT version. Production serving
at scale.

### Adapter formats

LoRA adapters are a few megabytes of low-rank matrices stored as `.safetensors`,
applied on top of a base model. This is why fine-tuning outputs are tiny and why you
can keep twenty task-specific adapters for one base model.

---

## Comparison

| Format | Purpose | Safe to load | Quantisation | Main use |
|---|---|---|---|---|
| `.bin` / `.pt` | PyTorch native | **No — executes code** | External | Legacy |
| `.safetensors` | Weight storage | Yes | External | Training, GPU serving |
| `.gguf` | Local inference | Yes | **Built in** | llama.cpp, Ollama, LM Studio |
| `.onnx` | Portable inference | Yes | Supported | Cross-platform production |
| `.tflite` | Mobile/embedded | Yes | Built in | On-device |
| `.mlx` | Apple Silicon | Yes | Supported | macOS local |
| `.engine` | TensorRT | Yes | Built in | NVIDIA production |

---

## 2. GGUF in detail

**GGUF — most commonly documented as "GPT-Generated Unified Format"**, though
"GGML Universal File" also circulates; the specification itself defines the format
without expanding the acronym. The format used by `llama.cpp` and everything built
on it: **Ollama, LM Studio, Jan, llamafile, text-generation-webui.** If you have run
a model locally, you have almost certainly used GGUF.

It replaced the older **GGML** format in August 2023, fixing GGML's central flaw:
GGML had no extensible metadata, so every architecture change broke compatibility
and required new conversion tooling.

### What makes it different

**1. It is a single self-contained file.**
Weights, tokeniser, vocabulary, architecture parameters, prompt template, and
licence metadata — all in one file. Compare with the `safetensors` approach, where a
model is a directory of weight shards plus `config.json`, `tokenizer.json`,
`tokenizer_config.json`, and more. One GGUF file is the entire model. That is why
`ollama run llama3.2` works with no setup: there is nothing to assemble.

**2. Extensible key-value metadata.**
An arbitrary KV store in the header. New architectures add new keys, and old files
still load. This is the specific fix for GGML's compatibility problem, and it is why
GGUF has survived several years of rapid architecture churn.

**3. Quantisation is built into the format.**
Not a separate step or a wrapper — the quantisation scheme is part of the file. This
is the whole reason GGUF exists.

**4. Memory-mapped loading.**
The OS pages weights in on demand. A model starts responding almost immediately
rather than after loading tens of gigabytes.

**5. CPU-first, with GPU offload.**
`llama.cpp` was built to run LLMs on CPUs. GGUF supports offloading a chosen number
of layers to a GPU, so a model larger than your VRAM still runs — partly on the GPU,
partly on the CPU. **No other mainstream format handles the "doesn't quite fit" case
this gracefully**, and that case is the normal one for consumer hardware.

### Quantisation levels

The naming looks cryptic and is actually systematic: `Q<bits>_<variant>`.

| Level | Bits | Size (7B) | Quality |
|---|---|---|---|
| `F16` | 16 | ~13 GB | Reference |
| `Q8_0` | 8 | ~7 GB | Essentially lossless |
| `Q6_K` | 6 | ~5.5 GB | Very close to reference |
| **`Q5_K_M`** | 5 | ~4.8 GB | Excellent balance |
| **`Q4_K_M`** | 4 | ~4.1 GB | **The standard recommendation** |
| `Q3_K_M` | 3 | ~3.3 GB | Noticeable degradation |
| `Q2_K` | 2 | ~2.8 GB | Significant degradation |

- **`_K`** — "K-quants", a smarter scheme that allocates more bits to the layers
  that matter most. Better quality at the same size than the older methods.
- **`_S` / `_M` / `_L`** — small, medium, large variants within a level.

**Practical rule: use `Q4_K_M`.** It is where the quality-per-gigabyte curve bends —
roughly a 4× size reduction for a quality loss most users cannot detect in normal
use. Go to `Q5_K_M` or `Q6_K` if you have the memory; go below `Q4` only if you must,
and expect it to show.

**The more important rule: a larger model at lower precision usually beats a smaller
model at higher precision.** A 13B at `Q4_K_M` generally outperforms a 7B at `Q8_0`
at a similar file size. Spend your memory budget on parameters, not on bits per
parameter.

### Creating GGUF

```bash
# From a Hugging Face model
python llama.cpp/convert_hf_to_gguf.py ./my-model --outfile my-model-f16.gguf

# Quantise
./llama.cpp/llama-quantize my-model-f16.gguf my-model-Q4_K_M.gguf Q4_K_M
```

Unsloth exports to GGUF directly at the end of a fine-tune, which is one of the
better reasons to use it — see
[`04_model_training_tools.md`](04_model_training_tools.md).

### Limitations

- **Inference only.** You cannot train or fine-tune a GGUF file. Fine-tune in
  `safetensors`, then convert.
- **Quantisation is lossy and irreversible.** Keep the full-precision weights.
- **Not the fastest on high-end GPUs** — vLLM with `safetensors`, or TensorRT, will
  beat it when the model fits comfortably in VRAM. GGUF wins on constrained
  hardware, not on datacentre hardware.
- **Conversion lags new architectures** by days or weeks after release.

---

## Summary

- **`.safetensors` for training and GPU serving.** Safe, fast, the current standard.
  It exists because `.bin`/pickle **executes code on load** — a real security flaw,
  and the reason to avoid legacy pickle files entirely.
- **`.gguf` for local inference.** One self-contained file, quantisation built in,
  memory-mapped loading, CPU-first with partial GPU offload. It is what makes running
  a capable model on a laptop routine rather than an achievement.
- **`.onnx`** for cross-platform production, **`.tflite`** for mobile, **`.mlx`** for
  Apple Silicon, **`.engine`** for maximum NVIDIA throughput.
- **The typical lifecycle:** train or fine-tune in `safetensors` → convert to GGUF →
  quantise to `Q4_K_M` → run in Ollama or LM Studio.
- **Default to `Q4_K_M`**, and prefer a bigger model at lower precision over a
  smaller model at higher precision.
