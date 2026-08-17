# 29 July 2026 — Tasks

**Manish Prakash · Team Mohit**

## Assigned

1. Positives and negatives of developing agents in Visual Studio / VS Code Copilot
2. Positives and negatives of OAuth keys (dynamic, session-based) vs API keys (static, permanent)
3. OpenClaw installation — setup and onboarding, complete configuration

## Deliverables

| # | Deliverable | File |
|---|---|---|
| 1 | Copilot agent development — balance sheet + recommendation | [`copilot_agent_development.md`](copilot_agent_development.md) |
| 2 | OAuth vs API key — full comparison | [`oauth_vs_api_key.md`](oauth_vs_api_key.md) |
| 3 | OpenClaw install, config schema, security posture | [`openclaw_setup.md`](openclaw_setup.md) |

## Key takeaways

- **Copilot agent mode is an accelerator, not an autonomous developer.** Its real
  advantage is free editor context and a tight build-fix-run loop; its real risk is
  autonomous terminal execution combined with repo content it did not author.
- **API keys trade security for simplicity; OAuth trades simplicity for security.**
  Neither is universally right. The common real-world mistake is using a static key
  where a scoped token belonged, because the key was faster to ship.
- **Agents amplify both credential failure modes** — which is why remote MCP servers
  standardise on OAuth 2.1 and why local stdio servers reading a plain key from the
  environment deserve scrutiny.
- **In OpenClaw, `bindings` and `channels` are root-level**, not per-agent. Most
  first-run failures are that structural mistake, reported as a generic schema error.
- **`AGENTS.md` quality matters more than model choice.** The install takes twenty
  minutes; writing a good agent identity is the rest of the work.
- **Sandbox before experimenting.** Shell access plus a public messaging channel is
  a prompt-injection surface by construction.
