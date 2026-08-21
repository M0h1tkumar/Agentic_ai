# 2. Research: Model Context Protocol (MCP)

## What is MCP?

**Model Context Protocol (MCP)** is an open protocol for connecting AI applications to external tools, resources, prompts, and other context.

The important idea is that MCP standardizes the **interface between an AI application and external capabilities** instead of forcing every AI application to build a custom integration for every tool.

MCP follows a host-client-server architecture and uses JSON-RPC for protocol messages. citeturn0search8turn0search11

## The Problem MCP Solves

Without MCP, an AI application may need custom code for every integration:

```text
AI Application
   |
   +---- custom code ---> GitHub
   |
   +---- custom code ---> Database
   |
   +---- custom code ---> Slack
   |
   +---- custom code ---> File System
```

As the number of tools increases, this becomes difficult to maintain.

MCP provides a standardized protocol:

```text
                 MCP
                  |
AI Application ---+--- GitHub MCP Server
                  |
                  +--- Database MCP Server
                  |
                  +--- File System MCP Server
                  |
                  +--- Other MCP Servers
```

The AI application can communicate with different MCP servers through the same protocol model.

## MCP Architecture

The major components are:

### 1. MCP Host

The **Host** is the AI application that coordinates MCP connections.

Examples conceptually include an AI coding assistant or desktop AI application.

The host:

- Creates and manages MCP clients.
- Controls connection lifecycle.
- Enforces permissions and security policies.
- Coordinates LLM integration.
- Aggregates context from multiple MCP clients. citeturn0search8

### 2. MCP Client

An MCP client is the component inside the host that communicates with a particular MCP server.

The relationship is approximately:

```text
Host
 |
 +--- Client A ---> MCP Server A
 |
 +--- Client B ---> MCP Server B
 |
 +--- Client C ---> MCP Server C
```

Each client maintains the connection/protocol interaction with its corresponding server. citeturn0search8

### 3. MCP Server

An MCP server provides capabilities to the AI application.

A server can expose:

- **Tools**
- **Resources**
- **Prompts**

Servers are intended to have focused responsibilities and can run locally or remotely. citeturn0search8

## MCP Primitives

### Tools

Tools are executable operations.

Examples:

```text
search_database()
create_file()
send_email()
query_api()
run_command()
```

The model can decide that it needs a tool and request its execution through the MCP architecture.

### Resources

Resources represent contextual data that an application can retrieve.

Examples:

```text
file://project/README.md
database://users/schema
docs://api/reference
```

Resources are about **providing context/data**, rather than directly performing an action.

### Prompts

Prompts are reusable prompt templates exposed by an MCP server.

For example:

```text
code_review_prompt
bug_analysis_prompt
documentation_prompt
```

They allow applications to discover and use structured prompt templates.

## Transport Layer

MCP currently defines standard transports including:

- STDIO
- Streamable HTTP

Both transport MCP JSON-RPC messages, but their deployment models differ. citeturn0search0turn0search3

## JSON-RPC

MCP uses JSON-RPC to encode protocol messages.

Conceptually:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {}
}
```

A tool call conceptually looks like:

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "search_database",
    "arguments": {
      "query": "users"
    }
  }
}
```

The exact message schema is defined by the MCP specification.

## MCP vs Normal API

A normal API integration might look like:

```text
Application
    |
    +---- HTTP request ----> /users
```

MCP provides a standardized protocol layer around AI-to-tool/context interaction:

```text
AI Application
      |
   MCP Client
      |
   MCP Protocol
      |
   MCP Server
      |
   Tool / Resource / Prompt
```

MCP is therefore not simply "another REST API." It defines a standardized interaction model for AI applications and external capabilities.

## MCP and RAG

MCP and RAG are different concepts.

### RAG

RAG generally means:

```text
Documents
   |
Chunking
   |
Embeddings
   |
Vector Database
   |
Similarity Search
   |
Context
   |
LLM
```

### MCP

MCP provides a standardized way for an AI application to interact with external capabilities:

```text
LLM Application
      |
   MCP Client
      |
   MCP Server
      |
 +----+---------+
 |    |         |
Tool Resource Prompt
```

An MCP server could itself provide access to a retrieval system, but **MCP is not a replacement for vector databases or RAG**.

## MCP and Multi-Agent Systems

MCP can be used as an integration layer in a multi-agent architecture, but MCP itself is **not a multi-agent framework**.

For example:

```text
                 Orchestrator Agent
                        |
                 MCP Client Layer
              /         |                      /          |                MCP Server A  MCP Server B  MCP Server C
          |             |             |
       Research       Database      Developer
        Tools           Tools         Tools
```

The orchestrator can use MCP to access external capabilities, while the actual agent coordination logic belongs to the application/framework.

This distinction matters:

> **MCP standardizes tool/context connectivity. It does not automatically create agent planning, delegation, or orchestration.**

## Advantages

- Standardized AI-to-tool integration.
- Clear client/server separation.
- Local and remote transport options.
- Reusable MCP servers.
- Capability discovery.
- Security boundaries between host/client/server components.
- Easier integration of multiple external systems.

## Limitations / Things MCP Does Not Solve

MCP does not automatically solve:

- Agent planning.
- Agent memory.
- Agent hierarchy.
- Multi-agent delegation.
- LLM reasoning quality.
- Business workflow design.
- Database/vector-store implementation.
- Authentication architecture for every deployment.
- Tool safety by itself.

You still need to design those parts.

## Security

MCP security depends heavily on the transport and server implementation.

For HTTP-based MCP, authentication and authorization need to be designed correctly. The MCP specification specifically calls out protections such as Origin validation and protection against DNS rebinding. citeturn0search4turn0search11

A dangerous architecture would be:

```text
Internet
   |
   v
Unprotected MCP Server
   |
   +---- filesystem
   +---- shell
   +---- database
```

An attacker who can invoke unrestricted tools could potentially cause serious damage.

## Key Points

1. MCP is a protocol for AI application ↔ external capability/context integration.
2. MCP uses JSON-RPC messages.
3. The architecture contains Host, Client, and Server components.
4. Servers can expose tools, resources, and prompts.
5. STDIO is primarily useful for local process-based integration.
6. Streamable HTTP is useful for independently deployed/networked servers.
7. MCP is not the same thing as RAG.
8. MCP is not itself a multi-agent framework.
9. Security and authorization remain application responsibilities.
10. MCP becomes particularly useful when an AI application needs to interact with many standardized external systems.
