# STDIO vs Streamable HTTP (MCP Transports)

MCP defines exactly two standard transport mechanisms for how a client and an MCP server exchange JSON-RPC messages: **stdio** and **Streamable HTTP**. Both carry the same JSON-RPC 2.0 message format — the difference is entirely in *how* those messages physically move between client and server.

## STDIO Transport

- The **client launches the MCP server as a local subprocess** — there's no network involved at all.
- The server reads incoming JSON-RPC messages from its **stdin** and writes responses to its **stdout**.
- Messages are plain JSON-RPC requests/notifications/responses, delimited by newlines (no embedded newlines allowed within a single message).
- The server may write logs to **stderr**; the client can capture or ignore that freely — stderr output isn't assumed to mean an error occurred.
- The connection lifecycle is simple: launch subprocess → exchange messages over stdin/stdout → client closes stdin and terminates the subprocess when done.

**Why use it:** zero network overhead, no ports to open, no auth handshake — it's the natural fit when the server runs *on the same machine* as the client (e.g. a local dev tool, a CLI-integrated MCP server). This is why the spec says clients **should** support stdio whenever possible.

## Streamable HTTP Transport

- The server runs as an **independent, long-lived process** that can serve **multiple clients** over the network, exposing a single HTTP endpoint (e.g. `https://example.com/mcp`) that accepts both `POST` and `GET`.
- **Sending a message to the server:** the client `POST`s a single JSON-RPC request/notification/response to the MCP endpoint, with an `Accept` header listing both `application/json` and `text/event-stream`. The server replies either with one plain JSON object, or by opening a **Server-Sent Events (SSE)** stream if it needs to send multiple messages (progress updates, nested requests) before the final response.
- **Listening for server-initiated messages:** the client can also issue a `GET` to open a standing SSE stream, letting the server push messages without waiting for a client request first.
- **Sessions:** the server can assign a session ID at initialization via an `MCP-Session-Id` header; the client must echo that header on every subsequent request. Sessions can be explicitly ended with an HTTP `DELETE`.
- **Resumability:** SSE events can carry an ID; if a connection drops, the client reconnects with a `Last-Event-ID` header so the server can replay only what was missed — avoiding message loss over an unreliable network link.
- **Security requirements baked into the spec:** servers must validate the `Origin` header (to prevent DNS-rebinding attacks), should bind to `localhost` only when running purely locally, and should implement real authentication for network-reachable deployments.

**Why use it:** it's the transport for **remote** MCP servers — anything not running on the client's own machine — since it works over standard HTTP/HTTPS infrastructure (proxies, load balancers, TLS) and supports normal HTTP auth (bearer tokens, API keys, custom headers).

> Note: Streamable HTTP replaced an earlier, separate "HTTP+SSE" transport from the 2024-11-05 version of the spec. That older transport is now deprecated; the current spec only recommends stdio (local) and Streamable HTTP (remote) as the two standard options.

## Side-by-Side

| | STDIO | Streamable HTTP |
|---|---|---|
| Where the server runs | Same machine, spawned as a subprocess | Anywhere reachable over HTTP — local or remote |
| Transport medium | Process stdin/stdout | HTTP POST/GET, optionally upgraded to SSE for streaming |
| Network overhead | None | Standard HTTP latency/overhead |
| Multiple concurrent clients | No — one subprocess per client session | Yes — a single server process can serve many clients |
| Authentication | Implicit (whoever can launch the process) | Explicit — bearer tokens, API keys, custom headers |
| Session management | Not needed — process lifetime *is* the session | Explicit `MCP-Session-Id` header, can be resumed after disconnect |
| Best fit | Local dev tools, CLI-integrated servers, local prototyping | Hosted/shared MCP servers, anything crossing a network boundary |

## Takeaway

stdio is the simple, zero-overhead choice when the MCP server and client live on the same machine — no auth, no networking, just pipes. Streamable HTTP is the standardized way to reach an MCP server over a network, adding proper session management, resumable streaming via SSE, and normal HTTP-based authentication — the tradeoff being the added complexity that any networked protocol requires.

---

### Sources
- [Transports — Model Context Protocol specification](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports)
- [MCP Server Transports: STDIO, Streamable HTTP & SSE — Roo Code Documentation](https://docs.roocode.com/features/mcp/server-transports)
- [MCP Transport: Stdio vs Streamable HTTP — TrueFoundry](https://www.truefoundry.com/blog/mcp-stdio-vs-streamable-http-enterprise)
