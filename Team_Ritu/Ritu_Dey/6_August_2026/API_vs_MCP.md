# API vs MCP (Model Context Protocol)

## What is an API

An API (Application Programming Interface) is a general-purpose contract that lets one piece of software call another — a defined set of endpoints, request/response shapes, and an authentication method (API key, OAuth, etc.). APIs predate AI agents entirely; they were designed for software talking to software (a mobile app calling a backend, one microservice calling another). Every API has its own conventions: REST vs GraphQL vs gRPC, its own auth style, its own pagination and error format.

## What is MCP

MCP (Model Context Protocol) is a standardized protocol, introduced by Anthropic, specifically for connecting AI models/agents to external tools, data sources, and prompts. An MCP **server** exposes its capabilities — tools it can execute, resources it can provide as context, and reusable prompt templates — in a single standard schema. Any MCP-compatible **client** (Claude Desktop, Claude Code, or any other MCP host) can connect to that server, discover what it offers at runtime, and call it, all through the same protocol regardless of which server it is.

## Core Difference

| Aspect | API | MCP |
|---|---|---|
| Designed for | Software-to-software communication in general | AI models/agents connecting to tools and data specifically |
| Discovery | None built in — a developer must read documentation and hand-write the integration | Built in — a client can query the server for its available tools/resources/prompts at runtime |
| Standardization | Every API has its own conventions (REST/GraphQL/SOAP/gRPC, custom auth, custom error formats) | One standard protocol (JSON-RPC based) used by every MCP server, regardless of what it wraps |
| Integration effort | New custom client/wrapper code required per API | One MCP client implementation works with any MCP server, no per-server glue code |
| What it exposes | Just endpoints/operations | Explicitly separates **tools** (actions), **resources** (context/data), and **prompts** (reusable templates) |
| Reuse across agents | Low — each agent framework needs its own bespoke integration per API | High — any MCP-aware agent can plug into any MCP server immediately |

## Drawback of API Over MCP

In the context of building AI agents, plain APIs have real disadvantages compared to MCP:

- **No self-description for the model.** An API doesn't tell an LLM what it can do — a developer has to manually translate the API's documentation into a function-calling/tool schema by hand, for every single endpoint they want the agent to use.
- **Fragmented conventions multiply integration work.** Because every API has its own auth style, request format, and error handling, none of that glue code is reusable — integrating 10 different APIs means writing and maintaining 10 different wrappers. MCP servers all speak the same protocol, so one client implementation covers all of them.
- **No runtime discovery.** An agent can't ask an arbitrary API "what can you do?" — the available operations must already be known and hardcoded ahead of time. MCP clients can enumerate a server's tools/resources dynamically.
- **Tight coupling to a specific shape.** When an API changes its response format or versions its endpoints, the hand-written integration code breaks and needs manual fixing. MCP's standardized schema insulates the agent side from those kinds of underlying implementation changes.
- **No native concept of "context vs action."** A regular API just exposes operations; it doesn't distinguish between something safe to read for context (a resource) and something that performs a side-effecting action (a tool). MCP bakes that distinction in, which matters for reasoning about what an autonomous agent should be allowed to do.
- **Composability is harder.** Wiring multiple APIs into a single agent session means stitching together several bespoke integrations. Wiring multiple MCP servers into a session is just adding more servers to the same client — no additional integration logic per server.

## Takeaway

An API is a general contract for two programs to talk to each other; MCP is a protocol layered specifically for AI agents to discover and use tools/data in a standardized, self-describing way. Where APIs require custom integration effort for every new connection, MCP trades that upfront wrapper work for a shared standard — which is exactly what makes it easier to plug an agent into many different tools without writing a new adapter each time.