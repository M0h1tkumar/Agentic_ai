# 30 July Tasks — Session Notes

> **Date:** 30 July | **Author:** Utkarsh Sinha

---

## ✅ Task 1: Session 1 & Session 2 (Performed)

### Session 1 — Introduction to AI Agents & Agentic Systems
- Overview of agentic AI vs traditional chatbots
- Understanding tool use, planning, and memory in agents
- Introduction to multi-agent orchestration frameworks
- Key concepts: ReAct pattern, Chain-of-Thought, Tool Calling

### Session 2 — OpenClaw Framework Deep Dive
- Multi-agent team creation concepts
- Agent roles: Orchestrator, Executor, Validator
- Task routing and delegation between agents
- Hands-on with OpenClaw configuration

---

## ✅ Task 2: OpenClaw Multi-Agent Team Creation (Tasks 1–9)

### Task 1: Install OpenClaw
```bash
pip install openclaw
# or
git clone https://github.com/openclaw/openclaw
cd openclaw && pip install -e .
```

### Task 2: Initialize a Project
```bash
openclaw init my_project
cd my_project
```

### Task 3: Configure API Keys
```bash
# Create .env file
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

### Task 4: Define Your First Agent
```python
from openclaw import Agent

researcher = Agent(
    name="Researcher",
    role="Research specialist",
    goal="Find and summarize information",
    backstory="Expert at gathering data from multiple sources",
    tools=["web_search", "read_file"]
)
```

### Task 5: Define a Writer Agent
```python
writer = Agent(
    name="Writer",
    role="Content writer",
    goal="Write clear, concise reports",
    backstory="Experienced technical writer",
    tools=["write_file"]
)
```

### Task 6: Create Tasks
```python
from openclaw import Task

research_task = Task(
    description="Research the latest trends in AI agents",
    agent=researcher,
    expected_output="A bullet-point summary of 5 key trends"
)

write_task = Task(
    description="Write a 500-word report on the research findings",
    agent=writer,
    expected_output="A formatted markdown report",
    context=[research_task]
)
```

### Task 7: Form a Crew
```python
from openclaw import Crew

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    verbose=True
)
```

### Task 8: Run the Crew
```python
result = crew.kickoff()
print(result)
```

### Task 9: Review & Iterate Output
- Review the output for accuracy and completeness
- Adjust agent roles, prompts, and task descriptions as needed
- Add more agents for specialized subtasks (e.g., fact-checker, reviewer)

---

## 🔧 Optional: Telegram Bot Integration

Instead of testing directly in CLI, the agent outputs can be sent to a Telegram bot:

```python
import requests

BOT_TOKEN = "your_bot_token"
CHAT_ID   = "your_chat_id"

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})

# After crew.kickoff():
send_to_telegram(f"*Agent Report:*\n{result}")
```

**Setup Steps:**
1. Message `@BotFather` on Telegram → `/newbot`
2. Get your bot token
3. Find your chat ID via `https://api.telegram.org/bot<token>/getUpdates`
4. Replace placeholders above and run

---

## 📥 Optional: Multica Download & Setup
- Downloaded Multica from the official repository
- Noted for upcoming mandatory installation (5 August session)
- Docker-based installation recommended for isolation and portability
