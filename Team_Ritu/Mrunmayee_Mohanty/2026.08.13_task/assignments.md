# STDIO vs Streamable HTTP in MCP

MCP supports different ways for an **MCP client** to communicate with an **MCP server**. Two important transports are **STDIO** and **Streamable HTTP**.

## 1. STDIO

**STDIO (Standard Input/Output)** is mainly used when the MCP server runs **locally on the same machine** as the MCP client.

The client starts the MCP server as a process and communicates with it through `stdin` and `stdout`.


Local Tools

**Example:** A coding agent running a local filesystem MCP server.

### Best suited for:

* Local development
* Local tools and files
* Simple, private integrations

---

## 2. Streamable HTTP

**Streamable HTTP** allows an MCP client to communicate with an MCP server through **HTTP**. The server can therefore run on another machine or on a remote/cloud server.


### Best suited for:

* Remote MCP servers
* Cloud deployments
* Multiple clients connecting to one server
* Production environments

---

## Key Difference

| Feature         | STDIO                | Streamable HTTP         |
| --------------- | -------------------- | ----------------------- |
| Connection      | Local process        | HTTP connection         |
| Server location | Usually same machine | Can be remote           |
| Network         | Not required         | Required for remote use |
| Best for        | Local tools          | Remote/cloud tools      |
| Example         | Local filesystem     | Remote GitHub service   |
