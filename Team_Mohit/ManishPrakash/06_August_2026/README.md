# 6 August 2026 — Tasks

**Manish Prakash · Team Mohit**

## Assigned

1. What is the difference between API and MCP (including the drawbacks of API over MCP)
2. Explore <https://mcpservers.org> and <https://mcpmarket.com/submit>
3. Re-attempt Task 6 from the previous day, then build a weather predictor for Bhubaneswar

## Deliverables

| # | Deliverable | File |
|---|---|---|
| 1 | API vs MCP comparison + API drawbacks | [`api_vs_mcp.md`](api_vs_mcp.md) |
| 2 | MCP directory exploration & security notes | [`mcp_directories_exploration.md`](mcp_directories_exploration.md) |
| 3 | Bhubaneswar weather predictor (working code) | [`weather_predictor/`](weather_predictor/) |

Task 6 of 5 August (AnythingLLM RAG → MCP) is written up under
[`../05_August_2026/06_anythingllm_rag_as_mcp.md`](../05_August_2026/06_anythingllm_rag_as_mcp.md).

## Run the weather predictor

```bash
cd weather_predictor
python3 bhubaneswar_weather.py --days 7
```

Python 3.9+, standard library only, no API key.

## Key takeaways

- **MCP does not replace APIs — it wraps them.** Nearly every MCP server is a thin
  adapter over an existing API. The API does the work; MCP makes it reachable by a
  model without bespoke per-client glue.
- **The M×N → M+N reduction is the whole argument.** 4 AI clients × 10 tools is 40
  hand-written connectors without MCP and 14 implementations with it.
- **The worst API drawback for agents is the absence of runtime discovery.** A model
  cannot use a tool nobody compiled into the client; adding a tool means a redeploy.
- **APIs still win** on determinism, latency, throughput, maturity, and any workflow
  with no LLM in the loop.
- **The weather script is a live demonstration of the drawbacks**, not just an
  illustration of them: hard-coded field names, a client-side copy of the server's
  WMO code table, and no way for a model to discover it.
- **Directory convenience cuts both ways.** One config line installs third-party
  code that runs with your privileges inside the model's trust boundary. Audit first.
