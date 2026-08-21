# Other AI Model Formats and GGUF

## Introduction

AI models are distributed in different file formats depending on the machine learning framework, storage requirements, optimization techniques, and deployment environment.

Different formats are designed for different purposes such as training, model storage, interoperability, and local inference.

---

## Common Model Formats

| Format | Used By | Main Purpose |
|---------|---------|--------------|
| GGUF | llama.cpp and related tools | Local LLM inference |
| Safetensors | Hugging Face and other frameworks | Safe model weight storage |
| PyTorch (.pt/.pth/.bin) | PyTorch | Training and model storage |
| TensorFlow (.ckpt/.pb) | TensorFlow | Training and model storage |
| ONNX | Multiple frameworks | Cross-platform deployment |
| TensorRT Engine | NVIDIA | GPU-optimized inference |
| Core ML | Apple | Apple device deployment |
| TFLite | TensorFlow Lite | Mobile and edge deployment |

---

## 1. Safetensors

### Definition

Safetensors is a file format designed for storing neural network tensors safely and efficiently.

It is widely used in the modern Hugging Face ecosystem.

### Advantages

- Safer than pickle-based serialization
- Fast loading
- Efficient storage
- Widely supported
- Suitable for distributing model weights

### Example

```text
model.safetensors