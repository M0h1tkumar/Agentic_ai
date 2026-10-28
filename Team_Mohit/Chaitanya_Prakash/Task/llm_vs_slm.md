# LLM vs SLM — Summary Paper

## Framing
Language models today split into two operating philosophies: **Large Language Models (LLMs)**, which chase broad, general-purpose reasoning ability, and **Small Language Models (SLMs)**, which trade some of that breadth for speed, low cost, and the ability to run on-device.

## Comparison
| Dimension | LLM | SLM |
|---|---|---|
| Parameter scale | ~10B up to 1T+ | Typically under 10B (often 1B–8B) |
| Examples | GPT-4o, Claude, Llama 3 70B/405B | Llama 3.2 1B/3B, Phi-3.5, Qwen 3 8B, Gemma 2B/7B |
| General reasoning | Strong zero-/few-shot reasoning | Basic to moderate; improves a lot with fine-tuning |
| Latency | Higher — API round trip or large forward pass | Low, often sub-10ms on-device |
| Fine-tuning cost | High — multi-GPU, can take weeks | Low — single consumer GPU, hours with QLoRA |
| Deployment | Cloud/API-based, needs real infra | Can run fully local — laptop, phone, edge device |
| Data privacy | Data typically leaves the device to a provider | Can be 100% on-device — nothing leaves |
| Context window | Very large (128K–1M tokens in top models) | Smaller, typically 4K–32K tokens |

## Where each wins
- **LLM territory:** open-ended research, complex multi-step reasoning, code generation across unfamiliar domains — situations where breadth matters more than cost or speed.
- **SLM territory:** narrow, repeated tasks — intent classification, structured data extraction, customer-support triage — high-volume pipelines where cost-per-query needs to stay near zero, and any privacy-sensitive workload that must stay fully local.

## The practical trend
SLMs are closing the capability gap for domain-specific work faster than raw parameter count would suggest, mainly because fine-tuning a small model on a narrow task now beats prompting a much larger general model for that same narrow task. For most production use cases, the winning pattern isn't "LLM vs SLM" — it's **LLM for the hard, general cases; a fine-tuned SLM for the high-volume, narrow ones**, often glued together with retrieval (RAG) to keep the smaller model grounded.

## My takeaway
If a task is well-defined, repeats often, and needs to run cheaply or privately, an SLM fine-tuned for that specific job will usually outperform a general LLM on cost and latency without giving up much accuracy — the LLM is worth its overhead mainly when the task itself is genuinely open-ended.
