# Privacy Policies of Major LLM Providers: OpenAI, Google, and Anthropic

## Why This Matters

Every time you type into a chatbot, you're deciding — often without thinking about it — whether that text might end up shaping a future model. The three major providers handle this differently, and importantly, their policies have shifted meaningfully over the past year. What was true a year ago isn't necessarily true today, so it's worth checking the actual settings rather than assuming.

## The Pattern That Matters Most: Consumer vs. Business

Across all three providers, the single biggest factor isn't *which* company you use — it's *which tier* of that company's product you use. Business, Enterprise, and API access almost universally come with a "not used for training" guarantee. Free and personal-paid consumer tiers are where the real differences (and the real risk) live.

## OpenAI

**Consumer (ChatGPT Free/Plus):** Your conversations can be used to train future models *unless* you turn this off. The control lives under Settings → Data Controls → "Improve the model for everyone." Even with it off, new conversations are still retained for up to 30 days for abuse monitoring before deletion. If you give a thumbs-up/down on a response, that full conversation may be used for training regardless of your general setting.

**Business (API, ChatGPT Team/Enterprise):** Not used for training by default. API data is typically retained for a short window (around 30 days) purely for abuse monitoring, and Zero Data Retention (ZDR) is available for eligible enterprise customers.

**Worth knowing:** A 2025 court order tied to litigation with The New York Times required OpenAI to preserve certain output data going forward for consumer and non-ZDR API accounts, overriding the normal deletion schedule — a reminder that legal proceedings can override a company's own stated retention policy.

## Google (Gemini)

**Consumer (Gemini app, free and paid individual/"Advanced" tiers):** Data can be used for training by default. Turning this off means disabling "Gemini Apps Activity" in your Google account — which also means losing your chat history, since Google ties the two together. A "Temporary Chat" mode exists as a workaround: conversations there are automatically deleted after 72 hours and aren't used for training.

**Business (Google Workspace, Vertex AI, Gemini for enterprise):** Not used for training. Data here is governed by the Cloud Data Processing Addendum, the same framework that protects Workspace Gmail and Drive data.

## Anthropic (Claude)

This is the one that's changed the most, and it's worth calling out explicitly: Anthropic's stance used to be "we don't train on consumer conversations, full stop." That changed in late 2025.

**Consumer (Claude Free, Pro, Max):** As of the current policy, training is **opt-out**, not opt-in — meaning your conversations *can* be used to improve Claude unless you actively turn the setting off in Privacy Settings ("Help improve Claude"). If training is on, data may be retained for up to 5 years. If you opt out, retention drops back to roughly 30 days and your data isn't used for training.

**Business (API, Claude for Work/Enterprise, Bedrock, Vertex):** Unaffected by the above change — commercial and API data is still excluded from training by default, and Zero Data Retention agreements are available for eligible enterprise/API customers.

## Quick Comparison

| | OpenAI | Google (Gemini) | Anthropic (Claude) |
|---|---|---|---|
| Consumer default | Trains unless you opt out | Trains unless you opt out | Trains unless you opt out |
| Consumer opt-out cost | None (history kept) | Lose chat history | Retention drops to ~30 days |
| Business/API default | Not used for training | Not used for training | Not used for training |
| Enterprise ZDR available | Yes | Yes (Vertex AI) | Yes |
| Consumer retention if training is on | Standard retention window | Standard, ties to activity settings | Up to 5 years |

## Practical Takeaways

- **Assume consumer-tier chats can be used for training unless you've explicitly opted out** — this is now the default posture across all three providers, not the exception.
- **Never paste anything genuinely sensitive** — names, account numbers, medical details, client information — into a consumer-tier chat, regardless of your training settings, since some retention for safety review is unavoidable.
- **Use business/enterprise/API access for anything work-related.** That's where the "not used for training" guarantee is strongest and most consistent.
- **Check your settings periodically.** Policies in this space have changed materially within the last year, and they'll likely keep changing — what's accurate today may not be in six months.

## Conclusion

All three providers now converge on roughly the same shape: business and API tiers keep your data out of training, while consumer tiers train on your data by default unless you turn it off. The details of *how* you opt out, and what you lose or keep by doing so, differ enough that it's worth actually checking your own account settings rather than relying on a provider's general reputation — especially since, as Anthropic's 2025 policy shift shows, that reputation can change.

## By - Omm Sahoo