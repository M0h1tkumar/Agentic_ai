# API vs MCP — and where plain APIs fall short

**Manish Prakash · Team Mohit · 6 August 2026**

---

## 1. The short answer

An **API** is a contract between two pieces of *software*. A human developer reads
the documentation, writes glue code, and ships it. The integration is baked in at
build time.

**MCP (Model Context Protocol)** is a contract between an *AI model* and the tools,
data, and prompts it can reach. The model discovers what is available at runtime,
reads machine-supplied descriptions, and decides what to call. The integration is
negotiated at connect time.

> An API tells a program *how to call a function*.
> MCP tells a model *what functions exist, what they mean, and when to use them.*

MCP is not a replacement for APIs. Almost every MCP server is a wrapper **around**
an API. MCP is the standard adapter layer that sits between "an API exists" and
"an agent can use it without a developer writing bespoke code."

---

## 2. What each one actually is

### API (Application Programming Interface)

- A defined set of endpoints/functions plus request and response formats.
- Styles: REST, GraphQL, gRPC, SOAP, plain library calls.
- Authentication is per-provider: API keys, OAuth, mTLS, signed requests.
- **Documentation is for humans.** OpenAPI/Swagger is machine-*readable*, but it
  describes shape, not intent — it says a field is a string, not when to use it.
- The caller must know the endpoint exists before the program runs.

### MCP (Model Context Protocol)

- An open protocol (introduced by Anthropic in November 2024, now with a broad
  multi-vendor ecosystem) for connecting LLM applications to external capabilities.
- Client–server architecture over JSON-RPC 2.0, transported via **stdio** (local
  process) or **HTTP with Server-Sent Events / streamable HTTP** (remote).
- The server exposes three kinds of things:
  - **Tools** — actions the model may invoke (`send_email`, `query_db`).
  - **Resources** — data the model may read (files, rows, documents).
  - **Prompts** — reusable templates the user can trigger.
- The client (Claude Desktop, Claude Code, an IDE, a custom agent) connects,
  calls `tools/list`, and receives names, descriptions, and JSON Schemas.
- **Descriptions are for models.** They carry semantics, not just types.

---

## 3. Side-by-side

| Dimension | API | MCP |
|---|---|---|
| **Primary consumer** | Human developer writing code | AI model at runtime |
| **Discovery** | Read docs, then hard-code | `tools/list` at connect time |
| **When integration happens** | Build time | Connect time |
| **Interface style** | Per-provider, all different | One protocol, uniform |
| **Descriptions** | Type shapes (OpenAPI) | Type shapes **+ intent** |
| **Statefulness** | Usually stateless request/response | Persistent session, capability negotiation |
| **Integration cost** | M models × N tools = **M×N** connectors | **M + N** — each side implements once |
| **Adding a new tool** | Redeploy the client | Restart/reconnect; often zero client change |
| **Transport** | HTTP, gRPC, etc. | JSON-RPC 2.0 over stdio or HTTP+SSE |
| **Auth** | Key/OAuth per provider | Handled by the server; OAuth 2.1 for remote servers |
| **Maturity** | Decades of tooling | Young — 2024 onward, still evolving |
| **Best at** | Deterministic, high-volume, fixed workflows | Open-ended agentic work with changing tools |

---

## 4. The M×N problem — the core argument for MCP

This is the single most important idea, so it gets its own section.

**Without MCP.** You have 4 AI applications and 10 tools you want them to reach.
Every application needs its own connector for every tool: **40 integrations**, each
separately written, tested, versioned, and maintained. Adding an 11th tool means
writing 4 more connectors. Adding a 5th application means writing 10 more.

```
Claude ──┬── Slack        (custom connector 1)
         ├── GitHub       (custom connector 2)
         └── Postgres     (custom connector 3)
Cursor ──┬── Slack        (custom connector 4)  ← same tool, written again
         ├── GitHub       (custom connector 5)
         └── Postgres     (custom connector 6)
...
```

**With MCP.** Each tool ships one MCP server. Each application ships one MCP client.
**14 implementations instead of 40**, and each new tool is +1, not +4.

```
Claude ──┐                    ┌── Slack MCP server
Cursor ──┼── MCP protocol ────┼── GitHub MCP server
IDE    ──┤                    ├── Postgres MCP server
Custom ──┘                    └── Filesystem MCP server
```

This is the same shape of win that USB-C delivered over a drawer full of
proprietary charging cables — which is why MCP is routinely described as
"USB-C for AI applications."

---

## 5. Drawbacks of API compared to MCP

The task asks specifically for this, so here it is in detail. Each point is a
weakness of the *plain-API-plus-glue-code* approach when the caller is an LLM.

### 5.1 The M×N integration explosion
Covered above. Every model/tool pair needs bespoke code. The cost is quadratic and
the maintenance burden is where most internal agent projects quietly die.

### 5.2 No runtime discovery
An API has no standard way to answer "what can you do?" The tool list must be
compiled into the client. An agent literally **cannot** use a tool nobody
pre-registered. With MCP, connecting a new server makes its tools available to the
model immediately — no redeploy.

### 5.3 Documentation is written for humans, not models
OpenAPI tells you `status` is a string enum. It does not tell you that `"pending"`
means payment cleared but shipping hasn't started, or that you must call
`/reserve` before `/checkout`. That knowledge lives in prose docs or a senior
engineer's head. MCP tool descriptions are explicitly authored as model-facing
instructions, so intent travels with the tool.

### 5.4 Every API is a different shape
REST vs GraphQL vs gRPC. Bearer tokens vs HMAC signatures vs OAuth. Errors as HTTP
status codes vs a `200` with `{"error": ...}` in the body. Cursor pagination vs
offset vs page tokens. Snake_case vs camelCase. Every one of these differences
becomes handwritten normalisation code. MCP gives one error convention, one call
convention, one schema convention.

### 5.5 Brittle coupling — the version treadmill
Hard-coded field names break when the provider renames or deprecates them. The
weather script in this folder is a live example: it depends on Open-Meteo's exact
field `precipitation_probability_max`. A rename breaks it silently at the parse
step. With MCP the schema is fetched at connect time, so the client sees the
current contract rather than a stale assumption from six months ago.

### 5.6 Statelessness and lost context
REST is stateless by design — a strength for scaling, a weakness for agents. Each
call is isolated, so multi-step workflows need the client to carry all state
manually. MCP sessions are persistent and negotiate capabilities up front, which
fits multi-turn agentic work far better.

### 5.7 Credential sprawl
N APIs means N keys embedded in the agent application, each with its own rotation
schedule and blast radius. An MCP server owns its own credentials; the client
holds a connection, not a vault. Remote MCP servers standardise on OAuth 2.1.

### 5.8 Context-window waste
Cramming dozens of full API specs into a system prompt burns tokens on tools that
will not be used in this conversation. MCP lets the client list tools compactly
and fetch detail on demand.

### 5.9 No standard for non-tool context
APIs return data. There is no convention for "here is a document the model should
read" or "here is a prompt template the user can invoke." MCP's **resources** and
**prompts** primitives cover exactly that gap.

### 5.10 Slow iteration
Changing which tools an agent has means a code change, a review, and a deploy. With
MCP it is a configuration edit and a reconnect. For a field that moves as fast as
agentic AI, that difference compounds.

---

## 6. Honest counterpoint — where APIs still win

A comparison that only lists one side's flaws is not analysis. Direct API calls
remain the right choice when:

- **The workflow is fixed and deterministic.** A payment webhook does not need a
  model deciding anything. Determinism beats flexibility.
- **Latency and throughput matter.** MCP adds a protocol hop and a negotiation
  round-trip. For millions of calls per second, call the API.
- **Maturity matters.** APIs have decades of gateways, rate limiters, observability,
  SDKs, and battle-tested auth. MCP tooling is young by comparison.
- **No LLM is involved.** MCP's entire value proposition is a model in the loop. A
  cron job syncing two databases gains nothing from it.
- **Security surface.** A misconfigured MCP server can hand an agent broad
  capabilities; prompt injection through tool descriptions or returned data is a
  real and actively researched risk class. Narrow, purpose-built API calls have a
  smaller attack surface.

**And the decisive point: it is not either/or.** MCP servers are overwhelmingly
thin wrappers over existing APIs. The API does the work; MCP makes it reachable by
a model. You keep both.

---

## 7. Decision guide

| If you need… | Use |
|---|---|
| Deterministic, high-volume, fixed integration | **API** |
| An LLM agent to use a tool it wasn't compiled against | **MCP** |
| One tool reachable from many AI clients | **MCP** |
| Lowest possible latency | **API** |
| Tools that change often without redeploying | **MCP** |
| To expose files/docs as model-readable context | **MCP** (resources) |
| Machine-to-machine with no model involved | **API** |

---

## 8. Concrete illustration

**Task:** let an AI assistant read the weather for Bhubaneswar.

**API route** — what [`weather_predictor/bhubaneswar_weather.py`](weather_predictor/bhubaneswar_weather.py) does:

1. Developer reads Open-Meteo docs.
2. Developer hard-codes the URL and every parameter name.
3. Developer copies the WMO weather-code table into the client.
4. Developer writes parsing for the exact response shape.
5. To let a model use it: write a wrapper, hand-author a JSON schema, add a
   dispatch branch, redeploy. Repeat for every AI client that wants it.

**MCP route:**

1. Wrap the same `fetch` / `parse_days` functions in an MCP server, one tool named
   `get_bhubaneswar_forecast` with a description saying what it is for.
2. Add the server to any MCP client's config.
3. Every MCP-speaking model — Claude Desktop, Claude Code, an IDE, a custom agent —
   now has the tool. No client-side code was written for any of them.

Step 5 versus steps 2–3 is the entire argument.

---

## 9. Summary

- An **API** is how software talks to software; **MCP** is how models talk to the world.
- MCP's central win is turning an **M×N** connector problem into **M+N**.
- Plain APIs, used as an agent's tool layer, suffer from no runtime discovery,
  human-only documentation, inconsistent shapes, brittle version coupling,
  statelessness, credential sprawl, and slow iteration.
- APIs remain better for deterministic, high-throughput, non-LLM work, and they are
  more mature.
- The two are complementary: **MCP is a standardised, model-facing wrapper around
  APIs**, not a competitor to them.

---

## References

- Model Context Protocol — specification and docs: <https://modelcontextprotocol.io>
- MCP introduction (Anthropic, Nov 2024): <https://www.anthropic.com/news/model-context-protocol>
- MCP server directories: <https://mcpservers.org>, <https://mcpmarket.com>
- JSON-RPC 2.0 specification: <https://www.jsonrpc.org/specification>
- Open-Meteo API (used in the companion project): <https://open-meteo.com>
