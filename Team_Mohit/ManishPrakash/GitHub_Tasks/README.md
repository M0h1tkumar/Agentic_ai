# GitHub Tasks — written deliverables

**Manish Prakash · Team Mohit**

The six standalone papers from the "Tasks to be uploaded on GITHUB" list in the
program README.

| # | Paper | File |
|---|---|---|
| 1 | Chatbot vs AI Agent | [`01_chatbot_vs_ai_agent.md`](01_chatbot_vs_ai_agent.md) |
| 2 | Privacy policies of major LLM providers (OpenAI, Google, Anthropic) | [`02_privacy_policies_llm_providers.md`](02_privacy_policies_llm_providers.md) |
| 3 | Closed vs open-source vs open-weight models | [`03_closed_open_source_open_weight.md`](03_closed_open_source_open_weight.md) |
| 4 | Top 3 model training & tuning tools + recommendation | [`04_model_training_tools.md`](04_model_training_tools.md) |
| 5 | LLM vs SLM | [`05_llm_vs_slm.md`](05_llm_vs_slm.md) |
| 6 | Model formats and GGUF | [`06_model_formats_and_gguf.md`](06_model_formats_and_gguf.md) |

## One-line summaries

1. **A chatbot responds; an agent acts.** The difference is tools and a loop, not
   model quality — and the underused middle ground is a fixed workflow with LLM
   calls inside it.
2. **Consumer tiers and API tiers have different privacy terms**, and the gap
   between tiers matters more than the gap between providers. Human reviewers can
   read consumer conversations, and deletion does not always delete.
3. **Most models called "open source" are open weight.** Downloadable, but no
   training data and a restricted licence — which matters legally and for auditing.
4. **Start with Unsloth** — VRAM is the real constraint. But dataset quality
   dominates tool choice, and RAG usually beats fine-tuning for adding facts.
5. **"Small" is about where a model runs, not how good it is.** Fine-tuned SLMs win
   on narrow high-volume tasks; LLMs still clearly win on open-ended reasoning.
6. **`.safetensors` for training, `.gguf` for local inference.** Default to
   `Q4_K_M`, and prefer a bigger model at lower precision over a smaller one at
   higher precision.

## A thread running through all six

Every one of these papers ends up at the same place: **match the tool to the
constraint, not to the hype.** Use a workflow instead of an agent when the steps are
known. Use the API instead of the chat window when privacy matters. Use an SLM when
the task is narrow. Use retrieval instead of fine-tuning when you need facts.

The capability ceiling is rarely the binding constraint. Cost, privacy, latency, and
predictability usually are.
