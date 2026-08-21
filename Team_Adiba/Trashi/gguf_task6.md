## What is GGUF? What are other foramts of models?

| Format | Main use | Ecosystem |
|---|---|---|
| **Safetensors** | Training / fine-tuning / model sharing | Hugging Face, PyTorch, Transformers |
| **PyTorch (.bin)** | Older model weights | PyTorch / Transformers |
| **GGUF** | Local inference | llama.cpp, Ollama, LM Studio |
| **ONNX** | Cross-platform inference | ONNX Runtime, edge/mobile |
| **TensorRT-LLM** | High-performance NVIDIA inference | NVIDIA GPUs |
| **MLX** | Apple Silicon inference/training | |
| **AWQ** | Quantized inference | GPU inference frameworks |
| **GPTQ** | Quantized inference | GPU/local inference |
| **EXL2** | Quantized inference | ExLlama/ExLlamaV2 |

## GGUF

**GGUF (GPT-Generated Unified Format)** is a file format designed for storing and running large language models efficiently, particularly for local inference.

It is widely used in tools such as **llama.cpp, Ollama, and LM Studio**.

Unlike formats primarily intended for model training, GGUF is designed to package the **model weights, model architecture information, configuration, and other metadata into a single file**, making the model easier to load and run on local hardware.

## Why is GGUF useful?

Large language models can require a significant amount of memory.

GGUF supports different levels of **quantization**, which reduce the number of bits used to represent model weights.

Lower-bit **quantization** reduces the model’s memory requirements, allowing models to run on devices with limited RAM or VRAM.