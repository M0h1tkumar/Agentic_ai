# 5 — Experimenting with Microsoft recorder skills

**Manish Prakash · Team Mohit · 5 August 2026**

> **Status:** exploratory. Microsoft ships several things called a "recorder"; this
> covers the ones relevant to agent skills and what the recording paradigm is
> actually good for. Windows-only tooling, so parts were evaluated conceptually
> rather than run on my Linux setup — that is flagged where it applies.

---

## The idea

A **recorder** watches a human perform a task and produces a machine-executable
description of it. Instead of writing an automation, you do the job once and the
tool writes it down.

For agentic AI the appeal is obvious: **demonstration is a much lower-friction way
to specify a procedure than prose.** Writing a good `AGENTS.md` skill file is hard;
doing the task once is easy.

---

## The Microsoft tools in this space

| Tool | What it records | Output |
|---|---|---|
| **Power Automate Desktop — Recorder** | UI actions: clicks, typing, window and control targeting | A sequence of PAD actions you can edit and replay |
| **Steps Recorder (PSR)** | Clicks with screenshots and a text log | An MHTML report for humans (deprecated in recent Windows) |
| **Office Scripts Action Recorder** | Actions in Excel on the web | A TypeScript script |
| **Power Automate web recorder** | Browser interactions | Cloud-flow actions |

The one that matters for agent work is **Power Automate Desktop**, because its
output is executable and editable rather than a human-readable report.

---

## How the PAD recorder works

1. Open Power Automate Desktop, create a desktop flow, start the recorder.
2. Perform the task — open the app, click, type, save.
3. Stop. Each interaction becomes an action with a **UI element selector**.
4. Edit: parameterise hardcoded values, add conditions and error handling.
5. Replay.

**Selectors are the whole story.** The recorder captures how to find each control —
by automation ID, class, name, or position in the window tree. Robust selectors
(stable automation IDs) survive UI changes; positional ones break the moment a
button moves. Reviewing and tightening selectors after recording is not optional
polish, it is the actual work.

---

## Recorded flows as agent skills

The interesting question for this program is whether a recording can serve as a
skill an agent invokes. Two workable shapes:

**A. Agent calls the flow as a tool.** The recorded flow is a deterministic
procedure with named inputs. The agent decides *when* and *with what arguments*;
the flow handles *how*. Clean separation, and the reliable option — the model does
not touch the UI at all.

**B. Recording as documentation for a written skill.** Record the task, read the
generated action list, and use it as the source for a markdown skill file. The
recording tells you the exact steps, field names, and order; you write them up in
the form an agent can reason about. Slower, but the result is portable and legible.

**A is more reliable; B is more flexible.** I would use A for anything repeated
often and B when the procedure needs judgement at some step.

---

## Recording vs computer-use agents

Worth separating clearly, because they look similar and fail differently:

| | Recorded RPA flow | Vision-based computer-use agent |
|---|---|---|
| Mechanism | Replays captured selectors | Looks at the screen and decides |
| Determinism | High | Low |
| Handles UI changes | Poorly — selectors break | Better — it re-reads the screen |
| Handles novel situations | Not at all | Sometimes |
| Speed | Fast | Slow |
| Cost per run | Near zero | A model call per step |
| Auditability | Every step is visible in the flow | Reasoning is opaque |

**The right architecture uses both:** the model decides *what* to do and supplies
the parameters; the recorded flow does *how*, deterministically and cheaply. Using a
model to click through a fixed five-step form is expensive, slow, and less reliable
than a recording — and using a recording for anything that varies is brittle.

---

## Limitations

- **Windows-centric.** PAD is a Windows desktop product. On Linux the equivalents
  are different tools entirely.
- **Selector fragility.** The dominant maintenance cost of all RPA.
- **Records the happy path only.** Error handling, timeouts, and unexpected dialogs
  are all manual additions afterwards.
- **Captures actions, not intent.** The recording knows you clicked a button; it
  does not know why, or what to do if the button is absent.
- **Secrets get recorded.** Typing a password during a recording puts it in the
  flow. Use the credential store, and review every recording before sharing it.
- **Licensing.** Attended/unattended desktop flows have real Power Platform
  licensing implications at scale.

---

## Takeaways

1. **Demonstration is an underrated specification method.** For a fixed procedure
   it is faster and more accurate than writing instructions.
2. **A recording is a first draft, not a finished automation.** Selector review,
   parameterisation, and error handling are where the reliability comes from.
3. **The hybrid is the point.** Model for judgement, recording for execution.
   Neither paradigm is a replacement for the other, and the boundary between them
   is where good design happens.
4. **Recordings capture whatever was on screen**, including credentials. Treat them
   as sensitive artifacts.
