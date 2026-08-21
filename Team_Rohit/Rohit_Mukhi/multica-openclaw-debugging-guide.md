# Multica + OpenClaw Debugging Guide
## "openclaw returned no parseable output" — Root Causes & Fixes

---

## TL;DR — Root Causes (in order of discovery)

1. **OpenClaw CLI container could not reach the gateway** (timing issue)
2. **Groq free tier TPM limit exceeded** — 33,000 tokens sent vs 12,000 limit
3. **Decommissioned fallback model** — `groq/llama-3.1-70b-versatile` rejected by Groq
4. **Log lines written to stdout** — polluted the output Multica tried to parse
5. **Multica overrode `OPENCLAW_CONFIG_PATH`** to a minimal config with no `agents.list`, causing "Unknown agent id nova"
6. **File permission conflicts** — openclaw files owned by `root` instead of uid 1000

---

## System Architecture

```
User (Browser)
    │
    ▼
multica-frontend-1  (port 3000)
    │
    ▼
multica-backend-1   (port 8080)
    │
    ▼
multica-daemon-1    (multica-daemon:local image)
    │  invokes /usr/local/bin/openclaw binary (bundled inside daemon image)
    ▼
OpenClaw embedded agent
    │
    ▼
LLM Provider (Groq / OpenRouter)
```

**Key insight discovered during debugging:** Multica does NOT use the separate `openclaw-openclaw-gateway-1` and `openclaw-openclaw-cli-1` containers for agent tasks. It uses the OpenClaw binary bundled **inside** the `multica-daemon:local` image directly. The external openclaw containers are for Telegram/direct chat only.

---

## Issue 1 — OpenClaw CLI Container Not Reaching Gateway

### Symptom
```
Gateway: not reachable at ws://127.0.0.1:18789
```

### Root Cause
The `openclaw-openclaw-cli-1` container was starting before the gateway was fully healthy. Even though `depends_on` was configured, it only waits for the container to *start*, not for it to be *healthy*.

### Fix
Restarting the CLI container after the gateway was healthy:
```bash
docker restart openclaw-openclaw-cli-1
```

### Permanent Fix
Add `condition: service_healthy` to the CLI's `depends_on` in `openclaw/docker-compose.yml`.

---

## Issue 2 — Groq Free Tier TPM Limit Exceeded

### Symptom
```
413 Request too large for model `llama-3.3-70b-versatile`
Limit 12000, Requested 33152
```

### Root Cause
OpenClaw was injecting ~33,000 tokens per request into the LLM, broken down as:

| Source | Size |
|--------|------|
| Built-in tool schemas | 45,043 chars |
| System prompt (openclaw internal) | 16,093 chars |
| 15 global skills | 4,872 chars |
| Workspace files (SOUL, AGENTS, HEARTBEAT etc.) | ~2,600 chars |

Groq's free tier limits: 12,000 TPM for `llama-3.3-70b-versatile`, 6,000 TPM for `llama-3.1-8b-instant`.

### Fix — Reduce Tokens via Tool Deny List
Added a `tools.deny` list to nova's agent entry in `~/.openclaw/openclaw.json`:

```json
{
  "id": "nova",
  "workspace": "/home/node/.openclaw/workspace",
  "skills": [],
  "tools": {
    "deny": [
      "music_generate", "video_generate", "tts", "image_generate", "image",
      "canvas", "browser", "cron", "nodes", "sessions_spawn", "sessions_send",
      "sessions_list", "sessions_history", "sessions_yield", "session_status",
      "subagents", "pdf", "exec", "apply_patch", "process", "agents_list",
      "get_goal", "create_goal", "update_goal", "skill_workshop", "message",
      "read", "edit", "write", "file_fetch", "dir_list", "dir_fetch",
      "file_write", "node_inference", "gateway"
    ]
  }
}
```

Also added `"skills": []` to suppress global skill injection.

**Result:** Tokens reduced from **33,000 → ~3,500** (90% reduction).

### Key Principle
- `tools.deny` at the agent level only affects that specific agent
- It does NOT affect openclaw gateway, CLI, or other agents
- `skills: []` suppresses the 15 global openclaw skills from being injected

---

## Issue 3 — Decommissioned Fallback Model

### Symptom
```
400 The model `llama-3.1-70b-versatile` has been decommissioned
```

### Root Cause
`groq/llama-3.1-70b-versatile` was listed as a fallback in `openclaw.json` but had been deprecated by Groq.

### Fix
Removed from fallbacks in `~/.openclaw/openclaw.json`:

```json
"model": {
  "primary": "groq/llama-3.3-70b-versatile",
  "fallbacks": [
    "groq/llama-3.1-8b-instant",
    "openrouter/free"
  ]
}
```

Also removed from `agents.defaults.models` and `models.providers.groq.models`.

---

## Issue 4 — File Permission Conflicts (openclaw.json owned by root)

### Symptom
```
EACCES: permission denied, open '/home/node/.openclaw/openclaw.json'
Config file is not readable by the current process.
```

### Root Cause
Running `openclaw config set` inside `multica-daemon-1` caused the config file to be written as `root` (uid 0), while the openclaw gateway container runs as uid 1000 (node user).

### Fix
```bash
sudo chown -R 1000 ~/.openclaw
```

### Critical Rule
**NEVER run `openclaw config set` inside `multica-daemon-1`.** Always edit `~/.openclaw/openclaw.json` directly on the host. The daemon runs as root internally and will corrupt file ownership.

---

## Issue 5 — Version Mismatch Between Gateway and Config

### Symptom
```
Refusing to run automatic gateway startup migrations because this OpenClaw binary (2026.6.34)
is older than the config last written by OpenClaw 2026.7.1.
```

### Root Cause
The `multica-daemon-1` container has OpenClaw `2026.7.1` bundled, while the external `openclaw-openclaw-gateway-1` was running `2026.6.34`. After the daemon wrote to the config, the older gateway refused to start.

### Fix
Pull and update the openclaw containers:
```bash
cd ~/Agentic\ AI\ Programme/openclaw && docker compose pull && docker compose up -d
```

---

## Issue 6 — stdout Log Pollution Breaking Multica Output Parsing

### Symptom
```
openclaw returned no parseable output
```

### Root Cause
When Multica invokes openclaw, it reads stdout and tries to parse the agent's response. However, OpenClaw writes diagnostic log lines to **stdout** (not stderr), such as:

```
[agents/tool-policy] tool policy removed 24 tool(s) via agents.nova.tools.deny: ...
[provider-transport-fetch] [model-fetch] start provider=groq ...
[provider-transport-fetch] [model-fetch] response provider=groq ...
[agents/agent-command] [agent] run abc123 ended with stopReason=stop
```

These lines are mixed with the actual response text, making it unparseable by Multica.

### Attempted Fix (Config)
Adding `"logging": { "level": "silent" }` to `openclaw.json` — **did not work** for CLI stdout output, only affected file logging.

### Working Fix — Wrapper Script in Dockerfile
The `--log-level silent` CLI flag suppresses stdout logging. Since Multica controls how openclaw is invoked (via `MULTICA_OPENCLAW_PATH`), the fix is a wrapper script baked into the Docker image:

In `Dockerfile.daemon`:
```dockerfile
RUN mv /usr/local/bin/openclaw /usr/local/bin/openclaw-real && \
    printf '#!/bin/sh\nexport OPENCLAW_CONFIG_PATH=/home/node/.openclaw/openclaw.json\nexec /usr/local/bin/openclaw-real --log-level silent "$@"\n' \
      > /usr/local/bin/openclaw && \
    chmod +x /usr/local/bin/openclaw
```

---

## Issue 7 — Multica Overriding OPENCLAW_CONFIG_PATH (The Final Root Cause)

### Symptom
```
Error: Unknown agent id "nova". Use "openclaw agents list" to see configured agents.
```

### Root Cause — The Smoking Gun
This was the hardest issue to find. Multica sets the environment variable:

```
OPENCLAW_CONFIG_PATH=/home/node/multica_workspaces/<workspace_id>/<task_id>/openclaw-config.json
```

This `openclaw-config.json` is a **minimal task-specific config** generated by Multica containing only:

```json
{
  "agents": {
    "defaults": {
      "workspace": "/home/node/multica_workspaces/.../workdir"
    }
  },
  "mcp": {
    "servers": {
      "weather": {
        "args": ["-y", "open-meteo-mcp@latest"],
        "command": "npx"
      }
    }
  }
}
```

This config has **no `agents.list`**. When openclaw loads it, it sees no configured agents, so `--agent nova` results in "Unknown agent id nova".

### Why Manual Tests Always Worked
Every manual test we ran used the real config at `~/.openclaw/openclaw.json` (either via `OPENCLAW_CONFIG_PATH` env var being set correctly, or by default path resolution). Multica's override was only visible when catching the actual environment at invocation time.

### Fix
The wrapper script was updated to **restore `OPENCLAW_CONFIG_PATH`** before calling openclaw:

```dockerfile
RUN mv /usr/local/bin/openclaw /usr/local/bin/openclaw-real && \
    printf '#!/bin/sh\nexport OPENCLAW_CONFIG_PATH=/home/node/.openclaw/openclaw.json\nexec /usr/local/bin/openclaw-real --log-level silent "$@"\n' \
      > /usr/local/bin/openclaw && \
    chmod +x /usr/local/bin/openclaw
```

This ensures:
1. `OPENCLAW_CONFIG_PATH` always points to the real config with `agents.list`
2. `--log-level silent` suppresses stdout log noise

---

## Issue 8 — Wrong Model Passed as Agent ID

### Symptom
Daemon logs showed:
```
args="[agent --local --json --session-id multica-xxx --agent groq/llama-3.3-70b-versatile ...]"
```

### Root Cause
In Multica's agent settings, the **Model** field maps to the `--agent` flag in openclaw, not to the LLM model. Setting `MULTICA_OPENCLAW_MODEL=groq/llama-3.3-70b-versatile` caused Multica to pass `--agent groq/llama-3.3-70b-versatile`, which openclaw interpreted as an agent ID (not a model name).

### Fix
- Removed `MULTICA_OPENCLAW_MODEL` from `.env`
- Selected `nova` in Multica's agent Model dropdown — this correctly passes `--agent nova`
- The actual LLM model is controlled by `~/.openclaw/openclaw.json`

---

## Final Working Configuration

### ~/.openclaw/openclaw.json (key sections)
```json
{
  "logging": {
    "level": "silent"
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "groq/llama-3.3-70b-versatile",
        "fallbacks": [
          "groq/llama-3.1-8b-instant",
          "openrouter/free"
        ]
      }
    },
    "list": [
      {
        "id": "nova",
        "workspace": "/home/node/.openclaw/workspace",
        "skills": [],
        "tools": {
          "deny": [
            "music_generate", "video_generate", "tts", "image_generate",
            "image", "canvas", "browser", "cron", "nodes", "sessions_spawn",
            "sessions_send", "sessions_list", "sessions_history",
            "sessions_yield", "session_status", "subagents", "pdf", "exec",
            "apply_patch", "process", "agents_list", "get_goal", "create_goal",
            "update_goal", "skill_workshop", "message", "read", "edit",
            "write", "file_fetch", "dir_list", "dir_fetch", "file_write",
            "node_inference", "gateway"
          ]
        }
      }
    ]
  }
}
```

### Dockerfile.daemon (final)
```dockerfile
ARG OPENCLAW_IMAGE=openclaw/openclaw:latest
FROM ${OPENCLAW_IMAGE}
USER root
ARG MULTICA_VERSION=latest
RUN set -eux; \
    ARCH="$(uname -m)"; \
    case "$ARCH" in \
      x86_64)  ARCH="amd64" ;; \
      aarch64) ARCH="arm64" ;; \
      *) echo "Unsupported arch: $ARCH" && exit 1 ;; \
    esac; \
    if [ "$MULTICA_VERSION" = "latest" ]; then \
      MULTICA_VERSION="$(curl -fsSI https://github.com/multica-ai/multica/releases/latest \
        | grep -i '^location:' | sed 's/.*tag\///' | tr -d '\r\n')"; \
    fi; \
    VERSION_NUM="${MULTICA_VERSION#v}"; \
    curl -fsSL "https://github.com/multica-ai/multica/releases/download/${MULTICA_VERSION}/multica-cli-${VERSION_NUM}-linux-${ARCH}.tar.gz" \
      | tar -xz -C /usr/local/bin multica; \
    chmod +x /usr/local/bin/multica
RUN apt-get update -qq && apt-get install -y --no-install-recommends gosu && rm -rf /var/lib/apt/lists/*
RUN printf '#!/bin/sh\nchown -R node:node /home/node/.multica 2>/dev/null || true\nexec gosu node /usr/local/bin/daemon-entrypoint.sh\n' \
      > /usr/local/bin/daemon-init.sh && chmod +x /usr/local/bin/daemon-init.sh
COPY docker/daemon-entrypoint.sh /usr/local/bin/daemon-entrypoint.sh
RUN chmod +x /usr/local/bin/daemon-entrypoint.sh
# Wrap openclaw: restore correct config path and suppress stdout log noise
RUN mv /usr/local/bin/openclaw /usr/local/bin/openclaw-real && \
    printf '#!/bin/sh\nexport OPENCLAW_CONFIG_PATH=/home/node/.openclaw/openclaw.json\nexec /usr/local/bin/openclaw-real --log-level silent "$@"\n' \
      > /usr/local/bin/openclaw && chmod +x /usr/local/bin/openclaw
WORKDIR /home/node
RUN mkdir -p /home/node/multica_workspaces
ENTRYPOINT ["/usr/local/bin/daemon-init.sh"]
```

### Multica Agent Settings
- **Runtime:** OpenClaw · docker-daemon
- **Model (openclaw agent ID):** nova
- **Routing:** Local

---

## Lessons Learned

1. **Multica uses its own bundled OpenClaw**, not the external openclaw containers. External containers are for Telegram/direct chat.

2. **Never run `openclaw config set` inside `multica-daemon-1`** — it runs as root and corrupts file ownership, breaking the gateway.

3. **`OPENCLAW_CONFIG_PATH` is silently overridden by Multica** per task. Always restore it in the wrapper if you need agent-specific config.

4. **OpenClaw writes diagnostic logs to stdout**, not stderr. Any log noise mixed with the agent response causes Multica to fail with "no parseable output".

5. **The Model dropdown in Multica = `--agent` flag in openclaw**, not the LLM model. LLM model selection comes from `openclaw.json`.

6. **Token budgeting is critical on Groq free tier.** The `tools.deny` list and `skills: []` are the primary levers for reducing context size.

7. **Wrapper scripts in Dockerfile don't survive `docker compose up -d`** unless they are baked into the image build — always add them to `Dockerfile.daemon` as a `RUN` step.

8. **File ownership must be uid 1000** for all files under `~/.openclaw/` for the openclaw gateway container to read them.
