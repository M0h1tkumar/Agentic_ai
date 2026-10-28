# Difference Between STDIO and Streamable HTTP

## Introduction

MCP needs some kind of transport to actually move messages between an MCP client and an MCP server. Two transports matter most in practice: **STDIO** and **Streamable HTTP**. Both let a client and server exchange MCP messages, but they're built for different situations — one for local communication, one for networked communication.

## STDIO

**STDIO (Standard Input/Output)** is a transport where the MCP client starts the MCP server as a local process on the same machine, and the two talk to each other through the process's standard input (`stdin`) and standard output (`stdout`). There's no network port involved — it's all happening on one machine.

```text
AI Application
      |
      | stdin / stdout
      v
MCP Server Process
      |
      v
Local Tool / Service
```

For example, an AI app like OpenCode can start a Weather MCP server directly as a subprocess, which in turn talks to AccuWeather.

A typical STDIO configuration looks like this:

```json
{
  "mcpServers": {
    "weather": {
      "command": "npx",
      "args": ["-y", "@timlukahorstmann/mcp-weather"],
      "env": {
        "ACCUWEATHER_API_KEY": "YOUR_API_KEY"
      }
    }
  }
}
```

The client launches the server locally using that command, and communication happens over stdin/stdout from there.

### Advantages of STDIO

- Very simple to set up — no HTTP server or network configuration needed
- Low overhead, since everything runs on one machine
- Great for local development, testing, and command-line tools
- Easy to run on a single developer machine

### Disadvantages of STDIO

- Designed for local communication, not remote access
- The client generally needs to start and manage the server process
- Not a natural fit for sharing one server across many remote clients
- Requires you to manage the process lifecycle yourself

## Streamable HTTP

**Streamable HTTP** is an MCP transport that uses the HTTP protocol to communicate between client and server. The server runs as a network service — it can expose an endpoint like `https://example.com/mcp` — and the client talks to it over HTTP rather than starting it as a local process.

```text
AI Application
      |
      | HTTP
      v
   MCP Server
      |
      v
External Service
```

For example, OpenCode could send an HTTP request to a remote MCP server, which then talks to the GitHub API on its behalf.

### Advantages of Streamable HTTP

- Works with remote MCP servers, not just local ones
- Fits naturally into cloud deployments
- One server can be shared across multiple clients
- Can use standard HTTP infrastructure — auth, gateways, proxies, load balancers
- Suitable for enterprise and production environments

### Disadvantages of Streamable HTTP

- Needs more infrastructure than STDIO
- Requires network connectivity to function
- Authentication and authorization need to be configured properly
- More moving parts overall, including deployment and security concerns
- Network issues can directly affect communication

## Comparison Table

| Feature | STDIO | Streamable HTTP |
|---|---|---|
| Full Form | Standard Input/Output | HTTP-based MCP transport |
| Communication | stdin/stdout | HTTP requests |
| Network Required | No | Yes |
| Server Location | Usually local | Local or remote |
| Process Model | Client starts server process | Server runs as a network service |
| Setup | Simple | More infrastructure |
| Remote Access | Not suitable | Suitable |
| Multiple Clients | Limited | Well suited |
| Authentication | Process/environment based | HTTP authentication mechanisms |
| Best Suited For | Local MCP tools | Remote and web-based MCP services |

## When to Use Which

**Use STDIO when:**
- The MCP server runs locally
- You're developing or testing an MCP server
- The AI application can launch the process itself
- No remote access is needed
- Simplicity matters more than scale

**Use Streamable HTTP when:**
- The MCP server is remote
- Multiple clients need access to the same server
- The server is deployed in the cloud
- Authentication is required
- You're working within enterprise infrastructure

In short: for local learning and development, STDIO is the natural choice; for production or any remotely accessible MCP service, Streamable HTTP is the better fit. The right pick really comes down to where the server needs to live and who needs to reach it.

## A Note on SSE

Earlier versions of MCP used an HTTP + Server-Sent Events (SSE) approach for network communication. The protocol has since moved toward Streamable HTTP as the standard, and the July 2026 specification update formally deprecated the legacy HTTP+SSE transport (with a transition period for existing implementations). New MCP projects should use Streamable HTTP rather than the older HTTP+SSE approach.

## Conclusion

STDIO and Streamable HTTP both connect an MCP client to an MCP server — they just solve different problems. STDIO is local, simple, and fast, which makes it ideal for development and single-machine setups. Streamable HTTP is network-based, scalable, and built for production, which makes it the right choice when a server needs to be remote or shared across multiple clients. The official MCP SDK supports both, so the decision comes down to deployment needs rather than one being universally "better."