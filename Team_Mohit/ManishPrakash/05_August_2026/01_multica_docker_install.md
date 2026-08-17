# 1 — Multica installation via Docker

**Manish Prakash · Team Mohit · 5 August 2026**

The full install walkthrough — architecture, `.env`, Compose, daemon, and the
troubleshooting table — is in
[`../03_August_2026/multica_setup.md`](../03_August_2026/multica_setup.md).

This page covers only what is specific to **making Docker the mandatory route**, as
the task requires.

---

## Why Docker is the right call here

| Reason | Detail |
|---|---|
| **Four services, one command** | Backend (Go), web (Next.js), Postgres+pgvector, daemon. Installing that stack natively means four toolchains and four sets of version conflicts. |
| **Reproducible across the team** | Everyone runs identical images. "Works on my machine" stops being a category of bug — which matters when a whole cohort is debugging together. |
| **pgvector without pain** | The Postgres image ships the extension. Building pgvector against a system Postgres is a genuinely annoying afternoon. |
| **Isolation** | Agent-adjacent software gets its own filesystem and network namespace instead of your host. This is the sandbox argument from the master task list, applied. |
| **Clean uninstall** | `docker compose down -v` removes everything, including the database volume. Native installs leave residue. |

---

## Minimal path

```bash
git clone https://github.com/multica-ai/multica.git
cd multica
cp .env.example .env
$EDITOR .env                    # DATABASE_URL, provider key, NEXT_PUBLIC_API_URL
docker compose up -d --build
docker compose ps
docker compose logs -f backend
```

Then <http://localhost:3000>.

---

## The three Docker-specific gotchas

1. **`localhost` inside a container is the container.** `DATABASE_URL` must use the
   Compose **service name** (`postgres:5432`). This causes more first-run failures
   than everything else combined.

2. **`NEXT_PUBLIC_API_URL` is evaluated in the browser.** It is baked into the
   frontend bundle and fetched by the user's browser, so it needs a host-reachable
   address (`http://localhost:8080`), *not* a service name. The two variables look
   symmetric in the file and are not.

3. **Startup order is not readiness order.** `depends_on` waits for the container to
   start, not for Postgres to accept connections. The backend restart loop on first
   run is this. Fix properly with a healthcheck:

   ```yaml
   postgres:
     healthcheck:
       test: ["CMD-SHELL", "pg_isready -U multica"]
       interval: 5s
       retries: 10
   backend:
     depends_on:
       postgres:
         condition: service_healthy
   ```

---

## Persistence

Named volumes, not bind mounts, for the database:

```yaml
volumes:
  multica-db:
```

`docker compose down` keeps the volume; `down -v` destroys it. Knowing which one you
typed is the difference between a restart and losing your workspace.

---

## Connecting to OpenClaw

The daemon must reach both the Multica API and the agent binary. Running the two
stacks as **separate Compose projects on a shared external network** keeps them
independently restartable while letting them resolve each other by name:

```bash
docker network create agentic-net
```

Then in both `docker-compose.yml` files:

```yaml
networks:
  default:
    external: true
    name: agentic-net
```

Separate projects rather than one big Compose file matters in practice: restarting
OpenClaw to pick up a config change should not bounce Postgres.

---

## Takeaway

Docker is not just convenient here — with four interdependent services and a
pgvector requirement, it is the difference between a twenty-minute setup and a lost
day. The cost is that every networking assumption you had on the host is now wrong,
and all three gotchas above are variations on that one theme.
