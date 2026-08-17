# 30 July 2026 — Tasks

**Manish Prakash · Team Mohit**

## Assigned

1. Perform session 1 and session 2
2. OpenClaw multi-agent team creation (tasks 1–9)
3. *(optional)* Create a bot in Telegram / Discord / any messaging app instead of testing in the CLI
4. *(optional)* Download and set up Multica

## Deliverables

| # | Deliverable | File |
|---|---|---|
| 1 | Session 1 & 2 consolidated notes | [`sessions_1_and_2_notes.md`](sessions_1_and_2_notes.md) |
| 2 | Multi-agent team build, tasks 1–9 | [`multi_agent_team.md`](multi_agent_team.md) |
| 3 | Messaging-app bot integration | [`messaging_bot_integration.md`](messaging_bot_integration.md) |
| 4 | Multica setup | [`../03_August_2026/multica_setup.md`](../03_August_2026/multica_setup.md) — done properly on 3 August |

## Key takeaways

- **An agent is an LLM in a loop with tools and a goal.** Everything else is
  machinery around that loop, and knowing this tells you where to look when it breaks.
- **Context is the scarce resource.** Cost, latency, and quality all degrade as the
  window fills. Return references, not payloads.
- **Only the orchestrator gets `sessions_send`.** Give every agent delegation and
  you get loops; one delegator gives you one traceable call graph.
- **Negative instructions beat positive ones.** Telling an agent what it must *not*
  do prevents scope creep far more reliably than describing its job.
- **Run the orchestrator on a strong model and the workers on a cheap one.**
  Planning is the reasoning-heavy step; specialists execute a narrow spec.
- **Multi-agent architecture is a context-management and permission-separation
  technique, not an intelligence multiplier.** It made outputs more consistent, not
  more insightful.
- **Binding a bot to a channel is a security change, not just a UX change** — it
  converts a single-user tool into a networked service that anyone who finds it can
  drive. Allow-list users first.
