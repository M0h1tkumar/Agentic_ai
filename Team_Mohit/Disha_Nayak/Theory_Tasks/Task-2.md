# Privacy Policies of Major LLM Providers: OpenAI, Google, Anthropic (2026)

## Abstract



## 1\. OpenAI (ChatGPT)

* **Free/Plus (consumer)**: the default setting is ON, meaning they can use your chats</cite> for training. Opt-out exists under Settings → Data Controls but is not prominent.
* **Business (Team/Enterprise)**: Business (Team/Enterprise): Safe. Training is OFF by default. OpenAI explicitly states they do not train on Team/Enterprise data.</cite>
* **API**: not used for training by default.
* **Deletion**: OpenAI normally schedules deletions within about 30 days, but has to retain some deleted ChatGPT logs longer due to ongoing litigation.</cite>
* **Advertising**: the US Privacy Policy disclaims selling personal data, but appears to permit certain advertising-related sharing subject to opt-out controls.</cite>

## 2\. Google (Gemini)

* **Free consumer**: Defaults to training with human review. To stop it, you must disable "Gemini Apps Activity," which forces you to lose your chat history.</cite>
* **Paid individual (Gemini Advanced/Google One)**: treated same as free — Your data is treated as consumer data. You still face the "Privacy vs. History" trade-off.
* **Business (Workspace)**: If you access Gemini via a paid Google Workspace business account, your data is treated like Workspace Gmail or Drive data—private and never used for training.
* **Retention quirk**: Google may retain conversation data for up to 72 hours after interactions even with this disabled, for safety and abuse monitoring purposes.
* **API**: not trained on by default.

## 3\. Anthropic (Claude)

* **Policy shift**: as of August 2025, Anthropic moved from opt-in to opt-out training for consumer plans (Free, Pro, Max). consumer users would need to actively opt out if they didn't want their Claude conversations used to train future models. The deadline was September 28. If you missed it, your data was in.
* **Retention impact**: The opt-in training setting extends data retention from 30 days to 5 years, a 60x increase in how long your conversations can sit in Anthropic's training pipeline.
* **Standard retention (opted out)**: Once deleted, they're removed from your chat history immediately but remain on Anthropic's back-end systems for up to 30 days before being permanently deleted.
* **Safety-flag carve-out**: Anthropic retains the right to use inputs and outputs for model improvement when conversations are "flagged for safety review," regardless of a user's stated opt-out.
* **Incognito**: Conversations in Incognito Mode on Claude are never used for training, even without changing this setting.
* **Business/Enterprise \& API**:Business (Claude Team): Safe. Training is strictly prohibited by default. Anthropic does not train on API traffic by default. Enterprise accounts are also excluded from training.
* **API log retention**: reduced from 30 days to 7 days as of September 2025 (per industry tracking sources).

## 4\. Side-by-Side Summary

|Provider|Free/Consumer default|Paid Individual|Business/Enterprise|API|
|-|-|-|-|-|
|OpenAI|Train ON (opt-out)|Train ON (opt-out)|Train OFF|Train OFF|
|Google|Train ON (opt-out via Activity toggle)|Train ON (same as free)|Train OFF (Workspace)|Train OFF|
|Anthropic|Train ON since Aug 2025 (opt-out)|Train ON (opt-out)|Train OFF|Train OFF|

## 5\. Key Takeaway

All three follow the same shape: **consumer tiers default to training-on, business/API tiers default to training-off.** The meaningful differences are retention length (Anthropic's 5-year figure stands out) and carve-outs (Anthropic's safety-flag exception bypasses opt-out). None currently offer full retroactive deletion from already-trained models — opting out stops future use, not past.

