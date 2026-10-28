# Multica Agentic AI Lab — Agent Documentation

This repository documents the Multica agents built as part of the Agentic AI Lab exercises,
running on a self-hosted Multica instance (Docker + OpenCode runtime) on WSL2.

## Environment
- **Multica:** self-hosted via `make selfhost` (Docker Compose: Postgres + backend + frontend)
- **Runtime:** OpenCode, connected via the Multica CLI daemon
- **Workspace:** Agentic AI Lab

## Agents

| # | Agent | Task | MCP Server | Status |
|---|-------|------|------------|--------|
| 1 | [Weather_Prediction](01-Weather_Prediction.md) | Weather + 5-day forecast for Bhubaneswar | `@timlukahorstmann/mcp-weather` (AccuWeather) | ✅ Working |
| 2 | [Explainer_Agent](02-Explainer_Agent.md) | Wikipedia summary, sections, and section extraction for Mahatma Gandhi | `wiki-mcp` | ✅ Working |
| 3 | [Currency_Converter_Agent](03-Currency_Converter_Agent.md) | Convert 500 USD→INR, show EUR→INR rate | `@easysolutions906/mcp-finance` | ✅ Working |
| 4 | [World_Clock_Agent](04-World_Clock_Agent.md) | Current time in Tokyo, London, New York | `mcp-server-time` | ⬜ Pending |
| 5 | [Definition_Agent](05-Definition_Agent.md) | Define 'ubiquitous' + example sentence | `mcp-server-dictionary` | ⬜ Pending |
| 6 | [HackerNews_Digest_Agent](06-HackerNews_Digest_Agent.md) | Top 5 HN stories with scores | `@devabdultech/hn-mcp-server` | ⬜ Pending |
| 7 | [GitHub_Repo_Agent](07-GitHub_Repo_Agent.md) | Open issue count + 3 most recent for anthropics/claude-code | `@modelcontextprotocol/server-github` | ⬜ Pending |

## Notes on package verification
Two originally-suggested MCP packages could not be verified to exist and were swapped for
verified alternatives (documented in each agent's file):
- `@cyanheads/wikipedia-mcp-server` → replaced with `wiki-mcp`
- `wesbos/currency-conversion-mcp` (hosted endpoint returned 404) → replaced with `@easysolutions906/mcp-finance`

## Setup pattern (per agent)
1. Verify/research the MCP server package and its exact tool names before configuring.
2. Test the MCP server standalone in a terminal (`npx`/`bunx`/`uvx ...`) to confirm it starts cleanly.
3. Create the skill in Multica (Skills → New skill) using the SKILL.md content in the agent's doc.
4. Create the agent (Agents → New agent) with the Instructions, OpenCode runtime, and skill attached.
5. Attach the MCP server under the agent's Capabilities tab (JSON mode, inner object only — no `mcpServers` wrapper).
6. Test via the agent's Chat/Test panel using the exact production prompt.
7. Optionally trigger via a real Issue (assign to the agent, place in Todo or later) to confirm end-to-end execution.