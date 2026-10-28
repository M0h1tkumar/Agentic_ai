# Model Context Protocol (MCP) — Research Summary

*Compiled August 2026*

## What It Is

MCP is an open protocol, originally released by Anthropic in November 2024, that defines how AI models communicate with external data sources, tools, and systems. It enables seamless integration between LLM applications and external data sources and tools, providing a standardized way to connect LLMs with the context they need — whether for an AI-powered IDE, a chat interface, or custom AI workflows.

It's often compared to USB-C: one common connector instead of a different integration for every tool.

### Core Primitives

MCP is built around three core primitives:

- **Resources** – data an AI model can read (files, databases, APIs)
- **Tools** – actions the model can execute (search, write files, call APIs)
- **Prompts** – reusable prompt templates with dynamic parameters

## Adoption

Growth has been dramatic:

- Across Tier 1 SDKs, MCP is seeing close to half-a-billion downloads a month
- Both the TypeScript and Python SDKs have crossed 1 billion total downloads
- It has become one of the key building blocks of the agentic AI stack — a common language for models to connect with external tools, files, and business systems
- Typical use cases: pulling a file from Drive, querying a database, checking a GitHub issue, or triggering an action in an internal app

## Major Recent Change: The 2026-07-28 Spec

This is the biggest news in the MCP world right now — the largest revision of the protocol since launch.

### Key changes

**Stateless protocol core**
The protocol moved from stateful to stateless design. This reflects "hard lessons" learned as MCP servers moved from personal laptops into multi-client enterprise cloud deployments, where the original stateful design created scalability problems.

**Header-based routing**
Streamable HTTP now requires `Mcp-Method` and `Mcp-Name` headers so load balancers, gateways, and rate-limiters can route on the operation without inspecting the request body. Servers reject requests where headers and body disagree.

**Tasks moved out of core**
The Tasks feature (for long-running operations) has been moved out of the core protocol and into an extension. Users can also build their own extensions following the spec's guidance.

**Backward compatibility risk**
Deprecated features stay functional for at least 12 months, but this is not a blanket interoperability guarantee — servers built on 2026-07-28 may not work with older clients, and vice versa.

**Other additions**
- Cacheable list results
- Authorization hardening
- Formal extensions framework
- MCP Apps (server-rendered UIs)

## 2026 Roadmap Themes

Beyond the spec release, the broader 2026 roadmap centers on four priority areas:

1. Transport scalability
2. Agent communication
3. Governance maturation
4. Enterprise readiness

Working Groups and Spec Enhancement Proposals (SEPs) now serve as the primary vehicle for protocol development, rather than routing through a small core team.

## Ecosystem

Existing MCP servers include:

- Filesystem access (read/write local files)
- GitHub (search repos, create PRs)
- Postgres (query databases)
- Brave Search (web search)
- Slack (read channels, send messages)
- Hundreds more built by the community

SDKs are available in multiple languages (TypeScript, Python, and others), maintained at different support tiers.

## Known Concerns

Security researchers have identified outstanding issues with MCP, including:

- **Prompt injection** risks
- **Tool permission combination** — where legitimate tool permissions can be combined to exfiltrate data
- **Lookalike tools** — malicious tools that can silently replace trusted ones

Enterprises adopting MCP at scale should factor these into their security review process.

## Sources

- Model Context Protocol Blog — "The 2026 MCP Roadmap" (March 2026)
- Model Context Protocol Blog — "The 2026-07-28 Specification" (July 2026)
- modelcontextprotocol.io — Official Specification (v2026-07-28)
- The Register — "Model Context Protocol prepares to break with its stateful past" (July 2026)
- The New Stack — "MCP's biggest growing pains for production use will soon be solved" (March 2026)
- Wikipedia — Model Context Protocol
- HyperNest Labs — "Model Context Protocol (MCP) 2026: Complete Developer Guide" (March 2026)
