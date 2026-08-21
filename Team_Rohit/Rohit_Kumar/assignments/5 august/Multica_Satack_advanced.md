# 5 August Tasks — Multica Setup, Slack Integration & Advanced Tasks

> **Date:** 5 August 2026
> **Author:** Rohit Kumar
> **Role:** Team Member

---

## Task 1: Multica Installation

Multica should be installed and verified before configuring the remaining integrations.

Docker is preferred when supported because it provides an isolated and reproducible environment.

```bash
docker pull <MULTICA_IMAGE>

docker run -d \
  --name multica \
  -p 8080:8080 \
  <MULTICA_IMAGE>

docker ps
```

The exact image name, port, and environment variables should be taken from the Multica version used by the team.

The local Multica installation should then be tested to confirm that the service is running.

---

## Task 2: Team Workspace

> **Note:** Workspace creation is performed by the respective Team Leader.

A team workspace should provide a common environment for:

* Agents
* Users
* Tools
* Workflows
* Configurations

### Example Workspace Details

```text
Name: Team Rohit
Description: Agentic AI Internship - Team Rohit
Admin: Team Leader
```

Team members can then be invited and assigned appropriate permissions such as:

* Admin
* Developer
* Viewer

---

## Task 3: Connect Multica with Slack

Slack can be used as a messaging interface for interacting with Multica agents.

### Architecture

```text
Slack User
    |
    v
Slack
    |
    v
Multica
    |
    v
Agent
    |
    v
LLM + Tools
```

### Step 1: Create a Slack App

Go to:

https://api.slack.com/apps

Create a new app using **From Scratch** and select the required Slack workspace.

Example:

```text
App Name: Multica Bot
```

### Step 2: Configure Permissions

Under **OAuth & Permissions**, add only the scopes required by the integration.

Typical examples may include:

```text
channels:read
chat:write
chat:write.public
users:read
```

The exact scopes depend on the required Slack functionality.

### Step 3: Install the App

Install the app into the Slack workspace and obtain the Bot User OAuth Token.

The token typically starts with:

```text
xoxb-
```

Treat this token as a secret.

### Step 4: Configure Multica

A configuration may look conceptually like:

```yaml
integrations:
  slack:
    enabled: true
    bot_token: ${SLACK_BOT_TOKEN}
```

The exact configuration keys depend on the Multica version.

### Step 5: Test

Send a test message from Multica to the selected Slack channel.

Expected result:

```text
Multica Agent
      |
      v
Slack Integration
      |
      v
#ai-agents
```

---

## Task 4: Experiment with OpenCode

### What is OpenCode?

OpenCode is an open-source AI coding agent that can run in the terminal, desktop application, or IDE extension. It supports multiple LLM providers and MCP servers.

### Installation

For Windows, OpenCode recommends using WSL for the best experience. It can also be installed using npm, Chocolatey, Scoop, or other supported methods.

Using npm:

```bash
npm install -g opencode-ai
```

Start OpenCode inside a project:

```bash
cd your_project
opencode
```

### MCP Integration

OpenCode supports local MCP servers using STDIO and remote MCP servers using Streamable HTTP.

Example local MCP configuration:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "weather": {
      "type": "local",
      "command": [
        "npx",
        "-y",
        "@timlukahorstmann/mcp-weather"
      ],
      "environment": {
        "ACCUWEATHER_API_KEY": "{env:ACCUWEATHER_API_KEY}"
      }
    }
  }
}
```

Configured MCP servers can be checked with:

```bash
opencode mcp list
```

OpenCode also provides:

```bash
opencode mcp add
```

for adding MCP servers.

### Observations

OpenCode is useful for agent development because it provides:

* Terminal-based interaction
* Project-aware coding
* Tool and MCP integration
* Multiple model/provider support
* Multi-file editing
* Agent-oriented workflows

---

## Task 5: Microsoft Skill Recorder / Agent Skills

Microsoft provides an Agent Skills ecosystem for reusable, domain-specific skills used by AI coding agents.

The Microsoft skills repository provides skills, custom agents, templates, and MCP configurations. Skills are organized as `SKILL.md` packages containing metadata and instructions.

### Installation

The Microsoft skills repository provides a skills installer:

```bash
npx skills add microsoft/skills
```

The installer lets the user select the required skills.

### What a Skill Contains

A typical skill contains:

```text
SKILL.md
```

with:

* Skill name
* Description
* Triggering conditions
* Instructions
* Domain-specific knowledge
* Expected behavior

### Example

```text
Skill Name:
Weather Research

Purpose:
Retrieve and summarize weather information.

Input:
City name

Workflow:
1. Identify the city.
2. Call the weather tool.
3. Retrieve current conditions.
4. Retrieve forecast.
5. Summarize the result.

Output:
Clear weather report.
```

### Key Learning

Skills make agent behavior more consistent by separating reusable domain instructions from the core agent logic.

---

# Advanced Task: AnythingLLM RAG → Multica via MCP

## Objective

The goal is to allow a Multica/OpenClaw agent to retrieve documents stored inside an AnythingLLM workspace during execution.

AnythingLLM can use vector databases such as LanceDB and Qdrant for RAG workflows.

---

## Architecture

```text
Documents
     |
     v
AnythingLLM Workspace
     |
     v
Embedding + Vector Database
     |
     v
Retrieval Layer
     |
     v
MCP Server
     |
     v
Multica / OpenClaw Agent
     |
     v
LLM
```

---

## Why Use MCP?

Instead of making the agent directly depend on the internal vector database:

```text
Agent
  |
  +---- LanceDB-specific code
```

use a controlled MCP interface:

```text
Agent
  |
  v
MCP Tool
  |
  v
AnythingLLM Retrieval
  |
  v
LanceDB / Qdrant
```

This provides an abstraction between the agent and the storage layer.

---

## AnythingLLM Setup

Create a workspace in AnythingLLM and upload the required documents.

Example:

```text
Workspace:
Team Rohit RAG
```

Documents may include:

* PDF files
* Markdown files
* Text files
* Documentation
* Internal project material

AnythingLLM processes the documents and makes them available for retrieval through its RAG system.

---

## MCP Retrieval Tool

The MCP layer can expose a tool such as:

```text
query_documents(query)
```

Example:

```json
{
  "query": "What is the company's AI usage policy?"
}
```

The MCP server can forward the request to AnythingLLM, retrieve relevant information, and return the result to the agent.

---

## Retrieval Flow

```text
User Question
      |
      v
Multica Agent
      |
      v
MCP query_documents()
      |
      v
AnythingLLM
      |
      v
Vector Database
      |
      v
Relevant Documents
      |
      v
Agent
      |
      v
Final Answer
```

---

## Security Considerations

The MCP retrieval layer should enforce:

* Authentication
* Authorization
* Workspace-level access
* Least-privilege permissions
* Secure API keys
* Logging where appropriate

API keys must never be committed to GitHub.

Use environment variables:

```env
ANYTHINGLLM_API_KEY=your_secret
```

---

## Expected Outcome

A successful implementation should allow:

```text
User
  ↓
Multica Agent
  ↓
MCP Tool
  ↓
AnythingLLM RAG
  ↓
Relevant Document Context
  ↓
Agent Response
```

The agent should be able to answer questions using documents stored in the AnythingLLM knowledge base.

---

## Key Learnings

1. Multica provides the agent execution environment.
2. Slack can provide a user-facing messaging interface.
3. OpenCode can act as an agent runtime and connect to MCP servers.
4. Reusable skills help maintain consistent agent behavior.
5. MCP provides a standardized interface between agents and external tools.
6. AnythingLLM can provide the RAG knowledge layer for agents.
7. Sensitive credentials should always be stored outside source code.

---

## Conclusion

The 5 August tasks connect the basic Multica environment with real users, agent runtimes, reusable skills, and external knowledge.

The resulting architecture can be summarized as:

```text
User
 ↓
Slack / CLI
 ↓
Multica
 ↓
Agent Runtime
 ↓
Agent
 ↓
Skills + MCP Tools
 ↓
APIs / RAG / Databases
```
