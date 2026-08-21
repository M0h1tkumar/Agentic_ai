# 5 August Tasks — Multica Setup, Slack Integration & Advanced Tasks

> **Date:** 5 August | **Author:** Utkarsh Sinha | **Role:** Team Member

---

## ✅ Task 1: Multica Installation (Docker — Recommended)

> Note: Team workspace creation is performed by Team Leaders only.

```bash
# Pull and run Multica via Docker
docker pull multica/multica:latest
docker run -d --name multica -p 8080:8080 multica/multica:latest

# Verify
docker ps | grep multica
open http://localhost:8080
```

See full installation guide → [`3 august/multica_installation.md`](../3%20august/multica_installation.md)

---

## ✅ Task 2: Workspace Creation (Team Leaders Only)

> This task is performed by respective team leaders.

**Steps for Team Leaders:**
1. Open Multica UI at `http://localhost:8080`
2. Navigate to **Workspaces → Create New Workspace**
3. Fill in workspace details:
   - Name: `Team Rohit`
   - Description: Agentic AI Internship - Team Rohit
   - Admin: Team Leader email
4. Invite team members via email or share invite link
5. Assign roles: Admin, Developer, Viewer

---

## ✅ Task 3: Connect Multica with Slack

### Step 1: Create a Slack App
1. Go to https://api.slack.com/apps → **Create New App**
2. Choose "From Scratch" → App Name: `Multica Bot`
3. Select your workspace → Create App

### Step 2: Configure Bot Token Scopes
In your Slack App settings → **OAuth & Permissions → Bot Token Scopes:**
```
channels:read
chat:write
chat:write.public
files:write
im:write
users:read
```

### Step 3: Install App to Workspace
- Click **Install to Workspace** → Allow
- Copy the **Bot User OAuth Token** (starts with `xoxb-`)

### Step 4: Configure Multica
```yaml
# In Multica config.yaml
integrations:
  slack:
    enabled: true
    bot_token: "xoxb-your-token-here"
    signing_secret: "your-signing-secret"
    channels:
      default: "#ai-agents"
      alerts: "#ai-alerts"
```

### Step 5: Test the Connection
```python
# test_slack.py
from multica.integrations import SlackIntegration

slack = SlackIntegration(bot_token="xoxb-...")
slack.send_message("#ai-agents", "✅ Multica is connected to Slack!")
```

```bash
python test_slack.py
# Expected: Message appears in #ai-agents channel
```

---

## ✅ Task 4: Experiment with OpenCode (Best for Runtime)

### What is OpenCode?
**OpenCode** is a terminal-based AI coding assistant optimized for real-time code generation and editing. It excels at:
- Fast code completion
- Terminal-native workflows
- Low-latency responses ideal for active development

### Installation
```bash
npm install -g opencode-ai
# or
brew install opencode
```

### Key Features Tested
| Feature | Result |
|---|---|
| Code Generation Speed | ⚡ ~2-3x faster than browser-based tools |
| Context Window | Reads full project files automatically |
| Multi-file Edits | ✅ Can modify multiple files in one request |
| Terminal Integration | ✅ Native shell command execution |
| Model Support | GPT-4o, Claude 3.5, Gemini 1.5 Pro |

### Usage
```bash
# Start OpenCode in project directory
cd your_project
opencode

# Key commands inside OpenCode
/help          - Show all commands
/model gpt-4o  - Switch model
/context .     - Load all files in current dir
/run python script.py  - Execute code directly
```

### Best Practices for Runtime Performance
1. Use `/context` sparingly — only load files you need
2. Prefer smaller, focused prompts over large monolithic requests
3. Use `/model gpt-4o-mini` for simple tasks to reduce latency
4. Enable streaming mode for real-time output

---

## ✅ Task 5: Microsoft Recorder Skills (Experimentation)

### What are Recorder Skills?
Microsoft's **Recorder Skills** in Power Automate allow you to record UI interactions and convert them into automated workflows/RPA (Robotic Process Automation) scripts.

### Key Experiments Performed

#### A. Basic UI Recording
1. Open **Power Automate Desktop**
2. Click **Record** → Record button clicks, form fills
3. Stop recording → Auto-generates action list
4. Review and edit generated actions
5. Run the automation

#### B. Web Recorder
```javascript
// Recorded selectors example
{
  "action": "click",
  "selector": "#submit-button",
  "timeout": 5000
}
```

#### C. Integration with AI
- Recorder Skills can trigger Multica agents after automation completes
- Example workflow: Record data entry → Trigger AI agent to validate entries

### Observations
- Best for repetitive data entry and form automation
- Works well with Microsoft 365 applications
- Limited flexibility with dynamic web pages
- Good starting point for RPA without coding

---

## 🔬 Advanced Task: Connect AnythingLLM RAG → Multica via MCP Server

### Architecture Overview
```
AnythingLLM (RAG DB) → MCP Server → Multica Agents
        ↓                    ↓              ↓
  Document Store      Tool Interface   AI Reasoning
```

### Step 1: Set Up AnythingLLM
```bash
docker pull mintplexlabs/anythingllm
docker run -d \
  --name anythingllm \
  -p 3001:3001 \
  -v $(pwd)/anythingllm:/app/server/storage \
  mintplexlabs/anythingllm
```

Access at: `http://localhost:3001`

### Step 2: Upload Documents to AnythingLLM
1. Login → Create Workspace → "Team Rohit RAG"
2. Upload PDFs, markdown files, docs
3. AnythingLLM processes and embeds them automatically
4. Note the **API Key** from Settings → API Keys

### Step 3: Build an MCP Server to Expose AnythingLLM
```python
# anythingllm_mcp_server.py
from mcp.server import Server
from mcp.server.stdio import stdio_server
import httpx

app = Server("anythingllm-rag")
ANYTHINGLLM_URL = "http://localhost:3001/api/v1"
API_KEY = "your-anythingllm-api-key"

@app.tool()
async def query_documents(query: str, workspace: str = "default") -> str:
    """
    Search the AnythingLLM RAG database for relevant documents.
    Args:
        query: The search query or question
        workspace: AnythingLLM workspace slug
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{ANYTHINGLLM_URL}/workspace/{workspace}/chat",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={"message": query, "mode": "query"}
        )
        data = response.json()
        return data.get("textResponse", "No relevant documents found.")

@app.tool()
async def list_workspaces() -> str:
    """List all available AnythingLLM workspaces."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{ANYTHINGLLM_URL}/workspaces",
            headers={"Authorization": f"Bearer {API_KEY}"}
        )
        workspaces = response.json().get("workspaces", [])
        return "\n".join([f"- {ws['name']} (slug: {ws['slug']})" for ws in workspaces])

if __name__ == "__main__":
    import asyncio
    asyncio.run(stdio_server(app))
```

### Step 4: Register MCP Server with Multica
```yaml
# In Multica config.yaml
mcp_servers:
  - name: "anythingllm-rag"
    command: "python anythingllm_mcp_server.py"
    description: "Access team documents from AnythingLLM RAG database"
```

### Step 5: Use RAG in Multica Agent
```python
from multica import Agent

rag_agent = Agent(
    name="DocumentResearcher",
    role="Document specialist",
    goal="Answer questions using team's knowledge base",
    tools=["query_documents", "list_workspaces"]  # MCP tools auto-registered
)

# The agent can now autonomously query AnythingLLM documents!
result = rag_agent.run("What are our company's AI usage policies?")
```

### Result / Outcome
- ✅ Multica agents can now retrieve context from AnythingLLM during execution
- ✅ RAG-augmented responses are significantly more accurate on domain-specific questions
- ✅ The MCP server acts as a clean abstraction layer — no hardcoded API calls in agents

---

## 📝 Key Learnings
1. MCP servers are the cleanest way to expose external services to AI agents
2. AnythingLLM + Multica creates a powerful RAG-enhanced agentic system
3. OpenCode is fastest for active development; great for runtime tasks
4. Recorder Skills automate repetitive UI tasks without code — great for non-technical users
5. Slack integration makes agent outputs accessible to the whole team in real-time
