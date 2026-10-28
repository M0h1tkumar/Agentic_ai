# Privacy Policies — OpenAI, Google (Gemini), Anthropic (Claude)

## Why this matters
The biggest privacy risk isn't usually the fine print — it's that "consumer" and "business" tiers of the *same* product run on opposite defaults. Assuming your paid personal plan behaves like an enterprise plan is the most common mistake.

## OpenAI (ChatGPT / API)
- **Free & Plus (consumer):** may use your conversations to train models **unless you opt out** (Settings → Data Controls → "Improve the model for everyone").
- **Team, Enterprise, and the API (business):** the default flips — **not** used for training unless the org explicitly opts in.
- **Retention:** even when training is off, inputs/outputs are typically kept for up to 30 days for abuse monitoring before deletion, unless law requires longer. Enterprise customers can get Zero Data Retention (ZDR) on eligible endpoints.
- **Practical note:** "not trained on" ≠ "not stored" — data still transits and sits on OpenAI's servers briefly even under the safer defaults.

## Google (Gemini)
- **Free / Gemini Advanced (consumer, incl. paid individual "Google One" tier):** governed by **Gemini Apps Activity**. If it's on, a subset of your chats can be reviewed by human raters (to improve quality/safety) and used to improve Google's models; reviewed chats are disconnected from your account and can be retained up to ~3 years.
- **Turning it off:** myaccount.google.com → Data & Privacy → Gemini Apps Activity → Off. This stops future conversations from being used for training, but Google still keeps a short (~72 hr) operational retention to actually serve the response.
- **Temporary Chat:** a session that isn't saved to your account and auto-clears after 72 hours, not used for training by default.
- **Business (Google Workspace / Vertex AI / paid API quota):** contractually walled off — content is not used for model training and stays within the organization's domain, matching how Gmail/Drive data is already handled.
- **Key catch:** the *paid individual* tier (Gemini Advanced) is still treated as consumer data — paying alone does not flip you into the safer default the way it does for a Workspace business account.

## Anthropic (Claude)
- **Free, Pro, and Max (consumer):** as of the September 2025 policy change, training moved from **opt-in to opt-out**. If you don't turn "Help improve Claude" off in Privacy Settings, new/resumed conversations (including Claude Code sessions on these tiers) can be used for training.
- **Retention swing:** opting in to training extends retention from the previous 30-day window to **up to 5 years** for the conversations affected.
- **Commercial Terms (API, Claude for Work, Bedrock, Vertex, Enterprise):** explicitly carved out — not subject to the consumer training default, and not affected by the 5-year retention change.
- **Deletion:** if you delete a conversation, it's excluded from future training use.

## Side-by-side snapshot
| Provider | Consumer default | Business/API default | Consumer retention if training is on |
|---|---|---|---|
| OpenAI | Opt-out (trains unless disabled) | Opt-in only (not trained by default) | ~30 days typical (short-term) |
| Google Gemini | Opt-out via Gemini Apps Activity | Not used for training (Workspace/Vertex) | Reviewed chats retained up to ~3 years |
| Anthropic Claude | Opt-out (as of Sept 2025 policy) | Not used for training (Commercial Terms) | Up to 5 years if opted in |

## My takeaway
All three follow the same pattern: **consumer plans default toward training, business/API plans default away from it.** None of this protects you from the actual biggest leak — pasting secrets, source code, or personal data directly into a prompt, since a permissive policy can't retroactively "un-train" what a model already saw. If working with sensitive data, use the business/API tier and confirm zero/short retention explicitly rather than relying on the consumer toggle.

---
