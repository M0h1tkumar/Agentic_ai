# 5 August Task Report

**Name:** Ankush Saha
**Date:** 5 August
**Role:** Team Member

## Tasks Assigned

The tasks assigned for 5 August focused on setting up Multica, exploring its integrations with external tools, and experimenting with agentic AI development workflows.

### 1. Multica Installation

The first task was to install and run **Multica** locally. Docker was preferred for the setup, so I used the Multica Docker image to get the environment running.

```bash
docker pull multica/multica:latest
docker run -d --name multica -p 8080:8080 multica/multica:latest
```

I verified that the container was running successfully using:

```bash
docker ps | grep multica
```

After the container started, Multica was accessible through:

```text
http://localhost:8080
```

This provided the base environment required for the remaining experiments.

---

## 2. Team Workspace Creation

Workspace creation was specified as a **Team Leader-only task**, so this was handled by the respective team leaders.

The expected workspace setup included creating a workspace for the team, adding members and assigning appropriate roles such as:

* Admin
* Developer
* Viewer

The workspace was intended to provide a common environment for the team's agentic AI work.

---

## 3. Multica and Slack Integration

The next task was to connect Multica with **Slack** so that agent outputs and notifications could be communicated through the team's Slack workspace.

I created a Slack application and configured the required bot permissions, including:

```text
channels:read
chat:write
chat:write.public
files:write
im:write
users:read
```

After installing the Slack application into the workspace, I obtained the Bot User OAuth Token and configured the integration in Multica.

The configuration followed this structure:

```yaml
integrations:
  slack:
    enabled: true
    bot_token: "xoxb-your-token-here"
    signing_secret: "your-signing-secret"
    channels:
      default: "#ai-agents"
      alerts: "#ai-alerts"
```

I then tested the connection by sending a message from Multica to the configured Slack channel.

```python
from multica.integrations import SlackIntegration

slack = SlackIntegration(bot_token="xoxb-...")
slack.send_message(
    "#ai-agents",
    "Multica is successfully connected to Slack!"
)
```

The successful delivery of the test message confirmed the basic Slack integration.

---

# 4. OpenCode Experimentation

The fourth task was to experiment with **OpenCode**, particularly because it is suitable for runtime-oriented development.

OpenCode provides a terminal-based AI coding workflow, allowing the developer to work with project files and execute commands without leaving the development environment.

I explored its installation and basic workflow:

```bash
npm install -g opencode-ai
```

or:

```bash
brew install opencode
```

The basic workflow involved opening the project directory and starting OpenCode:

```bash
cd your_project
opencode
```

I experimented with features such as:

* Project context loading
* Code generation
* Multi-file modifications
* Terminal command execution
* Switching between available AI models

Some of the commands explored included:

```text
/help
/model gpt-4o
/context .
/run python script.py
```

### Observations

OpenCode was particularly interesting for active development because the workflow stays within the terminal. It can inspect project files, make changes and execute commands as part of the same development process.

I also found that keeping the context focused and providing smaller tasks is preferable to loading the entire project unnecessarily.

---

# 5. Microsoft Recorder Skills Experimentation

The fifth task involved experimenting with **Microsoft Recorder Skills** through Power Automate.

The main objective was to understand how user-interface actions can be recorded and converted into automated workflows.

I explored the basic recording process:

1. Open Power Automate Desktop.
2. Start the Recorder.
3. Perform UI actions such as clicking buttons and entering information.
4. Stop the recording.
5. Review the generated actions.
6. Modify the workflow where required.
7. Run the automation.

For web-based workflows, recorded actions can contain selectors similar to:

```javascript
{
  "action": "click",
  "selector": "#submit-button",
  "timeout": 5000
}
```

### Observations

Recorder Skills appear useful for repetitive tasks such as:

* Data entry
* Form filling
* Repetitive browser operations
* Microsoft 365-related workflows

One interesting possibility is combining the recorded workflow with an AI agent. For example, a recorder could collect or enter data and then trigger a Multica agent to validate or process that information.

The main limitation I observed is that dynamic web pages may require additional handling because selectors can change.

---

# 6. Advanced Task — AnythingLLM RAG → Multica/OpenClaw Through MCP

The advanced task was to connect **AnythingLLM's RAG database to Multica/OpenClaw by exposing it through an MCP server**.

The objective was to allow Multica agents to retrieve and use documents stored in AnythingLLM while they were executing tasks.

The architecture can be represented as:

```text
        Documents
            ↓
       AnythingLLM
            ↓
        RAG Database
            ↓
        MCP Server
            ↓
    Multica / OpenClaw
            ↓
       AI Agent
            ↓
      Final Response
```

The important part of this setup is that the agent does not need to directly implement the AnythingLLM API. Instead, the MCP server exposes the required functionality as tools that the agent can call.

---

## AnythingLLM Setup

I first deployed AnythingLLM using Docker:

```bash
docker pull mintplexlabs/anythingllm

docker run -d \
  --name anythingllm \
  -p 3001:3001 \
  -v $(pwd)/anythingllm:/app/server/storage \
  mintplexlabs/anythingllm
```

The AnythingLLM interface was then available at:

```text
http://localhost:3001
```

I created a workspace and uploaded documents such as PDFs and Markdown files so that AnythingLLM could process and index them for retrieval.

The API key generated from AnythingLLM was then used for communication between the MCP server and the RAG system.

---

## MCP Server Development

I created a Python-based MCP server to act as the bridge between AnythingLLM and Multica/OpenClaw.

The MCP server exposed functionality such as:

### Document Query

A `query_documents` tool was used to send a question to an AnythingLLM workspace and retrieve information from the stored knowledge base.

### Workspace Listing

A `list_workspaces` tool was added to retrieve the available AnythingLLM workspaces.

The basic structure was:

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
import httpx

app = Server("anythingllm-rag")

ANYTHINGLLM_URL = "http://localhost:3001/api/v1"
API_KEY = "your-anythingllm-api-key"

@app.tool()
async def query_documents(
    query: str,
    workspace: str = "default"
) -> str:

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{ANYTHINGLLM_URL}/workspace/{workspace}/chat",
            headers={
                "Authorization": f"Bearer {API_KEY}"
            },
            json={
                "message": query,
                "mode": "query"
            }
        )

        data = response.json()

        return data.get(
            "textResponse",
            "No relevant documents found."
        )


@app.tool()
async def list_workspaces() -> str:

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{ANYTHINGLLM_URL}/workspaces",
            headers={
                "Authorization": f"Bearer {API_KEY}"
            }
        )

        workspaces = response.json().get(
            "workspaces",
            []
        )

        return "\n".join(
            f"- {ws['name']} (slug: {ws['slug']})"
            for ws in workspaces
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(stdio_server(app))
```

---

## Connecting the MCP Server to Multica

After creating the MCP server, it was registered with Multica through its configuration:

```yaml
mcp_servers:
  - name: "anythingllm-rag"
    command: "python anythingllm_mcp_server.py"
    description: "Access team documents from AnythingLLM RAG database"
```

The exposed MCP tools could then be provided to an agent:

```python
from multica import Agent

rag_agent = Agent(
    name="DocumentResearcher",
    role="Document specialist",
    goal="Answer questions using the team's knowledge base",
    tools=[
        "query_documents",
        "list_workspaces"
    ]
)
```

This allows the agent to query the knowledge base when it needs additional information during execution.

---

# Overall Outcome

The tasks gave me hands-on exposure to different parts of an agentic AI workflow.

### Multica

I successfully explored the local Docker-based setup and understood the basic workspace structure.

### Slack

I worked with Slack's bot API and connected it with Multica so that agent messages could be sent to team channels.

### OpenCode

I experimented with a terminal-based AI coding workflow and explored how it can be used for faster development and runtime tasks.

### Microsoft Recorder Skills

I explored how UI actions can be recorded and converted into automation workflows, along with the possibility of combining RPA with AI agents.

### AnythingLLM + MCP

The advanced task provided practical understanding of how an external RAG system can be exposed through MCP and consumed by an AI agent.

The final architecture demonstrated the separation between **knowledge storage, retrieval, tool exposure and agent reasoning**:

```text
Knowledge Base
     ↓
 AnythingLLM
     ↓
      RAG
     ↓
 MCP Tool Layer
     ↓
Multica/OpenClaw
     ↓
     Agent
     ↓
   Response
```

## Key Learnings

1. Docker simplifies the deployment of AI tools such as Multica and AnythingLLM.
2. Slack can be used as an external communication layer for agent outputs.
3. Terminal-based coding assistants such as OpenCode can integrate AI directly into the development workflow.
4. Recorder Skills demonstrate how traditional RPA workflows can be combined with AI-based processing.
5. MCP provides a standardized way of exposing external capabilities as tools for AI agents.
6. RAG allows agents to work with organization-specific information instead of relying only on their pretrained knowledge.
7. The AnythingLLM → MCP → Multica/OpenClaw architecture provides a flexible approach for building knowledge-aware agents.
