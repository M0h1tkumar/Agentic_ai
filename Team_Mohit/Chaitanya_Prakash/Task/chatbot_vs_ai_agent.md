# Chatbot vs AI Agent — Notes

## Why people mix these up
Both are powered by the same underlying LLMs, and both talk to you in natural language. The difference isn't the language model — it's what's wrapped around it: whether the system can act, remember, and decide the next step on its own, or whether it just answers and stops.

## Core distinction
- **Chatbot:** reactive. It receives a message, retrieves relevant context (often via RAG), and returns one generated reply. No planning loop, no tool selection, no follow-through — each turn is a single, isolated LLM call.
- **AI Agent:** goal-driven. It runs inside an observe → reason → act → evaluate loop, can call external tools/APIs, maintains memory across steps, and keeps working — re-planning if needed — until the goal is met or it's blocked.

## A concrete example
Customer says: "I got the wrong colour, I want a refund."
- A **chatbot** replies with the returns policy and a link to a form.
- An **agent** looks up the order, checks it against the return policy, processes the refund in the backend system, sends a confirmation, and closes the ticket — no human step in between.

## Five dimensions that actually separate them
| Dimension | Chatbot | AI Agent |
|---|---|---|
| Understanding | Matches intent to a script/FAQ or answers from a knowledge base | Understands context and reasons across multiple connected systems |
| Action | Read-only — can inform, can't do | Read *and* write — can execute actions with side effects |
| Memory | Stateless or very short-lived | Persists context across steps and sessions |
| Reasoning | None — one prompt in, one reply out | Multi-step planning; can chain observations and actions |
| Autonomy | Waits for the next human prompt every time | Keeps going independently, pausing only for sensitive/approval-gated steps |

## Where each one fits
- **Chatbots are the right call** for predictable, low-risk, linear queries — pricing questions, password-reset steps, document lookup. Adding agentic complexity here is pure overhead.
- **Agents earn their cost** when a task spans multiple systems, depends on context, needs follow-up, or currently involves a human doing manual copy-paste work between tools.


## My takeaway
Most products marketed as "AI agents" today are still closer to a retrieval chatbot with a nicer UI — the real test is whether the system can independently take an action with a consequence (refund issued, ticket closed, API called) rather than just describing what the user should do next.

