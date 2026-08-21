# Research: Model Context Protocol (MCP)

## What It Is

The Model Context Protocol (MCP) is an open, standardized protocol — originally introduced by Anthropic — that defines how AI applications connect to external tools, data sources, and prompt templates. Before MCP, every AI application that wanted to call a tool or read from a data source needed its own bespoke integration for that specific tool. MCP replaces that N×M integration problem (N applications × M tools, each pair hand-wired) with a single standard both sides implement once.

## Architecture

MCP uses a client-server model built on JSON-RPC 2.0, with three roles:

- **Host** — the user-facing application (e.g. Claude Desktop, Claude Code, an IDE). The host is what the user actually interacts with.
- **Client** — lives inside the host and manages a stateful, isolated connection to one specific MCP server. A host can run several clients at once, one per connected server.
- **Server** — an external program that exposes capabilities to any connected client. A server can run locally on the user's machine (spawned as a subprocess, communicating over stdio) or remotely as a hosted service (communicating over Streamable HTTP).

When a client connects to a server, they run a **capability-negotiation handshake** — the client learns exactly which tools, resources, and prompts that server offers, and which protocol features both sides support, before any real work begins.

## Core Primitives

Every MCP server exposes its capabilities through three primitives:

1. **Tools** — functions the model can actively invoke to take an action or fetch computed results (e.g. run a search, query a database, call an external API).
2. **Resources** — read-only data the model can pull in as context (e.g. file contents, a database record, a document).
3. **Prompts** — reusable, pre-defined prompt templates that structure a common workflow, so a user or client doesn't need to hand-craft the same instruction every time.

Separating these three explicitly (rather than exposing everything as one generic "endpoint," the way a typical API does) lets a client reason about what's safe to fetch automatically for context (resources) versus what's a deliberate, potentially side-effecting action (tools).

## Local vs Remote Servers

- A **local** server runs on the same machine as the host, launched as a subprocess and talking over **stdio** — e.g. Claude Desktop spawning a filesystem MCP server to read local files.
- A **remote** server runs elsewhere (a hosted service) and talks over **Streamable HTTP** — e.g. a SaaS product's MCP server that a client connects to over the network, with normal HTTP authentication (bearer tokens, API keys).

(See [`STDIO_vs_Streamable_HTTP.md`](STDIO_vs_Streamable_HTTP.md) in this same folder for the transport-level detail.)

## Why It Matters for Agent Development

- **Reusability** — a tool built as an MCP server works with *any* MCP-compatible host, not just one specific agent framework. Write the server once, connect it anywhere.
- **Discoverability** — clients can enumerate a server's tools/resources/prompts at connection time instead of a developer hardcoding a fixed integration ahead of time.
- **Ecosystem growth** — because the protocol is open and host-agnostic, an entire ecosystem of community and vendor-built MCP servers (databases, SaaS products, dev tools, search engines) has grown around it, each usable from any compliant client without custom glue code.
- **Security model** — because tools and resources are distinct primitives with their own permission surface, hosts can implement finer-grained control over what an agent is allowed to do automatically versus what requires explicit user approval.

## Takeaway

MCP is best understood as the "USB-C port" analogy commonly used for it: a single standard connector between AI applications and the tools/data they need, replacing a mess of one-off integrations with one protocol every side implements once. Its host/client/server architecture, the tools/resources/prompts split, and its two standard transports (stdio for local, Streamable HTTP for remote) together define how that connection actually works in practice.

---

### Sources
- [Architecture overview — Model Context Protocol](https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture)
- [Model Context Protocol (MCP) explained: A practical technical overview — CodiLime](https://codilime.com/blog/model-context-protocol-explained/)
- [Model Context Protocol (MCP): an overview — Phil Schmid](https://www.philschmid.de/mcp-introduction)
- [Transports — Model Context Protocol specification](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports)
