# API vs MCP (Model Context Protocol)

> **Date:** 6 August | **Author:** Utkarsh Sinha

---

## 🔍 What is an API?

An **API (Application Programming Interface)** is a set of rules and protocols that allows one software application to communicate with another. It defines **endpoints**, **request formats**, and **response formats** — acting as a contract between a client and a server.

- **Example:** A weather app calling `GET /weather?city=Bhubaneswar` to get temperature data from a weather service.
- **Common Styles:** REST, GraphQL, gRPC, SOAP
- **Primary Users:** Human developers who write code to call those endpoints

---

## 🤖 What is MCP (Model Context Protocol)?

**MCP (Model Context Protocol)** is an open standard developed by Anthropic that allows AI models and agents to **dynamically discover and use tools, data sources, and services** at runtime — without a human manually writing integration code.

It acts as a **universal adapter layer** between AI systems and the tools they need to use. Think of it as a "USB-C port" for AI — one standard interface for everything.

- **Example:** An AI agent using MCP auto-discovers a `get_weather` tool and calls it autonomously for Bhubaneswar during a conversation.
- **Primary Users:** AI models/agents operating autonomously
- **Spec Reference:** https://mcpservers.org/

---

## ⚖️ Key Differences Between API and MCP

| Feature | API | MCP |
|---|---|---|
| **Primary Consumer** | Human developers | AI models/agents |
| **Interaction Type** | Explicit, hard-coded calls | Dynamic, runtime discovery |
| **Integration Effort** | High — custom code per service | Low — one standard protocol |
| **Self-Description** | No — docs must be read by humans | Yes — tools describe themselves |
| **Context Awareness** | Stateless by default | Context-aware, session-based |
| **AI Compatibility** | Poor — needs adapters/prompts | Native — AI-first design |
| **Standardization** | Varies (REST, GraphQL, gRPC) | Unified open standard |
| **Control** | Developer decides what to call | AI model decides at runtime |
| **Use Case** | App-to-app communication | Agent-to-tool communication |
| **Security Model** | API keys, OAuth, JWT | MCP gateways, token-based auth |

---

## ❌ Drawbacks of API Over MCP (in AI Agent Context)

### 1. 🔧 High Integration Effort
With APIs, developers must **manually write integration code** for every service — custom authentication, endpoint mapping, error handling, pagination — for each and every API they want to use.

> **MCP Advantage:** A single MCP client can talk to ANY MCP server with zero custom glue code.

---

### 2. 🤖 Not AI-Native (Static Nature)
APIs don't **explain themselves** to AI. An LLM doesn't inherently know what `POST /v2/messages` does — it must be told via system prompts or documentation. This requires extensive **prompt engineering** to bridge the gap.

> **MCP Advantage:** MCP tools have built-in descriptions, input schemas, and documentation that the AI reads automatically at runtime.

---

### 3. 🧠 No Autonomous Tool Discovery
With APIs, an AI agent must be **pre-programmed** with a list of available APIs. It cannot discover new capabilities on its own. As tools change or grow, the agent's configuration must be manually updated.

> **MCP Advantage:** AI agents using MCP can **dynamically list and discover** all available tools from an MCP server at runtime.

---

### 4. 🔁 Stateless by Design
Traditional REST APIs are **stateless** — each request is independent. For AI agents running multi-step workflows, developers must build complex custom state management systems to maintain context across calls.

> **MCP Advantage:** MCP supports **persistent sessions** and carries context across multiple tool calls within a conversation.

---

### 5. 🧩 Fragmented Ecosystem
Different APIs use different authentication methods (OAuth 2.0, API Keys, Basic Auth), different data formats (JSON, XML), and different versioning strategies. Every integration is a unique puzzle to solve.

> **MCP Advantage:** One standardized protocol — same connection, same format, same auth patterns for everything.

---

### 6. 💸 Prompt Engineering Tax
To make an LLM use an API correctly, you must include detailed documentation in the prompt — wasting tokens and increasing cost. Complex APIs require even more context.

> **MCP Advantage:** Tool schemas are read programmatically — no need to stuff API docs into your prompt window.

---

### 7. 🔄 Harder to Scale
Adding 10 new services to an API-based agent means writing 10 new integration modules. Maintenance overhead grows linearly with the number of services.

> **MCP Advantage:** Adding a new MCP server automatically makes all its tools available to any connected agent.

---

## 🔗 Relationship: MCP Does NOT Replace APIs

MCP **wraps** APIs — it doesn't eliminate them.

```
AI Agent  →  MCP Client  →  MCP Server  →  Underlying REST API  →  Service
```

MCP acts as the orchestration layer that translates AI-native tool calls into standard API requests behind the scenes.

---

## 📦 MCP Server Resources Explored

| Resource | URL | Description |
|---|---|---|
| MCP Servers Directory | https://mcpservers.org/ | Browse 1000+ community MCP servers |
| MCP Market Submit | https://mcpmarket.com/submit | Submit your own MCP server |

### Notable MCP Servers from mcpservers.org:
- **Filesystem MCP** — Read/write local files
- **GitHub MCP** — Manage repos, PRs, issues
- **Slack MCP** — Send messages and read channels
- **PostgreSQL MCP** — Query databases
- **Brave Search MCP** — Web search tool
- **Google Maps MCP** — Geolocation and maps

---

## 🎯 Summary

| When to use API | When to use MCP |
|---|---|
| Simple app-to-app integrations | AI agent workflows |
| Human-controlled logic flows | Autonomous AI decisions |
| Legacy systems | Modern AI-native stacks |
| Low AI involvement | High AI involvement |

> **Bottom Line:** APIs were built for developers. MCP was built for AI agents. In the age of agentic AI, MCP is becoming the standard for how AI systems interact with the world.
