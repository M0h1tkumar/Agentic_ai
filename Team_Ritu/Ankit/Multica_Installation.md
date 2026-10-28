# Multica — Local Installation (Self-Hosted)

Notes from installing and running Multica locally on **Windows + WSL2**, self-hosted mode
(prebuilt Docker images + CLI + auth + daemon).

Repository: https://github.com/multica-ai/multica

## Environment
- **OS:** Windows 11 with WSL2 (Ubuntu)
- **Mode:** Self-hosted (`make selfhost`) — Docker containers pulled from GHCR, not built from source

## 1. Prerequisites

Checked in the WSL terminal before installing anything:

```bash
git --version
node --version
pnpm --version
go version
docker --version
docker compose version
make --version
```

| Requirement | Version installed | Notes |
|---|---|---|
| Git | 2.53.0 | already present |
| Node.js | 24.19.0 | already present |
| pnpm | 11.20.0 | already present |
| Go | 1.26.0 | already present |
| Docker | 29.6.2 | required enabling **WSL2 integration** in Docker Desktop settings first |
| Docker Compose | v5.3.1 | bundled with Docker |
| Make | 4.4.1 | already present |

**Docker fix needed:** Docker Desktop was installed on Windows but WSL integration wasn't
enabled. Fixed via Docker Desktop → **Settings → Resources → WSL Integration** → enable the
distro → **Apply & Restart**. After that, `docker --version` worked inside WSL.

## 2. Clone the repository

```bash
cd ~
git clone https://github.com/multica-ai/multica.git
cd multica
ls
```

Confirms the correct repo via key files: `Makefile`, `package.json`, `docker-compose.yml`,
`docker-compose.selfhost.yml`, `SELF_HOSTING.md`, `apps/`, `server/`.

## 3. Provision the self-hosted server

```bash
cd ~/multica
make selfhost
```

This command:
- Creates `.env` from `.env.example`, generating a random `JWT_SECRET`, `POSTGRES_PASSWORD`,
  and `MULTICA_VCS_SECRET_KEY`
- Pulls the official prebuilt images: `ghcr.io/multica-ai/multica-backend:latest`,
  `ghcr.io/multica-ai/multica-web:latest`, `pgvector/pgvector:pg17`
- Starts Postgres, backend, and frontend via `docker-compose.selfhost.yml`

**Requires the Docker daemon to be running** (Docker Desktop open on Windows) — if it fails
with a "Cannot connect to the Docker daemon" error, start/wait for Docker Desktop and retry.

Expected success output:
```
✓ Multica is running!
  Frontend: http://localhost:3000
  Backend:  http://localhost:8080
```

Verify:
```bash
docker ps
curl -I http://localhost:3000   # expect 200 OK
```

## 4. Install the CLI

```bash
curl -fsSL https://raw.githubusercontent.com/multica-ai/multica/main/scripts/install.sh | bash
```

Installs the `multica` CLI binary to `/usr/local/bin/multica` (separate from the server, which
is already running in Docker).

## 5. Connect and authenticate

```bash
multica setup self-host
```

- Prompts for the server URL (`http://localhost:8080`) and app URL (`http://localhost:3000`)
- Prints a login URL — since WSL can't auto-open a Windows browser, copy the printed URL
  manually into the browser
- Enter your email on the login page. Since no email backend (`RESEND_API_KEY`/`SMTP_HOST`) is
  configured, the verification code is printed to the backend logs instead of emailed:

```bash
docker logs multica-backend-1 --tail 20
# look for: [DEV] Verification code for you@email.com: 123456
```

- Enter that code in the browser. **Do not close/Ctrl+C the terminal running `multica setup
  self-host`** while waiting — it runs a local callback server that the browser redirects to
  on success.
- On first run it will also prompt to create a workspace (`/workspaces/new` in the browser).

Successful end state:
```
Authenticated as you@email.com
Token saved to config.
Found 1 workspace(s): * <workspace name>
Starting daemon...
Daemon started (pid ..., version ...)
✓ Setup complete! Your machine is now connected to Multica.
```

## 6. Restarting after a reboot

Docker containers with `restart: unless-stopped` come back automatically once Docker Desktop
starts. The **daemon does not auto-restart** — after opening Docker Desktop and confirming
`docker ps` shows all 3 containers `Up`, run:

```bash
multica daemon start
```

Then open `http://localhost:3000` — login/workspace state persists across reboots.

## 7. Connecting an agent runtime (OpenCode / OpenClaw)

Agent runtimes (e.g. OpenCode, OpenClaw) must be installed and on **PATH inside WSL** — not
just on Windows — since the Multica daemon runs in WSL.

```bash
npm install -g opencode-ai
opencode --version
which opencode
```

After installing/changing PATH, restart the daemon so it re-detects available runtimes:
```bash
multica daemon stop
multica daemon start
```

Check **Runtimes** in the browser sidebar to confirm the runtime(s) show as online.

## Issues encountered & fixes

| Issue | Cause | Fix |
|---|---|---|
| `docker` not found in WSL | WSL integration disabled in Docker Desktop | Enable integration in Docker Desktop settings → restart |
| `make selfhost` Docker daemon error | Docker Desktop not fully started yet | Wait for Docker Desktop, retry |
| Old containers survived `docker compose down -v` | Containers were started from `docker-compose.selfhost.yml`, not the default `docker-compose.yml` | Remove by container name directly: `docker rm -f <name>`, then `docker volume rm`, `docker network prune -f` |
| Login callback "page not reachable" | `multica setup self-host` process was killed (Ctrl+C) while waiting for the browser callback | Re-run `multica setup self-host` and don't interrupt it until it confirms auth |
| Verification code "not coming" | Was filtering logs too narrowly (`grep -i code`); code was present as `[DEV] Verification code for ...` | Use `docker logs multica-backend-1 --tail 100` without a narrow filter |
| Runtime (OpenCode) not detected | Installed after the daemon had already started | Restart daemon (`multica daemon stop && multica daemon start`) after installing/PATH changes |

## Status
✅ Fully installed and verified — frontend, backend, Postgres, CLI, auth, and daemon all
working; OpenCode and OpenClaw both detected as runtimes.