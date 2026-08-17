# Multica — cloning and installation

**Manish Prakash · Team Mohit · 3 August 2026**

> **Status:** installation reference. Steps I ran are described plainly; steps I have
> not personally verified end-to-end are marked *(unverified)*.

---

## 1. What Multica is

A **self-hosted, AI-native project management platform** — think Linear or Jira,
except issues can be assigned to AI agents rather than to people, and the agents
execute them.

Stack:

| Component | Technology |
|---|---|
| Backend API | Go |
| Frontend | Next.js |
| Database | PostgreSQL with **pgvector** |
| Daemon | Polls the backend for assigned tasks and spawns an agent CLI to run them |

Official images: `ghcr.io/multica-ai/multica-backend`, `ghcr.io/multica-ai/multica-web`.

### The piece that took longest to understand

**Multica does not contain an AI agent.** It is the *work queue and UI*. The
**daemon** is a separate process that watches for tasks assigned to an agent and
shells out to an agent runtime — OpenClaw, for example — to actually do them.

```
User creates issue → assigns to agent → daemon polls, sees it
                                      → spawns `openclaw` to execute
                                      → writes the result back to the issue
```

Once that clicked, the whole architecture made sense: Multica is the *manager*,
OpenClaw is the *worker*. Neither is useful alone for this workflow. This is also
why pgvector is in the stack — issue history is embedded so agents can retrieve
relevant prior context.

---

## 2. Prerequisites

| Requirement | Notes |
|---|---|
| Docker + Docker Compose | The strongly preferred install route |
| ~16 GB RAM | Postgres + backend + web + agent runtime together |
| Free ports | 3000 (web), backend API, 5432 (Postgres) |
| A model provider key | The agents need one |
| Git | Cloning |

---

## 3. Clone

```bash
git clone https://github.com/multica-ai/multica.git
cd multica
```

Keep it somewhere stable — the daemon config will reference absolute paths, and
moving the directory later means editing them.

---

## 4. Configure

```bash
cp .env.example .env
```

Values that matter:

```bash
DATABASE_URL=postgres://multica:<password>@postgres:5432/multica
MULTICA_ENV=development
ANTHROPIC_API_KEY=sk-ant-...        # or your provider of choice
NEXT_PUBLIC_API_URL=http://localhost:8080
```

Two notes worth more than they look:

- Inside Docker Compose, the database host is the **service name** (`postgres`), not
  `localhost`. `localhost` inside a container is the container itself. This is the
  most common connection failure.
- `.env` now holds a provider key. Confirm it is in `.gitignore` before your first
  commit — see [`../29_July_2026/oauth_vs_api_key.md`](../29_July_2026/oauth_vs_api_key.md)
  on why a leaked static key is the worst kind.

---

## 5. Launch

```bash
docker compose up -d --build
docker compose ps
docker compose logs -f backend
```

Expect the first build to take a while — Go compile plus a Next.js build.

**Wait for Postgres before judging the backend.** The backend often restarts a few
times while the database initialises; that is normal on first run and looks alarming
in the logs.

Then open <http://localhost:3000>.

---

## 6. Onboarding

1. Create the first account — it becomes the instance admin.
2. Create a workspace.
3. Create a project.
4. Register an agent as an assignee.
5. Create an issue and assign it to that agent.

At step 5 nothing happens yet, and that is expected: **without the daemon running,
the issue just sits there.** This confused me until I understood the architecture in
§1.

---

## 7. The daemon

The daemon is what makes the platform agentic rather than just a kanban board. It:

1. polls the backend for issues assigned to an agent;
2. builds a prompt from the issue title, description, and retrieved context;
3. spawns the agent CLI (e.g. `openclaw`) with that prompt;
4. captures the output and posts it back as a comment or status change.

It needs to reach both the Multica API and the agent binary. Running the two stacks
in separate Compose projects on a **shared Docker network** is the cleanest
arrangement — it keeps them independently restartable while letting them resolve
each other by service name *(unverified in my own setup; this is the design I
followed from the reference architecture)*.

---

## 8. Problems and fixes

| Symptom | Cause | Fix |
|---|---|---|
| Backend restart loop on first run | Postgres not ready yet | Wait; add a healthcheck + `depends_on: condition: service_healthy` |
| `connection refused` to database | `DATABASE_URL` uses `localhost` | Use the Compose service name (`postgres`) |
| Frontend loads, API calls fail | `NEXT_PUBLIC_API_URL` wrong | Must be reachable **from the browser**, not from inside the container |
| Port 3000 in use | Something else running | Remap in `docker-compose.yml` |
| Issue assigned but nothing happens | Daemon not running | Start the daemon — Multica alone does not execute |
| Login / OTP not arriving | No mail transport configured in a local dev instance | Read the code from the backend logs, or enable a dev auth bypass |

---

## 9. Assessment

**What is genuinely good:**
- Treating agent work as **issues with a lifecycle** is the right abstraction. It
  gives you assignment, status, comments, and history for free — all things ad-hoc
  agent scripts lack entirely.
- Self-hosted with your own keys: no third-party sees your code or your prompts.
- pgvector in the stack means retrieval over project history is built in rather than
  bolted on.

**What is hard:**
- **It is four moving parts** (backend, web, Postgres, daemon) plus a separate agent
  runtime. Any one being down produces "nothing happens" with no useful error.
- Resource-hungry for a laptop.
- Early-stage software: sparse documentation, and the daemon is the least documented
  and most essential part.

**Where it fits:** Multica is worth the setup cost when you have *recurring,
trackable* agent work that a team needs visibility into. For one-off tasks, a CLI
agent is faster and simpler. The value is the audit trail and the queue, not the
intelligence.
