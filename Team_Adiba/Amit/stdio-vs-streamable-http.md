# STDIO vs Streamable HTTP

Both are **transport mechanisms** — ways for a client and a server (or a client and a subprocess) to exchange messages. They're most commonly discussed today in the context of the **Model Context Protocol (MCP)**, but the underlying ideas apply to any client-server communication.

## Quick Comparison

| Aspect | STDIO | Streamable HTTP |
|---|---|---|
| **Transport medium** | Standard input/output streams of a local process | HTTP requests/responses over a network |
| **Process model** | Client spawns the server as a **child process** | Server runs **independently**, client connects to it |
| **Location** | Same machine only (local) | Local or remote (over a network) |
| **Connection type** | Persistent pipe (stdin/stdout) | HTTP connection, can be long-lived (streaming) or short-lived |
| **Message format** | Newline-delimited JSON-RPC messages | JSON-RPC messages sent over HTTP POST, with optional Server-Sent Events (SSE) for streaming |
| **Concurrency** | One client per server process (1:1) | Many clients can connect to one server (1:many) |
| **Authentication** | Not needed — process-level trust (OS handles it) | Needed — API keys, OAuth, headers, etc. |
| **Setup complexity** | Simple — just launch the executable | More complex — needs a server, ports, networking |
| **Latency** | Very low (in-memory pipes) | Higher (network round trip), though same-host is fast |
| **Typical use case** | Local tools, CLI integrations, desktop apps | Web services, remote APIs, multi-user/multi-client systems |
| **Lifecycle** | Tied to the parent process; dies when parent exits | Independent lifecycle; server can run continuously |
| **Scalability** | Not scalable beyond the local machine | Scalable — load balancers, multiple server instances |

## STDIO (Standard Input/Output)

- The client **launches the server as a subprocess** and communicates by writing to its `stdin` and reading from its `stdout`.
- Messages are typically JSON-RPC objects, one per line.
- `stderr` is often used for logging, separate from the protocol channel.
- Because it's just a local pipe, there's no network stack, no ports, and no auth layer — the OS process boundary is the trust boundary.
- **Best for:** local integrations, e.g., a desktop app talking to a locally-installed MCP server, CLI tools, editor plugins.

**Pros:**
- Extremely simple to implement and reason about
- Very low latency
- No network configuration or security surface

**Cons:**
- Only works locally — client and server must be on the same machine
- One server instance per client (no sharing across multiple clients)
- If the client crashes or exits, the server process typically dies with it

## Streamable HTTP

- The server runs as its **own independent process** (e.g., a web service), listening on an HTTP endpoint.
- The client sends requests via HTTP **POST**; the server can respond with a single JSON response *or* upgrade to a **stream** (using Server-Sent Events) to push multiple messages over time — useful for long-running operations, progress updates, or server-initiated messages.
- This replaced the older two-endpoint "HTTP+SSE" transport in MCP with a single, simpler endpoint that can act as both a normal request/response channel and a streaming channel.
- **Best for:** remote servers, multi-tenant services, cloud-hosted tools, anything where the server needs to be accessed by multiple clients or from a different machine than the client.

**Pros:**
- Works across networks — client and server don't need to be co-located
- One server can serve many clients simultaneously
- Standard HTTP infrastructure applies: load balancers, auth (bearer tokens/OAuth), TLS, logging, rate limiting
- Server lifecycle is decoupled from any single client

**Cons:**
- More setup and operational overhead (hosting, ports, TLS certs, auth)
- Higher latency than a local pipe
- Larger attack surface — needs proper authentication/authorization

## Languages / SDKs Commonly Used

MCP provides official SDKs, so servers can be written in several languages. Both transports are supported by the same SDKs — the language choice is independent of the transport choice.

| Language | SDK | Notes |
|---|---|---|
| **Python** | `mcp` (official Python SDK) | Very common for STDIO servers — quick to spin up as a local subprocess; also supports Streamable HTTP via frameworks like FastAPI/Starlette |
| **TypeScript / JavaScript** | `@modelcontextprotocol/sdk` | Popular for both transports; Node.js handles STDIO easily and frameworks like Express handle Streamable HTTP |
| **Java** | Official Java SDK | Used for enterprise-style servers, often Streamable HTTP for remote/shared deployments |
| **Kotlin** | Official Kotlin SDK | Similar use cases to Java |
| **C#** | Official C# SDK | Used in .NET environments, both transports supported |

In practice:
- **STDIO servers** are most often written in **Python** or **TypeScript/Node.js** since they're quick to launch as local subprocesses.
- **Streamable HTTP servers** are commonly built with **Python (FastAPI)**, **TypeScript (Express/Node)**, or **Java/Kotlin/C#** when deployed as standalone web services, since these ecosystems have mature HTTP server tooling.

## In short

- **STDIO** = fast, simple, local-only, one-to-one — good default for local dev tools and CLI-style integrations.
- **Streamable HTTP** = flexible, networked, one-to-many, supports both request/response and streaming — good default for anything that needs to be shared, remote, or production-grade.
- Language choice (Python, TypeScript, Java, Kotlin, C#) is independent of transport — pick based on your ecosystem, not the transport type.
