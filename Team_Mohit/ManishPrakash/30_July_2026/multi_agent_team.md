# OpenClaw multi-agent team — tasks 1 to 9

**Manish Prakash · Team Mohit · 30 July 2026**

> **Status:** working notes from building the team. Config shapes reflect the
> OpenClaw schema described in [`../29_July_2026/openclaw_setup.md`](../29_July_2026/openclaw_setup.md).

---

## The goal

Turn a single agent bound to one channel into a **team of specialist agents with an
orchestrator that delegates to them.** The interesting engineering is not creating
four agents — it is making delegation work, and knowing when it is worth it.

My team (a research/reporting team, chosen because it produces verifiable output):

| Agent | Role | Tools |
|---|---|---|
| **Atlas** | Orchestrator — receives requests, plans, delegates, assembles the answer | `sessions_send`, `read`, `write` |
| **Vega** | Research — gathers and summarises source material | `read`, `write`, `webfetch` |
| **Orion** | Analysis — turns research into structured findings | `read`, `write` |
| **Lyra** | Editor — fact-checks, tightens, formats the final deliverable | `read`, `write` |

Only Atlas gets `sessions_send`. That is deliberate: one delegator means one
traceable call graph. Give everyone delegation and you get loops.

---

## Step 1 — Workspace layout

Each agent needs an isolated workspace plus one shared directory for context that
everybody must agree on.

```bash
for a in atlas vega orion lyra; do
  mkdir -p ~/.openclaw/workspace-$a/skills
done
mkdir -p ~/.openclaw/workspace-vega/research
mkdir -p ~/.openclaw/workspace-orion/analysis
mkdir -p ~/.openclaw/workspace-lyra/drafts
mkdir -p ~/.openclaw/shared
```

**Why isolate?** So one agent cannot quietly overwrite another's working files, and
so each agent's file listing stays small enough to be useful context.

**Why share one directory?** Project brief, glossary, and standing constraints must
be identical for everyone. Duplicating them guarantees they drift.

## Step 2 — Identity files

For each agent, three files:

- `SOUL.md` — persona and voice.
- `AGENTS.md` — operating rules. The important one.
- `memory.md` — persistent notes across sessions.

Vega's `AGENTS.md`, abbreviated, to show the shape that actually worked:

```markdown
# Vega — Research Agent

## Role
You gather source material. You do not analyse it and you do not write
the final deliverable. Those are Orion's and Lyra's jobs.

## Output contract
Write findings to `research/<topic>.md` with, for every claim:
  - the claim, in one sentence
  - the source URL
  - a confidence marker: [confirmed] / [single-source] / [uncertain]

## Rules
- Never state a claim you cannot attribute. Say "not found" instead.
- Stop at 8 sources. More is not better; it is just longer.
- Reply to the delegator with the file path and a 3-line summary. Not the
  full contents.
```

Three things made these work:

1. **A negative section.** Saying what the agent must *not* do prevents scope creep
   far more reliably than describing what it should do.
2. **An explicit output contract.** If the format is unspecified, every run differs
   and the next agent in the chain cannot parse it.
3. **"Return a path, not a payload."** Delegating agents that reply with full
   documents blow up the orchestrator's context window within a few hops. This was
   the single biggest practical improvement.

## Step 3 — Shared context

`~/.openclaw/shared/project-context.md` — the brief, the audience, the tone, the
hard constraints. `~/.openclaw/shared/team-log.md` — an append-only record of what
each agent did, so a later session can reconstruct why something exists.

## Step 4 — Skills

Skills are markdown procedures in each agent's `skills/` directory.

- Atlas: `delegation.md` — when to delegate versus answer directly.
- Vega: `source-evaluation.md` — how to rank source credibility.
- Orion: `structured-analysis.md` — the required findings format.
- Lyra: `style-guide.md` and `fact-check.md`.

A skill is more reusable than the same text pasted into `AGENTS.md`, and it keeps
the identity file short enough to stay in context.

## Step 5 — Configuration

```jsonc
{
  "agents": {
    "defaults": { "model": { "primary": "anthropic/claude-haiku-4-5" } },
    "list": [
      {
        "id": "atlas",
        "workspace": "/home/manish/.openclaw/workspace-atlas",
        "model": "anthropic/claude-sonnet-5",
        "tools": { "allow": ["read", "write", "sessions_send"] }
      },
      {
        "id": "vega",
        "workspace": "/home/manish/.openclaw/workspace-vega",
        "tools": { "allow": ["read", "write", "webfetch"] }
      },
      {
        "id": "orion",
        "workspace": "/home/manish/.openclaw/workspace-orion",
        "tools": { "allow": ["read", "write"] }
      },
      {
        "id": "lyra",
        "workspace": "/home/manish/.openclaw/workspace-lyra",
        "tools": { "allow": ["read", "write"] }
      }
    ]
  },
  "channels": { "telegram": { "token": "<from BotFather>" } },
  "bindings": [ { "agent": "atlas", "channel": "telegram" } ]
}
```

**Reminder from the previous day:** `channels` and `bindings` are **root-level**.
Nesting them inside an agent yields `agents.list.0: Invalid input`.

Note Atlas runs a stronger model than the workers. Planning and delegation are the
reasoning-heavy steps; the specialists execute a narrow, well-specified job and a
cheaper model handles that fine. This materially cut cost per task.

## Step 6 — Delegation

Atlas calls `sessions_send` with a target agent and a message. Its `delegation.md`
skill encodes the policy:

```markdown
## When to delegate
- Needs external sources          → vega
- Needs structured reasoning      → orion
- Needs polish or fact-checking   → lyra
- Answerable in under 3 sentences → answer directly, do NOT delegate

## How to delegate
State the deliverable, the constraints, and where to write the output.
Never forward the user's raw message — translate it into a task.

## After delegating
Read the file the agent produced. Do not trust the summary alone.
```

That last line came from experience: an agent reporting "done" is not evidence the
output is good.

## Step 7 — Channel binding

Telegram via BotFather, token into `channels.telegram.token`, `bindings` maps
Telegram to Atlas only. Users talk to one agent; the team is an implementation
detail they never see. This is the right interface — exposing four bots to the user
just relocates the orchestration problem onto them.

## Step 8 — Test run

Prompt: *"Compare the top 3 model fine-tuning tools and recommend one for a team
with a single consumer GPU."*

Observed trace: Atlas plans → Vega researches, writes `research/finetuning-tools.md`
→ Orion reads it, writes structured comparison → Lyra edits → Atlas returns the
summary to Telegram.

The output of that run became the basis for
[`../GitHub_Tasks/04_model_training_tools.md`](../GitHub_Tasks/04_model_training_tools.md),
verified by hand before committing.

## Step 9 — What broke, and the fixes

| Problem | Cause | Fix |
|---|---|---|
| `agents.list.0: Invalid input` | `bindings` nested inside an agent | Move `bindings` and `channels` to root |
| Agent could not find its workspace | Used `~` in the path | Absolute paths only; `~` is not expanded |
| Orchestrator context exhausted after ~4 hops | Workers returned full documents | "Return a path, not a payload" in every `AGENTS.md` |
| Agents ignored shared context | Nothing told them to read it | Explicit "read `shared/project-context.md` first" in each `AGENTS.md` |
| Delegation loop (A→B→A) | Multiple agents had `sessions_send` | Only the orchestrator gets it |
| Inconsistent output format | No format specified | Explicit output contract per agent |
| Cost higher than expected | Every agent on the strong model | Strong model for the orchestrator, cheap for workers |

---

## Honest assessment: is a multi-agent team worth it?

**Yes, when:**
- The subtasks genuinely need different tools or different permissions.
- Specialisation improves quality — a dedicated editor really does produce cleaner
  output than "and also proofread it" appended to one prompt.
- You want separate context windows so a long research phase does not crowd out the
  writing phase.

**No, when:**
- One agent with a good prompt would do. Most tasks are in this category.
- Latency matters — every hop is a full model round trip.
- You have not yet defined output contracts. Without them a multi-agent team is
  just a slower, more expensive single agent with more failure modes.

The honest summary: **multi-agent architecture is a context-management and
permission-separation technique, not an intelligence multiplier.** It made my
outputs more consistent, not more insightful. Knowing that is the real lesson from
this task.
