# Developing agents in Visual Studio / VS Code Copilot — positives and negatives

**Manish Prakash · Team Mohit · 29 July 2026**

---

## 1. What "agent" means here

GitHub Copilot has moved through three distinct modes, and the differences matter
for this evaluation:

| Mode | Behaviour |
|---|---|
| **Completion** | Inline ghost-text suggestions as you type. The original Copilot. |
| **Chat / Edits** | Conversational; can apply multi-file edits you review before accepting. |
| **Agent mode** | Given a goal, it plans, edits multiple files, runs terminal commands and tests, reads the output, and iterates until done or stuck. |

This document is about **agent mode** — where Copilot acts autonomously — and about
using the VS Code / Visual Studio environment as the place to *build* agentic
workflows.

---

## 2. Positives

### 2.1 Zero-setup context
The editor already knows the open file, the selection, the workspace tree, the
symbol index, the git diff, and the terminal output. An agent built anywhere else
has to reconstruct all of that. This is the biggest single advantage and it is
structural, not incidental.

### 2.2 Tight feedback loop
Agent mode can run the build, read the compiler error, patch the file, and re-run
without leaving the editor. Error output feeds straight back into the next step.
That loop is where most of the real value is.

### 2.3 Diff-based review before commit
Every change lands as a reviewable diff with accept/reject per hunk. The human stays
the gate. Compare this with a CLI agent writing files directly — the editor's diff
UI is a genuine safety feature, not just convenience.

### 2.4 Multi-model choice
Recent versions let you pick the backing model per request (Claude, GPT, Gemini
families). You can route cheap mechanical edits to a fast model and hard reasoning
to a stronger one, in the same session.

### 2.5 MCP support
VS Code's Copilot supports MCP servers, so the agent can reach databases, issue
trackers, and internal APIs through the same standard protocol discussed in
[`../06_August_2026/api_vs_mcp.md`](../06_August_2026/api_vs_mcp.md). This turns the
editor into a general agent host, not just a code assistant.

### 2.6 Custom instructions and prompt files
`.github/copilot-instructions.md` lets you commit project conventions — style rules,
architectural constraints, "always use X" — into the repo so every developer's agent
inherits the same context. Reusable prompt files cover repeated tasks.

### 2.7 Low adoption friction
The team already has the editor, the extension, and often the licence. Compared to
standing up a custom agent stack, time-to-first-useful-result is minutes.

### 2.8 Enterprise plumbing exists
SSO, policy controls, audit logging, IP indemnification, and a documented option to
exclude your code from training. For an organisation, that paperwork matters as
much as the model quality.

---

## 3. Negatives

### 3.1 Context window is still the hard ceiling
The agent sees a fraction of a large repo. It will confidently reimplement a helper
that already exists three directories away, or miss a caller it needed to update.
Retrieval helps; it does not eliminate the problem.

### 3.2 Confident wrong answers
Plausible, well-formatted, wrong. Hallucinated method names, invented config keys,
APIs that existed two major versions ago. The output *looks* reviewed, which makes
under-reviewing tempting — the failure mode is social as much as technical.

### 3.3 Autonomous terminal execution is a real risk
Agent mode runs shell commands. Auto-approve is a genuinely dangerous setting on a
machine with credentials, cloud sessions, or a production kubeconfig. This is the
concrete argument for the "sandbox / VM" item on the master task list — do agentic
work in a VM or container, not on your primary machine.

### 3.4 It suggests insecure code
String-concatenated SQL, missing input validation, disabled TLS verification,
hard-coded secrets, weak crypto defaults, and unsanitised shell interpolation. The
model reproduces patterns common in its training data, and insecure patterns are
extremely common in public code. This is worse than an ordinary bug because it looks
idiomatic — the reviewer's eye slides over it. Committing security rules to
`.github/copilot-instructions.md` helps; reviewing generated code specifically for
injection sinks helps more.

### 3.5 Prompt injection through repo content
An agent that reads files, issues, or dependency READMEs can read attacker-authored
text. If it also has terminal access, that is an exploitable path. Untrusted content
plus autonomous capability is the dangerous combination.

### 3.6 Vendor lock-in and opacity
The orchestration layer is closed. You cannot fully inspect or replace how it plans,
retrieves, or truncates context. When it behaves oddly, you tune prompts and guess.
An open framework gives worse defaults and better control.

### 3.7 Cost and quota unpredictability
Agent runs consume far more tokens than completions — many model calls per task.
Premium-request quotas are easy to burn through in an afternoon of heavy use, and
per-seat pricing does not track actual consumption well.

### 3.8 Cloud dependency
No connectivity, no agent. Air-gapped or strictly regulated environments are largely
excluded. Local models via Ollama/LM Studio are the alternative, at a real capability cost.

### 3.9 Non-determinism
The same prompt produces different code on different runs. This is uncomfortable for
reproducible builds, code review norms, and debugging "it worked yesterday."

### 3.10 Weak on genuinely novel architecture
Strong on boilerplate, tests, refactors, and idiomatic patterns it has seen many
times. Weak on the design decisions that actually need a senior engineer. It
accelerates the easy 80% and can mislead on the hard 20%.

### 3.11 Skill atrophy and review fatigue
Reviewing generated code is harder than reviewing a colleague's — there is no author
to ask "why?", and the volume is higher. Over months, juniors risk shipping code they
could not have written or debugged themselves.

### 3.12 Licensing ambiguity
Suggestions can resemble training data. Filters for public-code matches exist and
help, but attribution and licence provenance remain unresolved in the general case.

### 3.13 Visual Studio vs VS Code parity
Feature rollout is not simultaneous. VS Code and the Insiders build generally get
agent features first; full Visual Studio lags. Worth checking before planning around
a specific capability.

---

## 4. Balance sheet

| | Positive | Negative |
|---|---|---|
| **Context** | Editor state for free | Bounded window on large repos |
| **Speed** | Fast build-fix-run loop | Non-deterministic output |
| **Safety** | Diff review before accept | Autonomous terminal execution |
| **Flexibility** | Multi-model, MCP support | Closed orchestration layer |
| **Adoption** | Already installed | Cloud-only, quota-limited |
| **Team** | Committed instructions file | Review fatigue, skill atrophy |

---

## 5. Recommendation

1. **Use it — with the human as the gate.** Never enable blanket auto-approve for
   terminal commands.
2. **Do agentic work in a VM or container.** Blast-radius control beats trust.
3. **Commit `.github/copilot-instructions.md`.** Cheap, and it fixes a large share
   of "why did it write it that way" complaints.
4. **Match task to model.** Mechanical edits to a fast model; architecture to a
   strong one.
5. **Review generated code harder than human code**, not softer. It reads more
   confidently than it deserves.
6. **Keep an escape hatch.** Use MCP and open standards where possible so the
   integration work survives a change of vendor.

**Verdict:** excellent as an accelerator inside a disciplined workflow; dangerous as
an unsupervised autonomous developer. The positives are real and immediate; the
negatives are all manageable by policy rather than by hoping the model improves.
