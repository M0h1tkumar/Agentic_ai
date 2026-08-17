# Model File Formats and GGUF Explained

## Abstract

## 1\. Major Model Formats

**PyTorch (.bin / .pt)**: native PyTorch serialization (pickle-based). Standard training/research format. Security risk: pickle can execute arbitrary code on load.

**SafeTensors (.safetensors)**: Hugging Face's safe alternative to .bin — same tensors, no pickle execution risk, faster loading. Now the default format on Hugging Face Hub.

**ONNX (.onnx)**: Open Neural Network Exchange — framework-agnostic graph format. Enables running a model trained in PyTorch inside ONNX Runtime, TensorRT, or other engines. Common for cross-platform production deployment.

**TensorFlow SavedModel / .h5**: TensorFlow/Keras native formats, used in TF-based pipelines and TF Serving.

**GGUF (.gguf)**: quantized, unified format for efficient CPU/edge inference via llama.cpp and its ecosystem. Covered in detail below.

**AWQ / GPTQ**: quantization formats optimized for GPU inference (used with vLLM, TGI). Not primarily CPU-oriented like GGUF.

**EXL2**: quantization format for the ExLlamaV2 engine — GPU-focused, popular for max-quality-per-VRAM tuning.

## 2\. What is GGUF

GGUF stands for GPT-Generated Unified Format. The name reflects its purpose: a unified, standardized way to store AI models that were originally in various formats (PyTorch, SafeTensors, etc.) It was created for the llama.cpp project. On August 21st 2023, GGML was replaced by GGUF which aims to address the limitations of GGML and improve the overall user experience, by offering more flexibility, extensibility, and compatibility with different types of LLMs.     

Key properties:

* Single-file packaging: weights + metadata + tokenizer in one file
* GGUF models can run entirely on CPU, entirely on GPU, or split layers across both. If your GPU has 8 GB of VRAM and the model needs 12 GB, llama.cpp offloads the overflow to system RAM automatically.     
* Runs on consumer hardware: laptops, Apple Silicon (Neural Engine), even phones
* Backbone of Ollama and LM Studio — If you're using Ollama or LM Studio, you're already on GGUF.     

## 3\. Quantization in GGUF

GGUF uses "K-quants" — mixed precision applied selectively across layers based on importance, not uniform rounding. Q4\_K\_M: the sweet spot — \~3.8GB for 7B models, +0.0535 perplexity increase. Q5\_K\_M: higher quality. Q6\_K: near-lossless — \~5.15GB for 7B models. Q8\_0: effectively lossless — \~6.7GB for 7B models.     

Practical guidance: For practical use, the difference between Q8 and Q4\_K\_M is hard to notice in conversation. The difference between Q4 and Q2 is very noticeable on complex reasoning tasks.      General rule: A larger model at lower precision almost always beats a smaller model at higher precision. A 70B Q4 model outperforms a 7B FP16 model by a wide margin.     

## 4\. GGUF vs GPU-Focused Formats

|Format|Target hardware|Best inference engine|Notes|
|-|-|-|-|
|GGUF|CPU / hybrid CPU-GPU / edge|llama.cpp, Ollama, LM Studio|Most flexible, widest hardware support|
|GPTQ|GPU only|vLLM, TGI|Calibration-based quantization, good accuracy|
|AWQ|GPU only|vLLM|Preserves important weights at higher precision|
|EXL2|GPU only|ExLlamaV2|Tunable bits-per-weight, max quality-per-VRAM|

Quick rule of thumb: If you're using Ollama or LM Studio, you're already on GGUF. If you're serving with vLLM, go AWQ. If you're tweaking for maximum quality on your RTX card, try EXL2.     

## 5\. Conclusion

GGUF is the standard for local, CPU-capable, hardware-flexible LLM deployment — not the format for GPU-only production serving, where GPTQ/AWQ dominate. Format choice depends on target hardware, not model quality: the same model can exist in all these formats simultaneously.

