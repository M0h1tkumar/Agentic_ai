# Multica + OpenClaw Docker Setup — Complete Architecture & Implementation Guide

This document is a complete reference for any AI model (Claude, Gemini, GPT, etc.) to understand, reproduce, debug, or extend the containerised self-hosted setup of **Multica** (AI project management platform) and **OpenClaw** (AI agent runtime) running as separate Docker stacks that communicate over a shared Docker network.

---

## Table of Contents

1. [What These Projects Are](#1-what-these-projects-are)
2. [Full Architecture](#2-full-architecture)
3. [Files Changed or Created](#3-files-changed-or-created)
4. [Step-by-Step: What Was Done and Why](#4-step-by-step-what-was-done-and-why)
5. [Errors Encountered and How They Were Fixed](#5-errors-encountered-and-how-they-were-fixed)
6. [How the Two Stacks Connect](#6-how-the-two-stacks-connect)
7. [The Daemon: How It Works](#7-the-daemon-how-it-works)
8. [Login / OTP Problem and Fix](#8-login--otp-problem-and-fix)
9. [Control Scripts](#9-control-scripts)
10. [Daily Workflow](#10-daily-workflow)
11. [Key Design Decisions](#11-key-design-decisions)
12. [Environment Variables Reference](#12-environment-variables-reference)

---

## 1. What These Projects Are

### Multica
- A self-hosted AI-powered project management platform (like Linear with AI agents)
- Stack: Go backend API, Next.js frontend, PostgreSQL with pgvector
- Users create issues and assign them to AI agents; agents execute tasks autonomously
- Requires a **daemon** — a process that polls the backend for tasks and spawns AI agent CLIs to execute them
- Official images: `ghcr.io/multica-ai/multica-backend` and `ghcr.io/multica-ai/multica-web`
- Source: `/home/master/Agentic AI Programme/multica/`

### OpenClaw
- An open-source AI agent runtime / gateway
- Runs as a Node.js gateway server that manages AI agent sessions
- Has its own web UI at port 18789
- The `openclaw` binary is the CLI that multica's daemon uses to execute AI tasks
- Official image: `openclaw/openclaw:latest`
- Source: `/home/master/Agentic AI Programme/openclaw/`

---

## 2. Full Architecture

```
HOST MACHINE (Linux)
│
├── Docker Network: agent-network (external bridge, shared between stacks)
│
├── MULTICA STACK (docker-compose.yml in multica/)
│   │
│   ├── multica-postgres-1
│   │     image: pgvector/pgvector:pg17
│   │     networks: internal (only)
│   │     port: NOT exposed to host or agent-network
│   │     purpose: primary database with vector extension
│   │
│   ├── multica-backend-1
│   │     image: ghcr.io/multica-ai/multica-backend:latest
│   │     networks: internal + agent-network
│   │     port: 127.0.0.1:8080 → container:8080
│   │     purpose: Go REST API + WebSocket server
│   │     entrypoint: ./migrate up && ./server (runs DB migrations on start)
│   │
│   ├── multica-frontend-1
│   │     image: ghcr.io/multica-ai/multica-web:latest
│   │     networks: internal + agent-network
│   │     port: 127.0.0.1:3000 → container:3000
│   │     purpose: Next.js web UI
│   │
│   └── multica-daemon-1
│         image: multica-daemon:local (custom built)
│         base: openclaw/openclaw:latest + multica CLI binary
│         networks: internal + agent-network
│         restart: "no"
│         purpose: polls backend for tasks, spawns openclaw to execute them
│         volumes:
│           - daemon_multica_config → /home/node/.multica  (token + config)
│           - daemon_workspaces    → /home/node/multica_workspaces
│           - host ~/.openclaw     → /home/node/.openclaw  (openclaw config)
│
└── OPENCLAW STACK (docker-compose.yml in openclaw/)
    │
    ├── openclaw-gateway-1
    │     image: openclaw/openclaw:latest (or openclaw:local if built locally)
    │     networks: agent-network + default
    │     ports: 18789 (gateway), 18790 (bridge), 3978 (MS Teams)
    │     purpose: OpenClaw gateway web UI and API
    │
    └── openclaw-cli-1
          image: openclaw/openclaw:latest
          network_mode: service:openclaw-gateway (shares gateway network stack)
          purpose: interactive CLI for openclaw
```

### Network Topology

```
agent-network (external Docker bridge)
    ├── multica-backend-1    (reachable as "backend" within this network)
    ├── multica-frontend-1
    ├── multica-daemon-1
    └── openclaw-gateway-1

internal (bridge, multica-only)
    ├── multica-postgres-1   (only reachable by backend)
    └── multica-backend-1
```

**Key point:** `postgres` is on the `internal` network only — it is never exposed to `agent-network` or the host. This is intentional security isolation.

---

## 3. Files Changed or Created

### New Files Created

| File | Location | Purpose |
|------|----------|---------|
| `Dockerfile.daemon` | `multica/Dockerfile.daemon` | Builds the daemon image on top of openclaw |
| `docker/daemon-entrypoint.sh` | `multica/docker/daemon-entrypoint.sh` | Entrypoint script for daemon container |
| `multica-control` | `multica/multica-control` | Control script for the multica stack |

### Files Modified

| File | Location | What Changed |
|------|----------|-------------|
| `docker-compose.yml` | `multica/docker-compose.yml` | Completely rewritten — added backend, frontend, daemon services; two networks; healthchecks |

### Files NOT Modified (left as-is)

| File | Reason |
|------|--------|
| `openclaw/docker-compose.yml` | Already had `agent-network` external network defined |
| `openclaw/openclaw-control` | Already existed and worked |
| `multica/docker-compose.selfhost.yml` | Reference file, not used directly |
| `multica/Dockerfile` | Backend image built by CI, not locally |
| `multica/Dockerfile.web` | Frontend image built by CI, not locally |
| `multica/docker/entrypoint.sh` | Backend entrypoint, unchanged |

### Symlink Created

```
/home/master/.local/bin/multica-control → /home/master/Agentic AI Programme/multica/multica-control
```

`~/.local/bin` is already on PATH via `~/.profile`.

---

## 4. Step-by-Step: What Was Done and Why

### Step 1 — Analysed the original docker-compose.yml files

**Original `multica/docker-compose.yml`** only had a single `postgres` service. No backend, no frontend, no daemon.

**Original `openclaw/docker-compose.yml`** had `openclaw-gateway` and `openclaw-cli` services, already referencing `agent-network` as an external network.

### Step 2 — Rewrote `multica/docker-compose.yml`

Added the full self-host stack based on `docker-compose.selfhost.yml` (the reference file), with these key additions:

- **Two networks**: `internal` (postgres isolation) and `agent-network` (shared with openclaw)
- **Backend healthcheck**: `wget -qO- http://127.0.0.1:8080/health` so the daemon waits for the backend to be ready
- **`APP_ENV=development`** and **`MULTICA_DEV_VERIFICATION_CODE=888888`** to bypass email OTP for login
- **`FRONTEND_ORIGIN` and `CORS_ALLOWED_ORIGINS`** set to `http://localhost:3000` to fix CORS errors
- Ports bound to `127.0.0.1` only (security — Docker bypasses UFW/iptables by default)

### Step 3 — Created `Dockerfile.daemon`

The daemon needs:
1. The `multica` CLI binary (Go static binary from GitHub Releases)
2. The `openclaw` binary (already in `openclaw/openclaw:latest` at `/usr/local/bin/openclaw`)

Solution: Build `FROM openclaw/openclaw:latest`, then download and install the `multica` binary on top.

The image also installs `gosu` to handle volume ownership — Docker named volumes are created as root-owned, but the container runs as the `node` user. A root wrapper script (`daemon-init.sh`) runs `chown` then drops to `node` via `gosu`.

### Step 4 — Created `docker/daemon-entrypoint.sh`

The entrypoint handles two states:
- **Token exists** (`"token"` key found in `/home/node/.multica/config.json`): start the daemon
- **No token**: print a message and `exec tail -f /dev/null` to keep the container alive for login

### Step 5 — Created `multica-control` script

Modelled after `openclaw/openclaw-control`. Provides `start`, `stop`, `restart`, `status`, `logs`, `build`, `login`, `daemon`, `health` commands. The `login` command:
1. Prompts for a personal access token (read silently)
2. Sets `server_url` and `app_url` in the daemon container's config
3. Runs `multica login --token <token>` inside the container
4. Force-recreates the daemon container so it re-runs the entrypoint and picks up the token

### Step 6 — Created the shared Docker network

```bash
docker network create agent-network
```

This must exist before either stack starts.

---

## 5. Errors Encountered and How They Were Fixed

### Error 1 — `ARG` not declared before `FROM`

```
WARN: UndefinedArgInFrom: FROM argument 'OPENCLAW_IMAGE' is not declared
failed to solve: openclaw:local: not found
```

**Cause:** Docker requires `ARG` to be declared before `FROM` when used in the `FROM` instruction.

**Fix:** Moved `ARG OPENCLAW_IMAGE=openclaw/openclaw:latest` to the very first line of `Dockerfile.daemon`, before `FROM`.

---

### Error 2 — Wrong openclaw image name

```
failed to solve: openclaw:local: failed to resolve source metadata
```

**Cause:** The default image name `openclaw:local` didn't exist locally. The actual image was `openclaw/openclaw:latest`.

**Fix:** Changed default in `Dockerfile.daemon` and `docker-compose.yml` from `openclaw:local` to `openclaw/openclaw:latest`.

**How to find the correct image name:**
```bash
docker images | grep openclaw
```

---

### Error 3 — Daemon container crash-looping before authentication

**Cause:** The original `Dockerfile.daemon` had `CMD ["daemon", "start", "--foreground"]` which immediately tries to connect to the backend with no token, fails, and exits. Docker's `restart: unless-stopped` policy then restarts it in a loop.

**Fix:** Created `docker/daemon-entrypoint.sh` that checks for a token before starting the daemon. If no token, runs `tail -f /dev/null` to keep the container alive. Changed daemon `restart` policy to `"no"` to prevent restart loops while idling.

---

### Error 4 — `set -e` in entrypoint killing the script

**Cause:** `multica auth status` exits with code 1 when not authenticated. With `set -e` at the top of the entrypoint, this killed the script before reaching the `else` branch, causing the container to exit.

**Fix:** Removed `set -e` from `daemon-entrypoint.sh`. The script uses explicit `|| true` where needed.

---

### Error 5 — `multica auth status` always exits 0

**Cause:** Even with no server configured, `multica auth status` exits 0 and prints "No server configured." This made it useless as a condition to check authentication state.

**Fix:** Changed the check to look directly at the config file:
```sh
if [ -f "$CONFIG" ] && grep -q '"token"' "$CONFIG"; then
```
After a successful `multica login`, the token is stored as a `"token"` key inside `/home/node/.multica/config.json`.

---

### Error 6 — Docker Compose interpolating shell variables

```
WARN: The "AUTHED" variable is not set. Defaulting to a blank string.
```

**Cause:** When using an inline `command:` block in `docker-compose.yml`, Docker Compose tries to interpolate `$VARIABLE` as a compose environment variable. Shell variables like `$?` and `$AUTHED` were being swallowed.

**Fix:** Moved the logic entirely into `docker/daemon-entrypoint.sh` (a file baked into the image), removing the inline command from `docker-compose.yml` entirely. This means Docker Compose never sees the shell variables.

---

### Error 7 — Volume owned by root, `node` user can't write

```
create temp config file: open /home/node/.multica/.config-xxx.json.tmp: permission denied
```

**Cause:** Docker named volumes are initialised as root-owned. The daemon container runs as the `node` user (uid 1000), which can't write to a root-owned directory.

**Fix:** Added a root wrapper script (`daemon-init.sh`) as the actual `ENTRYPOINT`. It runs as root, does `chown -R node:node /home/node/.multica`, then uses `gosu node` to drop privileges and exec the real entrypoint. `gosu` is installed in the Dockerfile via `apt-get install gosu`.

---

### Error 8 — `docker compose up -d` not recreating the container after login

**Cause:** `docker compose up -d` is idempotent — if the container is already running, it doesn't recreate it. After `multica login` writes the token to the volume, the container needs to be recreated to re-run the entrypoint and detect the token.

**Fix:** Changed `multica-control login` to use `--force-recreate`:
```bash
docker compose up -d --no-build --force-recreate daemon
```

---

### Error 9 — CORS errors preventing login

**Cause:** The backend's `FRONTEND_ORIGIN` and `CORS_ALLOWED_ORIGINS` were not set, defaulting to values that didn't match the actual frontend URL.

**Fix:** Explicitly set both in `docker-compose.yml`:
```yaml
FRONTEND_ORIGIN: ${FRONTEND_ORIGIN:-http://localhost:3000}
CORS_ALLOWED_ORIGINS: ${CORS_ALLOWED_ORIGINS:-http://localhost:3000}
```

If accessing from a different IP or hostname, set these in `.env` to match.

---

### Error 10 — No SMTP / email for OTP login

**Cause:** Multica uses email-based OTP for authentication. Without `RESEND_API_KEY` or `SMTP_HOST` configured, no email is sent and login is impossible.

**Fix:** Set `APP_ENV=development` and `MULTICA_DEV_VERIFICATION_CODE=888888` in the backend environment. In development mode, any email address can log in using the fixed OTP `888888`. This is **ignored when `APP_ENV=production`**.

> **Warning:** Never set `MULTICA_DEV_VERIFICATION_CODE` on a publicly accessible instance.

---

## 6. How the Two Stacks Connect

The two stacks are connected via the **`agent-network`** external Docker bridge network. This network must be created manually before starting either stack:

```bash
docker network create agent-network
```

### What shares the network

| Container | Networks |
|-----------|----------|
| `multica-backend-1` | `internal` + `agent-network` |
| `multica-frontend-1` | `internal` + `agent-network` |
| `multica-daemon-1` | `internal` + `agent-network` |
| `openclaw-gateway-1` | `agent-network` + `default` |

### What the network is used for

Currently the `agent-network` provides **potential** connectivity between the stacks. In the current setup:

- The **multica daemon** uses the `openclaw` binary **inside its own container** (not the openclaw-gateway container) to execute tasks
- The `agent-network` is in place for future integration where the daemon could call the openclaw gateway API directly

The openclaw-gateway container runs independently as openclaw's own web UI/API and is not directly involved in multica task execution.

---

## 7. The Daemon: How It Works

### What the daemon does

1. Connects to the multica backend over WebSocket (`ws://backend:8080/ws`)
2. Polls for tasks assigned to agents in watched workspaces (every 3 seconds by default)
3. When a task arrives, creates an isolated workspace directory under `/home/node/multica_workspaces/`
4. Spawns the `openclaw` binary as a subprocess to execute the task
5. Streams results back to the backend
6. Sends heartbeats every 15 seconds so the backend knows the daemon is alive

### How the daemon image is built

```
openclaw/openclaw:latest          ← base image (has openclaw binary at /usr/local/bin/openclaw)
    + multica CLI binary           ← downloaded from GitHub Releases during docker build
    + gosu                         ← for dropping root privileges
    + daemon-init.sh               ← root wrapper: chown volume, then gosu node → entrypoint
    + daemon-entrypoint.sh         ← checks for token, starts daemon or idles
```

### Entrypoint flow

```
daemon-init.sh (runs as root)
    └── chown -R node:node /home/node/.multica
    └── gosu node daemon-entrypoint.sh (drops to node user)
            └── multica config set server_url http://backend:8080
            └── multica config set app_url http://localhost:3000
            └── check if /home/node/.multica/config.json contains "token"
                    ├── YES → exec multica daemon start --foreground
                    └── NO  → print message, exec tail -f /dev/null (idle)
```

### Volumes

| Volume | Mount point | Purpose |
|--------|-------------|---------|
| `daemon_multica_config` | `/home/node/.multica` | Persists multica CLI config and auth token across restarts |
| `daemon_workspaces` | `/home/node/multica_workspaces` | Task execution directories |
| `~/.openclaw` (host) | `/home/node/.openclaw` | OpenClaw config and state |
| `~/.openclaw-auth-profile-secrets` (host) | `/home/node/.config/openclaw` | OpenClaw auth profiles |

---

## 8. Login / OTP Problem and Fix

### The problem

Multica's login flow:
1. User enters email on the frontend
2. Backend generates a 6-digit OTP and sends it via email (Resend or SMTP)
3. User enters OTP to authenticate

Without email configured, step 2 fails silently and the user never receives the OTP.

### The fix

Set these two environment variables on the backend service:

```yaml
APP_ENV: development
MULTICA_DEV_VERIFICATION_CODE: "888888"
```

In `development` mode with a fixed code set, **any email address** can log in using OTP `888888`.

### Alternative: read OTP from logs

If you prefer not to use a fixed code, leave `MULTICA_DEV_VERIFICATION_CODE` unset. The backend will print the generated code to stdout:

```bash
docker compose logs backend | grep "Verification code"
# daemon-1 | [DEV] Verification code for user@example.com: 123456
```

### Production login

For production, configure one of:
- `RESEND_API_KEY` — Resend SaaS email service (recommended)
- `SMTP_HOST` + `SMTP_PORT` + `SMTP_USERNAME` + `SMTP_PASSWORD` — any SMTP relay

---

## 9. Control Scripts

### `openclaw-control`

Location: `/home/master/Agentic AI Programme/openclaw/openclaw-control`
Symlinked to: already on PATH (check with `which openclaw-control`)

| Command | Action |
|---------|--------|
| `openclaw-control start` | Start openclaw gateway |
| `openclaw-control stop` | Stop openclaw gateway |
| `openclaw-control restart` | Restart gateway container |
| `openclaw-control status` | Show container status |
| `openclaw-control logs` | Stream gateway logs |
| `openclaw-control health` | Check gateway health |
| `openclaw-control chat` | Interactive CLI session |

### `multica-control`

Location: `/home/master/Agentic AI Programme/multica/multica-control`
Symlinked to: `/home/master/.local/bin/multica-control`

| Command | Action |
|---------|--------|
| `multica-control start` | Start all services (postgres, backend, frontend, daemon) |
| `multica-control stop` | Stop all services |
| `multica-control restart` | Restart all services |
| `multica-control status` | Show all container statuses |
| `multica-control logs` | Stream all logs |
| `multica-control logs <svc>` | Stream logs for specific service (backend/frontend/daemon/postgres) |
| `multica-control build` | Rebuild the daemon image |
| `multica-control login` | Authenticate daemon with personal access token (one-time setup) |
| `multica-control daemon` | Show daemon status (agents detected, workspaces, uptime) |
| `multica-control health` | Check backend `/health` endpoint |

---

## 10. Daily Workflow

### First-time setup

```bash
# 1. Create the shared network (once ever)
docker network create agent-network

# 2. Build the openclaw image (if not already built)
cd "/home/master/Agentic AI Programme/openclaw"
docker compose build

# 3. Start openclaw
openclaw-control start

# 4. Start multica (builds daemon image on first run)
multica-control start
# Wait ~30 seconds for backend to be healthy

# 5. Open http://localhost:3000, enter any email, use OTP: 888888
# Create your account and workspace

# 6. Go to Settings → API Tokens, create a token

# 7. Authenticate the daemon (one-time)
multica-control login
# Paste your token when prompted

# 8. Verify daemon is connected
multica-control daemon
# Should show: Agents: openclaw, Workspaces: 1
```

### Daily start

```bash
multica-control start
openclaw-control start
```

### Daily stop

```bash
multica-control stop
openclaw-control stop
```

### Check everything is running

```bash
multica-control status
openclaw-control status
```

---

## 11. Key Design Decisions

### Why the daemon runs in a container (not on the host)

Complete isolation — the daemon's lifecycle is tied to the multica stack. `multica-control stop` stops everything including the daemon. No host-side processes to manage.

### Why the daemon is built FROM the openclaw image

The daemon needs the `openclaw` binary on PATH to execute AI tasks. Rather than installing Node.js and openclaw separately, we use the openclaw image as a base — it already has `openclaw` at `/usr/local/bin/openclaw`, Node.js, and all dependencies. The multica CLI binary (a single static Go binary) is layered on top.

### Why `restart: "no"` on the daemon

Before authentication, the daemon container idles with `tail -f /dev/null`. With `restart: unless-stopped`, Docker would restart the container after every `docker compose up` cycle, causing it to re-run the entrypoint. Since the entrypoint exits cleanly (exit 0) when idling is interrupted, `restart: "no"` prevents unnecessary restart loops. After login, the daemon process itself keeps running indefinitely.

### Why postgres is on `internal` network only

Docker bypasses host firewall rules (UFW/iptables) by default. Putting postgres only on the `internal` network means it is never reachable from outside the multica stack, even if Docker's port publishing were misconfigured.

### Why ports are bound to `127.0.0.1`

Same reason — prevents Docker from exposing ports to the network interface. The backend (8080) and frontend (3000) are only reachable from localhost, which is sufficient for the daemon (which connects via Docker DNS, not localhost) and for browser access from the same machine.

### Why `gosu` instead of `su` or `sudo`

`gosu` is the standard Docker pattern for dropping privileges in entrypoints. Unlike `su`, it properly replaces the process (exec semantics) so signals (SIGTERM, etc.) are delivered correctly to the child process. This is important for graceful shutdown.

---

## 12. Environment Variables Reference

### Backend (multica-backend)

| Variable | Default | Purpose |
|----------|---------|---------|
| `APP_ENV` | `development` | Set to `production` to enforce real email OTP |
| `MULTICA_DEV_VERIFICATION_CODE` | `888888` | Fixed OTP for dev login (ignored in production) |
| `JWT_SECRET` | `change-me-in-production` | **Change this** for any real deployment |
| `FRONTEND_ORIGIN` | `http://localhost:3000` | Must match actual frontend URL to avoid CORS errors |
| `CORS_ALLOWED_ORIGINS` | `http://localhost:3000` | Must match actual frontend URL |
| `DATABASE_URL` | derived from postgres vars | PostgreSQL connection string |
| `RESEND_API_KEY` | empty | Resend email API key for production OTP |
| `SMTP_HOST` | empty | SMTP relay host for production OTP |

### Daemon (multica-daemon)

| Variable | Value | Purpose |
|----------|-------|---------|
| `MULTICA_SERVER_URL` | `ws://backend:8080/ws` | WebSocket URL to backend (Docker DNS) |
| `MULTICA_OPENCLAW_PATH` | `/usr/local/bin/openclaw` | Explicit path to openclaw binary |
| `MULTICA_DAEMON_POLL_INTERVAL` | `3s` | How often to poll for new tasks |
| `MULTICA_DAEMON_HEARTBEAT_INTERVAL` | `15s` | How often to send heartbeat to backend |
| `MULTICA_DAEMON_DEVICE_NAME` | `docker-daemon` | Name shown in Settings → Runtimes |

### OpenClaw Gateway

| Variable | Default | Purpose |
|----------|---------|---------|
| `OPENCLAW_GATEWAY_TOKEN` | empty | Auth token for gateway API |
| `CLAUDE_AI_SESSION_KEY` | empty | Claude AI session for openclaw |
| `OPENCLAW_GATEWAY_BIND` | `lan` | Bind to all interfaces (needed for Docker bridge networking) |

---

## Appendix: File Contents Summary

### `multica/Dockerfile.daemon`
Builds the daemon image: starts from `openclaw/openclaw:latest`, installs `multica` CLI binary from GitHub Releases, installs `gosu`, copies entrypoint scripts, sets `ENTRYPOINT` to `daemon-init.sh`.

### `multica/docker/daemon-entrypoint.sh`
Shell script (no `set -e`): sets `server_url` and `app_url` in multica config, checks for `"token"` in `config.json`, either starts the daemon or idles with `tail -f /dev/null`.

### `multica/docker-compose.yml`
Full self-host stack: postgres (internal network only), backend (internal + agent-network, healthcheck), frontend (internal + agent-network), daemon (internal + agent-network, `restart: "no"`, built from `Dockerfile.daemon`). Two named networks: `internal` (bridge) and `agent-network` (external).

### `multica/multica-control`
Bash control script. Hardcodes `PROJECT_DIR`. Provides start/stop/restart/status/logs/build/login/daemon/health commands. `login` command uses `--force-recreate` to ensure the daemon re-runs its entrypoint after token is written.
