# 5 August 2026 — Tasks

**Manish Prakash · Team Mohit**

## Assigned

1. Compulsory installation of Multica (Docker preferred)
2. *(team leaders only)* Create workspace for your team
3. Connect Multica with Slack
4. Experiment with OpenCode (best for runtime)
5. Experiment with Microsoft recorder skills
6. *(advanced)* Connect AnythingLLM's RAG database to Multica/OpenClaw by exposing it as an MCP server

## Deliverables

| # | Deliverable | File |
|---|---|---|
| 1 | Multica via Docker — Docker-specific setup | [`01_multica_docker_install.md`](01_multica_docker_install.md) |
| 2 | Workspace model + handover notes | [`02_team_workspace.md`](02_team_workspace.md) |
| 3 | Slack integration | [`03_multica_slack_integration.md`](03_multica_slack_integration.md) |
| 4 | OpenCode evaluation | [`04_opencode_experiment.md`](04_opencode_experiment.md) |
| 5 | Microsoft recorder skills | [`05_microsoft_recorder_skills.md`](05_microsoft_recorder_skills.md) |
| 6 | AnythingLLM RAG as MCP — design + **working server** | [`06_anythingllm_rag_as_mcp.md`](06_anythingllm_rag_as_mcp.md) · [`anythingllm_mcp_server/`](anythingllm_mcp_server/) |

Task 2 was scoped to team leaders; my notes cover the workspace model and a handover
list rather than creating the Team Mohit workspace.

## Key takeaways

- **Docker is not just convenient for Multica — it is the difference between twenty
  minutes and a lost day.** Four interdependent services plus pgvector. The cost is
  that every host networking assumption is now wrong: `DATABASE_URL` needs the
  Compose service name, `NEXT_PUBLIC_API_URL` needs a browser-reachable host.
- **An agent-assigned issue is a prompt with a database row around it** — and unlike
  a chat you cannot nudge it mid-run, so acceptance criteria in the issue body are
  the highest-leverage habit.
- **Socket Mode is what makes Slack practical for a self-hosted stack** — no public
  URL, no ngrok. And the 3-second ack requirement versus multi-minute agent latency
  forces an ack-first, answer-later design in every integration of this kind.
- **OpenCode's advantage is the loop**, not the model: change → run → read failure →
  change again, in the terminal where the build already lives. Give it a runnable
  verification command and it produces real fixes; without one it produces churn.
- **Recorded automation and model-driven agents are complements.** Model decides
  *what* and supplies parameters; the recording does *how*, deterministically and
  for free. Using a model to click a fixed five-step form is slower, costlier, and
  less reliable than a recording.
- **The RAG-over-MCP task is the clearest demonstration of MCP's value in the whole
  program:** one ~120-line server gives every current and future MCP client document
  retrieval, AnythingLLM's API is unchanged and unaware, and the real engineering is
  in the tool docstrings rather than the code.
- **Granting a tool is not the same as using it.** The agent needs an explicit
  `AGENTS.md` instruction to search the knowledge base first — the most common
  reason a correct RAG integration appears to do nothing.
