# 🔌 Model Context Protocol (MCP) & Agent Skills Guide

> **Author:** Mohit Kumar — Team Mohit Lead  
> **Topic:** Tool connectivity, schema discovery, and extensible procedural memory for AI agents.

---

## 1. What is the Model Context Protocol (MCP)?

Traditional REST APIs are designed for human developers writing static code. They require manual SDK installations, custom authentication headers, and static endpoint definitions.

**MCP (Model Context Protocol)** is an open standard that gives AI models a dynamic, standardized way to discover and call tools at runtime.

### Why MCP Replaces Traditional REST for AI Agents:
- **Dynamic Discovery (`tools/list`):** The LLM asks the MCP server what tools are available, and the server returns the tools along with their JSON schemas.
- **Type-Safe Schema Validation:** Every argument is verified against standard JSONSchema before execution.
- **Context Preservation:** Enables tools to inject structured resources, prompts, and continuous context directly into the agent's context window.

---

## 2. MCP Transport Protocols: STDIO vs. Streamable HTTP (SSE)

Choosing the correct transport protocol is crucial for performance and reliability:

| Transport Mode | How It Works | When to Use | Advantages |
| :--- | :--- | :--- | :--- |
| **STDIO (Standard I/O)** | Agent spawns the server as a local child process and talks over `stdin`/`stdout`. | Local IDE agents, same-machine scripts, desktop tools. | **Fastest (near-zero latency)**, no network ports required, immune to network drops or firewall blocks. |
| **Streamable HTTP (SSE)** | Agent connects over HTTP/HTTPS using Server-Sent Events for bi-directional streaming. | Distributed Docker stacks, remote cloud agents, microservices. | Works across containers and networks; allows multiple agents to share one server. |

### Example: Local STDIO MCP Configuration
```json
{
  "mcpServers": {
    "local-tools": {
      "command": "node",
      "args": ["C:/TraeProjects/mcp-server/index.js"]
    }
  }
}
```

### Example: Remote SSE/HTTP MCP Configuration
```json
{
  "mcpServers": {
    "cloud-bridge": {
      "url": "http://kali-multica-bridge:8080/sse"
    }
  }
}
```

---

## 3. Agent Skills Architecture (`SKILL.md`)

### What is an Agent Skill?
A **Skill** is a modular directory of instructions, examples, and scripts that extends an agent's capabilities without bloating the global system prompt.

### Anatomy of a Skill
```
skills/
└── git-release-skill/
    ├── SKILL.md          <-- Core instructions with YAML frontmatter (Required)
    ├── scripts/          <-- Helper automation scripts
    └── examples/         <-- One-shot reference patterns
```

### Writing a High-Performance `SKILL.md`
```markdown
---
name: vercel-deployment-skill
description: Triggers production Vercel builds using headless token authentication and verifies live status.
triggers:
  - deploy to vercel
  - production release
  - redeploy frontend
---

# Instructions for Vercel Deployment

1. Check that all Git changes are committed to the target branch.
2. Run the deployment using the headless non-interactive flag:
   `npx vercel --prod --token $VERCEL_TOKEN --yes`
3. Capture the live URL from the output and verify HTTP 200 using curl.
4. Return the live URL to the user.
```

### Why Skills Outperform Huge System Prompts:
1. **Token Efficiency:** The agent only loads the `SKILL.md` file when the user prompt triggers it.
2. **Maintainability:** You can upgrade or fix a skill without breaking other agent behaviors.
3. **Portability:** Skills can be shared across agents (Antigravity, OpenClaw, Multica, Claude Code).
