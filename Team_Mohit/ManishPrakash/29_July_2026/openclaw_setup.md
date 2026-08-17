# OpenClaw — installation, setup and onboarding

**Manish Prakash · Team Mohit · 29 July 2026**

> **Status:** written as a working reference from the program material and the
> OpenClaw configuration schema. Commands and config shapes below are the ones I
> use; anything I have not personally verified end-to-end is marked *(unverified)*.

---

## 1. What OpenClaw is

An open-source **AI agent runtime / gateway**. It is not an editor plugin and not a
chat app — it is a long-running Node.js service that:

- hosts one or more **agents**, each with its own workspace, model, and tool policy;
- exposes a **web UI** (default port `18789`) and a CLI (`openclaw`);
- binds agents to **channels** — Telegram, Discord, Slack — so a conversation in a
  messaging app drives an agent;
- lets agents talk to each other via `sessions_send`, which is what makes
  multi-agent teams possible;
- is invoked by other systems (Multica's daemon, for instance) as the thing that
  actually executes an AI task.

The mental model that made it click for me: **OpenClaw is to agents what systemd is
to daemons.** It is the supervisor and the config surface, not the work itself.

---

## 2. Prerequisites

| Requirement | Notes |
|---|---|
| Node.js (LTS) | The gateway is a Node service |
| Git | For cloning |
| A model provider key | Anthropic / OpenRouter / local endpoint |
| Linux, macOS, or WSL | Native Windows is the least-travelled path |
| **A VM or container** | Strongly recommended — see §7 |

---

## 3. Install

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
npm install
npm run build
npm link          # puts `openclaw` on PATH
openclaw --version
```

Docker is the alternative and is preferable if you want isolation without a full VM:

```bash
docker run -d --name openclaw \
  -p 18789:18789 \
  -v ~/.openclaw:/root/.openclaw \
  openclaw/openclaw:latest
```

Note the volume mount: **all state lives in `~/.openclaw`**. Mount it or you lose
your agents on every container restart.

---

## 4. Onboarding

```bash
openclaw onboard
```

The wizard walks through, in order:

1. **Model provider and credentials** — written to the config, not to your shell
   profile.
2. **Default model** — I use a fast/cheap model as the default and override
   per-agent where reasoning quality matters.
3. **Workspace directory** — the agent's working root. Treat this as a sandbox
   boundary; do not point it at `$HOME`.
4. **Tool permissions** — which tools the agent may call.
5. **Channel bindings** — optional at this stage.

Everything it writes lands in `~/.openclaw/openclaw.json`, which you can and
should edit by hand afterwards.

---

## 5. Configuration structure

The single most useful thing to understand up front, because it is where the
first error usually appears:

```jsonc
{
  "agents": {
    "defaults": {
      "model": { "primary": "anthropic/claude-haiku-4-5" }
    },
    "list": [
      {
        "id": "atlas",
        "workspace": "/home/manish/.openclaw/workspace-atlas",
        "model": "anthropic/claude-haiku-4-5",
        "tools": { "allow": ["read", "write", "bash", "sessions_send"] }
      }
    ]
  },
  "channels": {
    "telegram": { "token": "..." }
  },
  "bindings": [
    { "agent": "atlas", "channel": "telegram" }
  ]
}
```

**Three things that trip people up:**

1. `bindings` is a **root-level array**, not a per-agent field. Putting it inside an
   agent object produces `agents.list.0: Invalid input`, which is an unhelpfully
   generic message for the actual mistake.
2. `channels` is also **root-level**. Bot tokens go there, not on the agent.
3. `workspace` must be an **absolute path**. Relative paths and `~` are not expanded.

---

## 6. Agent identity files

Inside each workspace, three files define who the agent is:

| File | Purpose |
|---|---|
| `SOUL.md` | Persona, tone, values. *Who* the agent is. |
| `AGENTS.md` | Operating instructions, constraints, what it may and may not do. *How* it works. |
| `memory.md` | Persistent notes carried between sessions. |

Plus a `skills/` directory of markdown files — each one a reusable procedure the
agent can follow.

This is the part worth spending real time on. Model choice matters less than most
people assume; **`AGENTS.md` quality matters more than most people assume.** A vague
`AGENTS.md` produces a vague agent regardless of which model is behind it.

---

## 7. Security posture — read before running

OpenClaw agents run shell commands with your user's privileges and read from
channels that other people can write to. That is a genuinely powerful combination
and deserves deliberate handling:

- **Run it in a VM or container.** This is the concrete reason the master task list
  has a sandbox item. Blast-radius control, not paranoia.
- **Narrow the workspace.** A dedicated directory, never `$HOME` or `/`.
- **Allow-list tools per agent.** An agent that only drafts text does not need `bash`.
- **Treat inbound channel messages as untrusted.** A Telegram bot is a public input
  to a system that can run commands — that is a prompt-injection surface by
  construction.
- **Keep provider keys scoped and rotatable.** See
  [`oauth_vs_api_key.md`](oauth_vs_api_key.md); a static key inside an autonomous
  agent is exactly the risk profile described there.
- **Audit skills before installing them.** Same discipline as the Skill Spector task.

---

## 8. Verifying the install

```bash
openclaw --version          # binary on PATH
openclaw config validate    # schema check before starting (unverified)
openclaw gateway start      # start the service
```

Then open `http://localhost:18789` and confirm the agent appears and responds. If
running under systemd as a user service, `journalctl --user -u openclaw -f` is where
the real errors are — the web UI tends to show a generic failure.

---

## 9. What I took away

- The config schema is strict and its error messages are not. Read the shape
  carefully; most setup failures are structural JSON mistakes, not real problems.
- **All state is in `~/.openclaw`.** Back it up; mount it in Docker.
- The identity files are the actual product of the setup work. The install is
  twenty minutes; writing a good `AGENTS.md` is the rest of the day.
- Autonomous execution plus a public messaging channel is a serious security
  posture. Sandbox first, then experiment.
