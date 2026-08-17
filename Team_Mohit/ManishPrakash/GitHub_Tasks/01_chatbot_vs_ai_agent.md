# Chatbot vs AI Agent

**Manish Prakash · Team Mohit**

---

## The distinction in one line

A **chatbot responds. An agent acts.**

A chatbot takes input and produces output. An agent takes a *goal*, decides what
steps to take, executes them against real systems, observes what happened, and
repeats until the goal is met or it gives up.

The difference is **not model quality**. The same model powers both. The difference
is architecture: **tools plus a loop.**

---

## What each one is

### Chatbot

```
User message → Model → Response
```

One turn in, one turn out. It may have conversation history and it may retrieve
documents, but it produces **text** and stops. The user does everything else.

Examples: a customer-support FAQ bot, a plain LLM chat window, a rule-based
website assistant.

### AI Agent

```
Goal → ┌─ Plan next step
       │  Call a tool
       │  Observe the result
       └─ Repeat until done
    → Outcome
```

The agent has **tools** (search, file access, shell, APIs, databases) and runs a
loop. Critically, its next action depends on the *result of its previous action* —
which is what makes it capable of multi-step work and also what makes it
unpredictable.

Examples: a coding agent that edits files and runs tests until they pass; a
research agent that searches, reads, and writes a report; the OpenClaw multi-agent
team in [`../30_July_2026/multi_agent_team.md`](../30_July_2026/multi_agent_team.md).

---

## Comparison

| Dimension | Chatbot | AI Agent |
|---|---|---|
| **Input** | A message | A goal |
| **Output** | Text | A changed state in the world |
| **Steps** | One turn | Many, decided at runtime |
| **Tools** | None, or one fixed retrieval step | Multiple, chosen by the model |
| **Control flow** | Fixed | Decided by the model, per step |
| **Memory** | Conversation history | History + working state + persistent memory |
| **Failure mode** | A wrong answer | A wrong *action* — possibly irreversible |
| **Cost per request** | One model call | Many model calls |
| **Latency** | Seconds | Seconds to minutes |
| **Predictability** | High | Low |
| **Testing** | Compare output to expected | Hard — non-deterministic path *and* result |
| **Human oversight** | Read the answer | Approve actions, review the trace |

---

## The three things that actually make an agent

1. **Tools.** Without the ability to affect something outside the conversation, it
   is a chatbot with a longer prompt.
2. **A loop.** One tool call and stop is a function call. Deciding what to do *next*
   based on what just happened is agency.
3. **Autonomy over control flow.** If a developer hardcoded the sequence, it is a
   workflow with an LLM inside it — useful, often preferable, but not an agent.

That third point separates agents from **LLM workflows**, which are frequently the
better engineering choice: a fixed pipeline with model calls at known points is
predictable, testable, and cheap. Reach for an agent only when the sequence of steps
genuinely cannot be known in advance.

---

## The spectrum

Real systems sit between the poles:

| | Behaviour |
|---|---|
| **Plain chatbot** | Text in, text out |
| **RAG chatbot** | Retrieves documents, then answers. One fixed extra step. |
| **Tool-using assistant** | Can call tools, but usually once per turn |
| **LLM workflow** | Fixed pipeline, model calls at defined stages |
| **Agent** | Chooses its own steps in a loop |
| **Multi-agent system** | Agents delegating to agents |

Moving down this list buys capability and costs predictability, money, and
reviewability. **Most production systems should stop earlier than their builders
want them to.**

---

## Why the difference matters practically

**Cost.** A chatbot is one model call. An agent solving a real task might make
twenty. Order-of-magnitude difference, not a marginal one.

**Risk.** A chatbot's worst case is a wrong sentence. An agent's worst case is a
deleted file, a posted message, or a spent budget. This is why the sandbox/VM
discipline runs through every document in this repository.

**Prompt injection.** A chatbot that reads a malicious document produces a bad
answer. An agent that reads the same document may *execute* what it says. Untrusted
input plus real capability is the dangerous combination, and it exists only on the
agent side.

**Testing.** Chatbot output can be compared against expectations. Agent behaviour
varies run to run — the same prompt takes different paths. Evaluation requires
fixed test scenarios and trace review, not assertions.

**Interface.** Agents are slow, which makes a blocking terminal feel broken and a
chat thread feel fine — the observation from
[`../30_July_2026/messaging_bot_integration.md`](../30_July_2026/messaging_bot_integration.md).

---

## When to use which

**Use a chatbot when:**
- The task is answering questions from known material.
- Latency and cost matter.
- You need predictable, reviewable behaviour.
- Nothing needs to change in the outside world.

**Use an agent when:**
- The task needs multiple steps that cannot be enumerated in advance.
- It requires acting on real systems.
- Success is verifiable by the agent itself — running tests, checking a build.
  Agents work far better with a signal they can check against.

**Use a fixed LLM workflow when** — and this is the underused middle — the steps
*are* known. You get the model's language ability with an ordinary program's
predictability. A large share of "we need an agent" requirements are actually this.

---

## Summary

- A chatbot **responds**; an agent **acts**. Tools and a loop, not a better model.
- Capability comes at the price of cost, latency, predictability, and safety.
- The middle ground — a fixed workflow containing LLM calls — is often the correct
  answer and is routinely skipped over.
- An agent's failure mode is a wrong *action*, which is why sandboxing, narrow tool
  permissions, and human approval on irreversible steps are not optional extras.
