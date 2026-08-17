# 4 — Experimenting with OpenCode

**Manish Prakash · Team Mohit · 5 August 2026**

*(Task note: "best for runtime.")*

---

## What OpenCode is

An **open-source terminal-based AI coding agent** — a TUI that lives in your
terminal, reads and edits your repository, runs commands, and iterates on the
results. Same category as Claude Code and Aider; the distinguishing property is
that it is **provider-agnostic and open source**, so you choose the model behind it.

Install (Go/Node binary, distributed the usual ways):

```bash
curl -fsSL https://opencode.ai/install | bash
# or: npm i -g opencode-ai
opencode
```

Run it from inside a git repository. That is not a suggestion — see §4.

---

## Why "best for runtime"

Reading it as *execution speed and iteration loop*, the claim holds up, for
identifiable reasons:

1. **No editor in the loop.** No extension host, no language server contention, no
   UI thread. The agent reads files and runs commands directly.
2. **The terminal is already where builds and tests live.** The agent runs `pytest`,
   reads the failure, patches, re-runs — without the round trip through an editor's
   task system.
3. **Streaming TUI.** You see tool calls as they happen and can interrupt
   immediately, which matters more than raw speed. Catching a wrong direction at
   second three beats waiting for a wrong answer at second ninety.
4. **Model choice per task.** A cheap fast model for mechanical edits; a strong one
   for design work. See [`../03_August_2026/omniroute_notes.md`](../03_August_2026/omniroute_notes.md)
   — a router in front makes this a config change.
5. **Runs over SSH.** Works on a remote build box, in a VM, or in a container with
   the real toolchain. GUI tools do not.

That last point is the one that matters most for this program: **it is the natural
fit for the sandbox/VM task.** You can put the agent where the code and the risk
are, rather than on your laptop.

---

## Comparison with the alternatives

| | OpenCode | Copilot agent mode | Claude Code |
|---|---|---|---|
| Interface | Terminal TUI | Inside the editor | Terminal / IDE / web |
| Model | Your choice, any provider | Selectable from a fixed set | Claude family |
| Source | Open | Closed | Closed |
| Works over SSH | Yes | Awkward | Yes |
| Diff review UI | Terminal diffs | Rich editor diffs | Terminal + IDE diffs |
| Best at | Fast build-fix-run loops | Edits with editor context | Broad agentic work |

**Honest read:** for tight iteration against a test suite, the terminal agents win
on loop speed. For editing code you are actively reading, the editor integration
from [`../29_July_2026/copilot_agent_development.md`](../29_July_2026/copilot_agent_development.md)
is genuinely better — the free context and the per-hunk diff review are hard to
match in a TUI.

They are complementary, and using both is not a contradiction.

---

## What actually worked

**Give it a verification command.** The single biggest quality difference. "Fix the
failing test" with a runnable `pytest -x` produces a real fix; "improve this code"
produces plausible churn. The agent needs a signal it can check itself against.

**Commit before you start.** The undo mechanism is git. No commit, no undo.

**Small scoped tasks.** "Add error handling to this module" beats "refactor the
project." Large tasks exhaust context and the agent starts contradicting its own
earlier edits — the context lesson from
[`../30_July_2026/sessions_1_and_2_notes.md`](../30_July_2026/sessions_1_and_2_notes.md)
showing up in a concrete tool.

**Read the tool calls as they stream.** Interrupting early is cheap; reviewing a
large wrong diff afterwards is not.

**Project instructions file.** Committing conventions to the repo means the agent
stops re-litigating style on every run.

---

## What went wrong

| Problem | Fix |
|---|---|
| Edited files outside the intended scope | Narrow the prompt; work on a branch |
| Confidently invented a library API | Give it the docs, or a failing test to satisfy |
| Context exhausted mid-task | Split the task; start a fresh session per unit |
| Repeated a failing fix in a loop | Interrupt and give a different framing — it will not break out on its own |
| Cost higher than expected | Cheap model by default, strong model only when needed |

The failing-fix loop is worth flagging: **an agent that has decided on a wrong
approach will keep trying variants of it.** Re-running does not help. Re-framing
does.

---

## Security

Same posture as everywhere else in these notes, and more urgent because the tool
runs shell commands by design:

- **Run it in a VM or container.** Explicitly the sandbox task.
- **Do not enable blanket auto-approve** for commands.
- **Never point it at a repository you have not read**, and be aware that any file
  it reads — including dependency READMEs — is a prompt-injection surface.
- **Keep provider keys scoped**, with spend caps.

---

## Verdict

Genuinely good at the tight loop: change → run → read failure → change again. That
loop is where most engineering time actually goes, and compressing it is real value.

Open source and provider-agnostic matter more than they look. You can run it against
a local model in an air-gapped VM — an option no closed cloud tool offers.

**Where I would use it:** test-driven fixes, mechanical refactors, working on remote
machines, and anywhere the code should not leave a controlled environment.

**Where I would not:** exploratory design work, and any repository I have not read
and do not trust.
