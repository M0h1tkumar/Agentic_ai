# Privacy policies of major LLM providers — OpenAI, Google, Anthropic

**Manish Prakash · Team Mohit**

> **Read this first.** Provider privacy terms change frequently — all three
> materially revised theirs during 2024–2025. This document describes the *structure*
> of these policies and the questions to ask, which is stable; the specific settings
> are not. **Verify against the live policy before making any decision that matters.**
> Links in §7.

---

## 1. The single most important fact

**The consumer product and the API are governed by different terms, and the
difference is usually "your data trains the model" versus "it does not."**

Across all three providers, the same pattern holds:

| Tier | Typical default |
|---|---|
| **Consumer** (ChatGPT free/Plus, Gemini app, Claude.ai) | Data **may** be used to improve models, often opt-out rather than opt-in |
| **API / developer** | Inputs and outputs **not** used for training by default |
| **Enterprise / business** | Not used for training; additional controls, DPAs, sometimes zero-retention |

If you take one thing from this document: **the free consumer chat window is the
riskiest place to paste confidential material, and the API is the safest** — the
opposite of most people's intuition, because the consumer product feels more
personal and less "sent somewhere."

---

## 2. What every one of these policies actually covers

Reading all three side by side, they answer the same seven questions. Comparing them
question by question is far more useful than reading them end to end:

1. **What is collected?** Prompts, outputs, uploaded files, account data, device and
   usage telemetry.
2. **Is it used for training?** The headline question. Tier-dependent everywhere.
3. **Do humans see it?** All three allow human review for safety, abuse detection,
   and quality — this surprises people more than the training question.
4. **How long is it kept?** Distinguish *your* retention (deletable) from
   *safety/abuse* retention (usually not deletable, typically ~30 days).
5. **Who else gets it?** Sub-processors, cloud infrastructure, and legal requests.
6. **Where does it go?** Cross-border transfer, which is the compliance question in
   the EU and increasingly in India under the DPDP Act.
7. **What control do you have?** Opt-out, delete, export, retention settings.

---

## 3. Provider summaries

### OpenAI

- **Consumer (ChatGPT).** Conversations may be used to improve models by default;
  there is a setting to turn this off, and Temporary Chat exists for one-off
  sessions. Turning training off historically also affected history features.
- **API.** Data submitted through the API is **not** used to train models by
  default. This has been the stated position since March 2023 and is the reason to
  build on the API rather than paste into the chat window.
- **Retention.** API data retained for a limited period (around 30 days) for abuse
  monitoring, then deleted. Zero Data Retention is available for eligible endpoints
  and customers on request.
- **Business/Enterprise.** No training on business data; SOC 2, encryption in
  transit and at rest, admin controls, DPA available.
- **Human review.** Possible for safety and abuse investigation.

### Google (Gemini)

- **Consumer (Gemini app).** Gemini Apps Activity governs whether conversations are
  saved and used to improve services. Google has been explicit that **reviewed
  conversations may be read by human reviewers** and advises against entering
  confidential information. Reviewed samples have historically been retained for an
  extended period (up to ~3 years) **detached from your account** — meaning deleting
  your activity does **not** delete already-reviewed samples. This is the single
  most under-appreciated clause across all three providers.
- **Vertex AI / Google Cloud.** Enterprise terms: customer data is **not** used to
  train foundation models, governed by the Cloud Data Processing Addendum, with data
  residency options.
- **AI Studio.** Sits between the two; free-tier usage has historically had weaker
  guarantees than paid Vertex. Check the tier you are actually on.
- **Broader context.** Gemini data handling interacts with Google Account-wide
  settings, which is a genuinely different posture from the other two — Google has
  far more surrounding context about the user.

### Anthropic (Claude)

- **Consumer (Claude.ai).** Historically Anthropic did *not* train on user
  conversations by default — a notable differentiator. **This changed in 2025**:
  consumer users are now asked to choose, with training on chats and coding sessions
  permitted unless the user opts out, and a longer retention period for those who
  allow it. **Check your current setting.**
- **API / Commercial.** Inputs and outputs are **not** used to train models by
  default under the commercial terms.
- **Retention.** Limited retention for trust-and-safety purposes; enterprise
  arrangements can reduce it.
- **Human review.** For safety and policy enforcement.
- **Additional posture.** Published Usage Policy, and copyright indemnification for
  commercial customers.

---

## 4. Comparison

| Question | OpenAI | Google | Anthropic |
|---|---|---|---|
| Consumer data trains models | Yes by default, opt-out | Yes if activity on, opt-out | Now opt-out (changed 2025) |
| API/enterprise data trains models | No | No (Vertex) | No |
| Human review possible | Yes | Yes — explicitly stated | Yes |
| Reviewed data survives deletion | — | **Yes, up to ~3 years** | — |
| Abuse-monitoring retention | ~30 days | Varies by product | Limited |
| Zero-retention option | Yes, eligible customers | Enterprise arrangements | Enterprise arrangements |
| Free tier weaker than paid | Yes | Yes | Yes |

---

## 4a. Certifications and contractual controls

Policy prose describes intent. Certifications and contracts are what a procurement
or compliance review actually asks for, and they are a separate axis from the
training question above.

| Control | OpenAI | Google | Anthropic |
|---|---|---|---|
| **SOC 2 Type II** | Yes | Yes (Google Cloud) | Yes |
| **ISO 27001** | Yes | Yes | Yes |
| **GDPR DPA** | Available | Cloud Data Processing Addendum | Available |
| **HIPAA BAA** | Available, eligible customers | Available (Google Cloud) | Available, eligible API customers |
| **Data residency** | Some enterprise tiers | Regional options on Vertex | Enterprise arrangements |
| **SSO / SAML** | Enterprise, Team | Google Workspace / Cloud IAM | Enterprise |
| **SCIM provisioning** | Enterprise | Cloud Identity | Enterprise |
| **Audit logs** | Enterprise, Team | Cloud Audit Logs | Enterprise |
| **Encryption in transit and at rest** | Yes | Yes | Yes |

Two observations from lining these up:

- **These are overwhelmingly enterprise-tier features.** SSO, audit logs, and a BAA
  are not available on a consumer subscription, which is another reason the
  tier distinction in §1 matters more than the provider distinction.
- **A certification is not a privacy guarantee.** SOC 2 attests that stated controls
  are operating; it says nothing about whether your data trains a model. The two
  questions are independent and are frequently conflated in vendor comparisons.

Verify current certification status directly — each provider maintains a trust
centre, and scope changes over time.

---

## 5. Practical guidance

**For individuals**

1. **Do not paste confidential material into a free consumer chat.** All three
   effectively tell you this in their own documentation.
2. **Turn training off** where the setting exists, and know that it may not remove
   what has already been reviewed.
3. **Understand that deletion is not always deletion** — safety retention and
   already-sampled data are commonly exempt.

**For teams and products**

4. **Build on the API, not the consumer product.** Different legal terms, better
   defaults, and it is the difference that matters most.
5. **Get a DPA** if you process personal data. Under GDPR or India's DPDP Act this
   is not optional.
6. **Ask for zero data retention** if you handle regulated data. It exists; it is
   often gated behind a request.
7. **Redact before sending.** The strongest privacy control is not transmitting the
   data. Strip PII, secrets, and customer identifiers client-side.
8. **Consider local models** for genuinely sensitive workloads — an on-premise model
   via Ollama or LM Studio has no third-party privacy policy at all. This is a real
   argument for the local-model and fine-tuning work elsewhere in this program.
9. **Re-read the policies periodically.** All three changed materially in the last
   two years, and Anthropic's consumer change reversed a differentiator people had
   relied on.

---

## 6. Agent-specific concerns

Agents make this materially worse, and it is worth stating separately:

- **An agent sends far more data than a chatbot.** It reads files, command output,
  database rows, and repository contents — and all of it goes into the prompt. You
  are no longer choosing what to share message by message.
- **Tool output is not reviewed by a human before transmission.** An agent that runs
  `cat .env` to debug something has just sent your secrets to a provider.
- **Multi-agent systems multiply exposure.** Every hop is another transmission.
- **Logging.** Your own agent logs may contain more sensitive data than the provider
  ever receives, in a less protected place.

The practical rule: **an agent's data exposure is its entire accessible
environment, not the prompt you typed.** Sandboxing is a privacy control as much as
a security one.

---

## 7. Sources — verify before relying

- OpenAI Privacy Policy: <https://openai.com/policies/privacy-policy>
- OpenAI Enterprise privacy: <https://openai.com/enterprise-privacy>
- Google Privacy Policy: <https://policies.google.com/privacy>
- Gemini Apps privacy notice: <https://support.google.com/gemini/answer/13594961>
- Google Cloud / Vertex AI data governance: <https://cloud.google.com/vertex-ai/generative-ai/docs/data-governance>
- Anthropic Privacy Policy: <https://www.anthropic.com/legal/privacy>
- Anthropic Commercial Terms: <https://www.anthropic.com/legal/commercial-terms>

---

## 8. Conclusion

The three policies converge on the same structure: **weaker guarantees for free
consumer use, strong guarantees for paid API and enterprise use.** The differences
between providers matter less than the difference between tiers within any one of
them.

The two clauses most people miss:

1. **Human reviewers may read your conversations** — stated plainly by all three.
2. **Deleting your data does not always delete already-sampled data.** Google is
   explicit that reviewed conversations persist detached from your account.

And the two facts that should change behaviour: **use the API rather than the chat
window for anything that matters**, and **remember that an agent transmits its whole
environment, not just your prompt.**
