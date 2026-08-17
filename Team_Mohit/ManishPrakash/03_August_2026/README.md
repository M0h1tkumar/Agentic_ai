# 3 August 2026 — Tasks

**Manish Prakash · Team Mohit**

## Assigned

1. Cloning and installation of Multica
2. *(optional)* Experiment with OmniRoute

## Deliverables

| # | Deliverable | File |
|---|---|---|
| 1 | Multica install, architecture, troubleshooting | [`multica_setup.md`](multica_setup.md) |
| 2 | OmniRoute / LLM router evaluation | [`omniroute_notes.md`](omniroute_notes.md) |

## Key takeaways

- **Multica does not contain an agent.** It is the work queue and UI; the **daemon**
  spawns an agent runtime (OpenClaw) to execute assigned issues. Multica is the
  manager, OpenClaw is the worker. Without the daemon, an assigned issue simply sits
  there — which is the confusing part of the first run.
- **Treating agent work as issues with a lifecycle is the right abstraction.**
  Assignment, status, comments, and history come for free; ad-hoc agent scripts have
  none of that. The value is the audit trail, not the intelligence.
- **Inside Docker Compose, the DB host is the service name, not `localhost`.** That
  single mistake accounts for most first-run connection failures.
- **`NEXT_PUBLIC_API_URL` must be reachable from the browser**, not from inside the
  container — a different requirement that looks identical in the config file.
- **A router standardises models the way MCP standardises tools.** Router : models ::
  MCP : tools. Both let you swap implementations behind a fixed interface.
- **A router is infrastructure without a job until you have real spend or several
  models.** And check it exposes the provider features you rely on — trading away
  prompt caching for provider independence is a bad deal if caching is what makes
  the workload affordable.
