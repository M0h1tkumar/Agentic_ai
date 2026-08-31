# Model File Formats & GGUF

## Why format matters
A model's file format determines how it loads, what hardware it can run on efficiently, and how safe it is to distribute. The same trained weights can be packaged very differently depending on whether the target is a training cluster, a cloud inference server, or a laptop CPU.

## Common formats
| Format | Extension | Notes |
|---|---|---|
| PyTorch Checkpoint | `.pt` / `.bin` | Raw tensor dump using Python's `pickle` — flexible but carries a real security risk (pickle can execute arbitrary code on load). Standard output during training. |
| Safetensors | `.safetensors` | Hugging Face's replacement for pickle-based checkpoints — zero-copy, memory-mapped loading, no executable code. Now the default for sharing weights on the Hub. |
| ONNX | `.onnx` | Cross-framework graph format meant for portable, optimized inference across different runtimes/hardware backends. |
| TensorFlow SavedModel | `.pb` / directory | TensorFlow's native serialization; used mainly inside the TF/Keras ecosystem. |
| GGUF | `.gguf` | Single-file binary format built for efficient CPU (and hybrid CPU/GPU) inference — see below. |

## What is GGUF?
GGUF ("GPT-Generated Unified Format") is the file format used by **llama.cpp** and the tools built on it (including Ollama). It succeeded the earlier GGML format and is designed specifically to make running large models on consumer hardware practical.

Key properties:
- **Single-file packaging** — model weights, tokenizer, and metadata (architecture, quantization type, hyperparameters) all live in one `.gguf` file, so there's nothing extra to configure or ship alongside it.
- **Built-in quantization support** — GGUF natively supports multiple quantization levels (e.g., Q4_K_M, Q5_K_M, Q8_0), letting a model shrink from, say, 16GB down to 4–5GB by trading a small amount of accuracy for a large drop in memory footprint.
- **CPU-first, GPU-optional inference** — optimized so a model can run acceptably on a laptop CPU alone, with optional partial GPU offloading if a GPU is available.
- **mmap-based loading** — the file can be memory-mapped rather than fully loaded into RAM up front, which speeds up startup and lowers peak memory use.

## Why it matters for local/edge deployment
GGUF is the format that made "download a model and run it on your own laptop" realistic for models in the multi-billion parameter range — this is exactly the format `ollama pull` fetches under the hood. Without quantized single-file formats like this, running an 8B+ parameter model outside a GPU server would be impractical for most people.

## My takeaway
Think of the format choice as matching the stage of the pipeline: **Safetensors** while the model lives on a training/fine-tuning server, **GGUF** once it needs to leave that server and run efficiently on ordinary hardware (a laptop, a phone, an edge device).
