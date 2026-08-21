# Closed, Open-Source, and Open-Weight Models: Definitions and Trade-offs

## Abstract

## 1\. Definitions

**Closed model**: only API access. No weights, no training code, no data. Examples: GPT-4/5 series, Gemini (proprietary tiers), Claude. You send input, get output — the model itself never leaves the provider's infrastructure.

**Open-weight model**: model weights (the trained parameters) are downloadable and runnable locally, but training code, training data, and full methodology are NOT released. You can run and fine-tune it, but can't reproduce it from scratch or fully audit what it was trained on. Examples: Llama 3/4 family, Mistral, Qwen, DeepSeek, Gemma.

**Open-source model**: weights + training code + (ideally) training data or a documented data pipeline are released under an open license, satisfying reproducibility. True open-source AI is rare because full training data disclosure has legal and competitive costs. Examples: OLMo (Allen AI), Pythia, some BLOOM variants.

## 2\. Comparison Table

|Property|Closed|Open-Weight|Open-Source|
|-|-|-|-|
|Weights available|No|Yes|Yes|
|Training code available|No|Rarely|Yes|
|Training data disclosed|No|No|Yes (or documented)|
|Can self-host|No|Yes|Yes|
|Can fully audit/reproduce|No|No|Yes|
|Can fine-tune freely|Limited (API-based fine-tune only)|Yes, fully|Yes, fully|
|License restrictions|N/A (usage ToS)|Often has usage caps (e.g. Llama's 700M MAU clause)|Usually permissive (Apache/MIT)|
|Typical performance tier|Highest (frontier)|Near-frontier|Usually behind frontier|

## 3\. Why the Distinction Matters

* **Data sovereignty**: open-weight models can run entirely inside your infrastructure — no data leaves your network. Closed models require sending data to a third party.
* **Cost model**: closed = pay-per-token, predictable but ongoing. Open-weight = upfront compute/hosting cost, no per-token fee.
* **Customization depth**: full fine-tuning and architecture modification only possible with open-weight/open-source; closed models limit you to prompting or provider-hosted fine-tuning APIs.
* **Reproducibility/research**: only open-source lets researchers verify training data provenance, detect contamination, or replicate results — critical for scientific integrity.
* **Legal/licensing risk**: "open-weight" licenses often aren't OSI-approved open source (e.g. Llama license has field-of-use restrictions). Read the license, not the marketing label.

## 4\. Common Misconception

"Open-weight" is frequently marketed as "open-source." They are not the same. A model with public weights but a secret training corpus is open-weight, not open-source — you cannot verify or reproduce it, only use and adapt it.

## 5\. Conclusion

Use closed models for fastest time-to-market and top-tier capability without infra burden. Use open-weight models when you need self-hosting, data control, or deep fine-tuning without full reproducibility needs. Use open-source models only when auditability/reproducibility is a hard requirement (research, compliance-heavy domains) — accepting a capability trade-off.

