# Closed Source vs Open Weight vs Open Source Models

## The three buckets
1. **Closed Source** — you get an API endpoint and nothing else. No weights, no architecture code, no training data. You send a request, pay per token, get a response.
   - Examples: GPT-4o/5, Claude, Gemini (via their hosted APIs).
   - Pros: zero infra to manage, always the latest version, fastest way to prototype.
   - Cons: your prompts leave your machine, no fine-tuning of the base weights, cost scales with usage forever, and you're at the mercy of the vendor's pricing/availability decisions.

2. **Open Weight** — the trained parameters (the weight files) are published and downloadable, but the training data and often the full training code are not. You can run it locally, fine-tune it, quantize it — but you can't fully reproduce how it was built.
   - Examples: Llama 3 family, Qwen3, Gemma, Mistral (some releases).
   - Pros: full data privacy (nothing leaves your machine), fine-tune for a niche domain, no ongoing per-token API bill after the hardware investment, works offline/air-gapped.
   - Cons: you need your own GPU capacity, and you're extending someone else's black-box training run rather than understanding it end to end.

3. **Open Source (Open Weight + open pipeline)** — weights, training code, and often the dataset/recipe are all public, so the whole thing is inspectable and reproducible.
   - Examples: OLMo, Falcon, some Mistral/EleutherAI releases.
   - Pros: full transparency, academic reproducibility, freedom to modify the architecture itself.
   - Cons: heaviest infra and expertise requirement of the three; fewer models actually reach this bar compared to "open weight."

## Quick comparison
| Aspect | Closed Source | Open Weight | Open Source (full) |
|---|---|---|---|
| Access to weights | No | Yes | Yes |
| Access to training data | No | No | Usually yes |
| Fine-tuning | Not possible / very limited | Full | Full + can retrain from scratch |
| Data privacy | Data leaves to provider | Fully local | Fully local |
| Infra cost | Low (API billing only) | High (own GPUs) | High (own GPUs) |
| Vendor lock-in | High | None | None |
| Ease of use | Easiest (just call the API) | Moderate | Hardest |

## When to reach for which
- Need a working prototype today, no ML infra → **Closed source**.
- Need to fine-tune on private/proprietary data, or must run offline → **Open weight**.
- Doing research that needs full reproducibility or wants to change the architecture itself → **Open source (full pipeline)**.

## My takeaway
"Open" is a spectrum, not a binary — most models people call "open source" today (Llama, Qwen) are actually **open weight**, since the training data isn't released. True open source (data + code + weights) is rarer and mostly comes from research labs rather than product companies.
