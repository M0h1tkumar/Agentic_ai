# 1. STDIO vs Streamable HTTP

## Overview

MCP (Model Context Protocol) uses a transport layer to move JSON-RPC messages between an MCP client and MCP server. The two standard transports are:

1. **STDIO**
2. **Streamable HTTP**

Both carry MCP/JSON-RPC messages, but they are designed for different deployment scenarios. citeturn0search0turn0search3

## STDIO

With STDIO, the MCP client launches the MCP server as a subprocess.

The communication flow is:

```text
MCP Client
    |
    | launches
    v
MCP Server Process
    |              |
 stdin            stdout
    |              |
 requests ------> responses
```

The server reads JSON-RPC messages from `stdin` and writes JSON-RPC messages to `stdout`. Logging can be written to `stderr`. The server must not write non-MCP output to `stdout`, because that would corrupt the protocol stream. citeturn0search0

### Characteristics

- Usually used for **local MCP servers**.
- The client manages the server process lifecycle.
- Communication happens through operating-system standard input/output streams.
- No HTTP server or network port is required.
- Simple to run locally.
- Good fit for tools such as local filesystem, local development tools, or command-line utilities.

## Streamable HTTP

With Streamable HTTP, the MCP server runs as an independent HTTP service.

The client sends MCP JSON-RPC messages to an MCP endpoint using HTTP POST. Depending on the protocol revision and response, the server can return a normal JSON response or an SSE stream for streaming results. The current 2026-07-28 specification uses a single POST endpoint and has changed some behavior from earlier revisions. citeturn0search4

Example:

```text
MCP Client
    |
    | HTTP POST /mcp
    v
MCP Server
    |
    | JSON response / SSE stream
    v
MCP Client
```

### Characteristics

- Designed for **remote or network-accessible MCP servers**.
- Server runs independently of the client process.
- Uses normal HTTP infrastructure.
- Multiple clients can connect to the same server.
- Easier to deploy behind gateways, authentication systems, load balancers, etc.
- Requires proper network security.

## Main Difference

| Feature | STDIO | Streamable HTTP |
|---|---|---|
| Communication | stdin/stdout | HTTP |
| Server lifecycle | Client launches subprocess | Independent server |
| Typical use | Local | Remote/networked |
| Multiple clients | Usually one client per process | Multiple clients |
| Network required | No | Yes |
| Endpoint | None | HTTP MCP endpoint |
| Authentication | Usually environment/process credentials | HTTP authentication mechanisms can be used |
| Deployment | Simple local process | Web/server infrastructure |
| Streaming | Through the stream itself | JSON response or SSE response stream |
| Best for | Local tools | Remote/shared services |

MCP's architecture documentation also describes local STDIO servers as typically serving a single MCP client, while remote Streamable HTTP servers typically serve many clients. citeturn0search12

## When Should You Use Which?

### Use STDIO when:

```text
AI Application
     |
     +----> local MCP server
             |
             +----> local files
             +----> local database
             +----> local scripts
```

Use STDIO when the MCP server is trusted, local, and controlled by the same machine/application.

### Use Streamable HTTP when:

```text
Client A ----Client B -----+----> MCP Server
Client C ----/
```

Use Streamable HTTP when the server needs to be independently deployed and accessed over a network.

## Important Security Point

Streamable HTTP is not automatically secure simply because it uses HTTP.

The MCP specification requires security considerations such as validating the `Origin` header to prevent DNS rebinding attacks. Local HTTP servers should generally bind to `127.0.0.1` rather than all interfaces, and proper authentication should be implemented where appropriate. citeturn0search4
