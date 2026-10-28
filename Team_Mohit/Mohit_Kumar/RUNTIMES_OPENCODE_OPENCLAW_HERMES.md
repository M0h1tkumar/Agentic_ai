# ⚙️ Agent Runtimes: OpenCode, OpenClaw, Multica & Hermes Swarms

> **Author:** Mohit Kumar — Team Mohit Lead  
> **Topic:** Runtime environments, session management, multi-agent communication, and squad coordination.

---

## 1. Comparing the Modern Agentic Runtimes

| Dimension | OpenCode | OpenClaw | Multica |
| :--- | :--- | :--- | :--- |
| **Primary Role** | Fast Headless Execution Engine | Agent Gateway & Session Server | Collaborative PM & Agent Orchestrator |
| **Best For** | Code generation, terminal loops, compilers | Stateful multi-turn chats, Slack/Discord bridges | Issue tracking, task delegation, team boards |
| **Port / Interface** | CLI-driven / Stdio / API | Web UI (`:18789`) / REST API | Web UI (`:3000`) / Go API (`:8080`) |
| **Memory Model** | Workspace file-based | Curated `MEMORY.md` + Daily Notes | PostgreSQL with `pgvector` embeddings |

---

## 2. OpenClaw: Native Gateway Architecture

OpenClaw acts as an intelligent proxy between human communication channels and autonomous agents.

### Core Structure:
- **`SOUL.md`**: The agent's core identity, persona, principles, and safety boundaries.
- **`USER.md`**: Human context, preferences, active working hours, and coding standards.
- **`MEMORY.md`**: Curated long-term memory distilled from past interactions.
- **`HEARTBEAT.md`**: Scheduled background tasks that the agent checks periodically (e.g., verifying builds, PR statuses, unread emails).

### Safe Multi-Channel Operation:
- **Direct Chat:** Full access to long-term memory and workspace tools.
- **Group Chat (Slack/Discord):** Restricts private memory access; only responds when directly tagged (`@agent`) or when critical errors are detected.

---

## 3. Multica: The Autonomous Project Manager

Multica provides a self-hosted platform (similar to Linear or Jira) where issues are assigned to AI agents instead of human engineers:
1. **Multica Backend:** Go-based API managing projects, tasks, comments, and agent teams.
2. **Multica Daemon:** A background listener that polls Multica's task queue, detects assigned tasks, and invokes the appropriate agent CLI (`openclaw` or `opencode`).
3. **Multica Web:** Next.js frontend where human operators review progress and live deployment links.

---

## 4. Hermes & Multi-Agent Swarms

A single monolithic agent struggles when balancing high-level design with deep debugging. **Hermes-style swarms** solve this by decomposing tasks into specialized micro-agents:

```
[User Request]
       │
       ▼
[Orchestrator Agent (Hermes Lead)]
       │
       ├──► [Researcher Subagent]: Checks docs, searches web, inspects repo
       │
       ├──► [Coder Subagent]: Implements files, updates database schemas
       │
       ├──► [Linter / Tester Subagent]: Runs builds, fixes compiler errors
       │
       └──► [DevOps Subagent]: Deploys commit to cloud & validates HTTP 200
```

### Key Principles of Swarm Architecture:
1. **Ephemeral Lifecycles:** Subagents are spawned for a specific sub-task and killed once finished to free up memory and token budget.
2. **Explicit Interfaces:** Subagents communicate via structured JSON or filesystem queues, never ambiguous conversational banter.
3. **Decoupled Fallbacks:** If a subagent crashes, the orchestrator catches the failure and spawns a retry or fallback agent without breaking the main task.
