# Model Context Protocol (MCP)

## Introduction

Model Context Protocol (MCP) is an open protocol that allows AI applications to connect to external tools, data sources, and services in a standardized way.

Instead of building a separate integration for every AI application and every external service, MCP provides a common protocol that can be used by AI applications, MCP clients, and MCP servers.

MCP is especially useful for AI Agents because agents often need to access external systems such as:

* Web search
* Databases
* APIs
* File systems
* GitHub
* Weather services
* Knowledge bases
* Business applications

---

## Why MCP Is Needed

Without MCP, an AI application may need a custom integration for every service.

For example:

```text
AI Agent
   |
   +---- Custom Weather API Integration
   |
   +---- Custom GitHub Integration
   |
   +---- Custom Database Integration
   |
   +---- Custom Search Integration
```

This becomes difficult to maintain as the number of tools increases.

MCP provides a standardized interface:

```text
                    MCP
                     |
        +------------+------------+
        |            |            |
     Weather       GitHub       Database
      Server        Server        Server
```

The AI application can connect to different MCP servers using the same general protocol.

---

## Basic Architecture

A typical MCP system contains:

```text
User
  |
  v
AI Application / Host
  |
  v
MCP Client
  |
  +-------------------+
  |                   |
  v                   v
MCP Server         MCP Server
  |                   |
  v                   v
Weather API        Database
```

### Host

The host is the AI application that provides the environment in which the model operates.

Examples can include:

* Agent runtimes
* Coding assistants
* Desktop AI applications
* AI development tools

### MCP Client

The MCP client manages communication between the host application and an MCP server.

### MCP Server

An MCP server exposes capabilities that an AI application can use.

For example:

```text
Weather MCP Server
       |
       +---- current_weather
       |
       +---- forecast
```

---

## MCP Primitives

MCP defines three important primitives.

| Primitive | Controlled By | Purpose                           |
| --------- | ------------- | --------------------------------- |
| Tools     | Model         | Perform actions                   |
| Resources | Application   | Provide contextual data           |
| Prompts   | User          | Provide reusable prompt templates |

### Tools

Tools are functions that the model can call.

Examples:

```text
get_weather()
search_web()
get_github_issues()
query_database()
```

### Resources

Resources provide data or context to the application.

Examples:

* Files
* Documents
* Database information
* API responses

### Prompts

Prompts are reusable templates that users can select and provide arguments to.

For example:

```text
/review-code
/summarize-document
/explain-topic
```

---

## MCP Server Example

A weather MCP server might expose:

```text
Weather MCP Server
        |
        +---- get_current_weather
        |
        +---- get_forecast
        |
        +---- get_weather_alerts
```

An AI Agent can select the appropriate tool based on the user's request.

For example:

```text
User:
"What is the weather in Bhubaneswar?"

        ↓

AI Agent
        ↓

Weather MCP Server
        ↓

get_current_weather()
        ↓

AccuWeather
        ↓

Weather Result
```

---

## MCP and AI Agents

MCP is especially useful for AI Agents because agents need to interact with external systems.

An agent can:

1. Understand the user's goal.
2. Determine which tool is required.
3. Call the MCP tool.
4. Receive the result.
5. Continue reasoning.
6. Perform additional tool calls if required.
7. Return the final answer.

Example:

```text
User
 |
 v
Agent
 |
 +---- Search MCP
 |
 +---- Database MCP
 |
 +---- GitHub MCP
 |
 v
Final Result
```

---

## Advantages of MCP

### Standardized Integration

Applications can communicate with different tools using a common protocol.

### Reusability

One MCP server can potentially be used by multiple MCP-compatible clients.

### Tool Discovery

Clients can discover the capabilities exposed by an MCP server.

### Modularity

Tools can be separated into independent MCP servers.

### Easier Agent Development

Agents can use external tools without implementing a completely custom integration for every service.

### Scalability

As the number of tools increases, organizations can organize them into separate MCP servers.

---

## MCP vs Traditional API Integration

| Feature                  | Traditional API Integration | MCP                             |
| ------------------------ | --------------------------- | ------------------------------- |
| Purpose                  | Service integration         | AI application/tool integration |
| Standard interface       | API-specific                | Common MCP protocol             |
| Tool discovery           | Usually custom              | Supported                       |
| AI-specific metadata     | Usually limited             | Supported                       |
| Reusable across AI hosts | Requires integration        | Designed for MCP clients        |
| Tools                    | API endpoints               | Model-callable tools            |
| Resources                | API-specific                | Standardized concept            |
| Prompts                  | Usually not part of API     | Supported                       |

MCP does not replace APIs.

Instead, an MCP server can act as an AI-friendly interface over existing APIs.

For example:

```text
AI Agent
   |
   v
MCP Server
   |
   v
Weather API
```

The underlying service can still be a normal REST API.

---

## MCP Transports

MCP supports different ways of communicating between a client and server.

Two important transports are:

* STDIO
* Streamable HTTP

They are discussed in detail in the separate `stdio-vs-streamable-http.md` assignment.

---

## Security Considerations

Giving an AI Agent access to tools also introduces security risks.

Examples include:

* Excessive permissions
* Malicious or compromised MCP servers
* Prompt injection
* Unauthorized database access
* Destructive tool execution
* Sensitive data exposure

Therefore, MCP tools should follow the principle of least privilege.

Agents should only receive the permissions required to perform their tasks.

---

## MCP in Multica

In the Multica architecture, MCP can be used to provide tools to agents.

For example:

```text
                  Multica
                     |
               Orchestrator
                     |
          +----------+----------+
          |          |          |
       Weather     GitHub     Wikipedia
        Agent       Agent       Agent
          |          |           |
          v          v           v
       MCP Server  MCP Server  MCP Server
```

This allows different agents to use different capabilities while the orchestrator coordinates the overall workflow.

---

## Conclusion

Model Context Protocol provides a standardized way for AI applications and agents to interact with external tools, data sources, and services.

Its main benefits are:

* Standardized communication
* Tool discovery
* Reusable integrations
* Modular architecture
* Better support for AI Agents

MCP is therefore an important part of modern agentic AI systems because it connects the reasoning capabilities of an AI model with real-world tools and data.

## References

* Model Context Protocol — Official Documentation
* MCP Specification
* MCP Python SDK
* MCP TypeScript SDK
