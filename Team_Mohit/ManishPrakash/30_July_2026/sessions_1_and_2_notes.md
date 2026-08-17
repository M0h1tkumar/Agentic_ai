# Sessions 1 and 2 — notes

**Manish Prakash · Team Mohit · 30 July 2026**

> **Status:** consolidated notes from working through the two session files provided
> by the instructors, written in my own words with my own conclusions. The session
> materials themselves are not reproduced here.

---

## Session 1 — foundations

### What an agent actually is

The definition that survived contact with practice: **an agent is an LLM in a loop
with tools and a goal.** Strip away the framework vocabulary and every agent is:

```
while not done:
    decide what to do next      (model call)
    do it                       (tool call)
    observe the result          (feed back into context)
```

Everything else — orchestration, memory, planning modules — is machinery around
that loop. This matters because it tells you where things break: the loop fails
when the model decides badly, when the tool fails, or when the observation does not
fit back into context.

### Chatbot vs agent

Covered in full in [`../GitHub_Tasks/01_chatbot_vs_ai_agent.md`](../GitHub_Tasks/01_chatbot_vs_ai_agent.md).
The one-line version: a chatbot **responds**; an agent **acts**. The difference is
tools and a loop, not model quality.

### The four components

| Component | Role | Where it goes wrong |
|---|---|---|
| **Model** | Decides | Hallucinates a plan; picks the wrong tool |
| **Tools** | Acts | Fails silently; returns unparseable output |
| **Memory** | Persists | Grows until it crowds out the task |
| **Loop** | Continues | Never terminates; repeats a failing step |

The failure column is the useful half of this table. Most agent debugging is
identifying which of these four is at fault, and it is usually the loop or memory,
not the model.

### Prompt as specification

The system prompt is not decoration. It is the agent's spec: role, constraints,
output format, and — critically — what it must *not* do. Negative constraints
turned out to be far more effective than positive descriptions, a lesson that
repeated in the multi-agent task.

---

## Session 2 — building and running

### Context is the scarce resource

Everything expensive about agents traces back to context: cost is tokens, latency is
tokens, and quality degrades as the window fills with irrelevant history. The
practical consequences:

- **Summarise long tool outputs** before feeding them back.
- **Return references, not payloads** — a file path beats a file's contents.
- **Reset sessions between unrelated tasks** rather than letting one thread sprawl.

This single idea explains most of the architectural choices in the rest of these
notes, including why multi-agent teams help at all.

### Tool design matters more than expected

A tool the model cannot use correctly is worse than no tool — it produces confident
wrong actions. What makes a tool usable by a model:

- A name that says what it does.
- A description written for a model: *when* to use it, not just what it takes.
- A narrow, obvious parameter set.
- Errors that explain how to fix the call, not just that it failed.

This is precisely the argument MCP formalises — see
[`../06_August_2026/api_vs_mcp.md`](../06_August_2026/api_vs_mcp.md), §5.3.

### The human in the loop

Full autonomy is rarely the right target. The useful spectrum:

| Level | Behaviour | Use for |
|---|---|---|
| Suggest | Proposes, human executes | Anything destructive |
| Approve | Executes after per-action approval | Writes, deploys, external sends |
| Notify | Executes, reports afterwards | Reversible internal work |
| Autonomous | Runs unattended | Narrow, well-tested, sandboxed loops |

Choosing the level per *tool* rather than per *agent* worked better in practice —
read freely, ask before writing.

### Evaluation

Non-determinism means "it worked when I tried it" is not evidence. The minimum
viable discipline: a fixed set of test prompts, run after every prompt change, with
outputs eyeballed side by side. Crude, but it catches regressions that otherwise
surface a week later in front of someone else.

---

## Overall takeaways

1. **An agent is a loop, tools, and a goal.** The rest is packaging.
2. **Context is the budget.** Design for it explicitly or it will design your system
   for you.
3. **Tool descriptions are model-facing documentation** and deserve the care of an
   API contract.
4. **Constrain by default.** Narrow tools, negative instructions, human approval on
   anything irreversible.
5. **Non-determinism is the defining engineering difficulty.** It breaks testing,
   debugging, and reproducibility all at once, and no amount of model improvement
   removes it.
