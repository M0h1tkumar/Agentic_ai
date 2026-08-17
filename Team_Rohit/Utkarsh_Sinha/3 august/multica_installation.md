# 3 August Tasks — Multica Installation & OmniRoute

> **Date:** 3 August | **Author:** Utkarsh Sinha

---

## ✅ Task 1: Cloning & Installation of Multica

### What is Multica?
**Multica** is a multi-agent collaboration framework that allows teams of AI agents to work together on complex tasks. It provides:
- Role-based agent assignment
- Task orchestration and handoff
- Workspace management for teams
- Integration with popular messaging platforms (Slack, Discord)

---

### Clone the Repository
```bash
git clone https://github.com/multica/multica.git
cd multica
```

### Method 1: Direct Python Installation
```bash
# Create virtual environment
python3 -m venv multica_env
source multica_env/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
pip install -e .

# Verify installation
multica --version
```

### Method 2: Docker Installation (Recommended)
```bash
# Pull official Docker image
docker pull multica/multica:latest

# Run Multica container
docker run -d \
  --name multica \
  -p 8080:8080 \
  -e OPENAI_API_KEY=your_key_here \
  -v $(pwd)/workspace:/app/workspace \
  multica/multica:latest

# Verify container is running
docker ps | grep multica

# Access Multica UI
open http://localhost:8080
```

### Docker Compose (For Team Setup)
```yaml
# docker-compose.yml
version: '3.8'
services:
  multica:
    image: multica/multica:latest
    ports:
      - "8080:8080"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - SLACK_BOT_TOKEN=${SLACK_BOT_TOKEN}
    volumes:
      - ./workspace:/app/workspace
      - ./config:/app/config
    restart: unless-stopped

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
```

```bash
# Start with Docker Compose
docker-compose up -d

# Check logs
docker-compose logs -f multica
```

### Initial Configuration
```bash
# Create config file
cp config.example.yaml config.yaml

# Edit with your API keys
nano config.yaml
```

```yaml
# config.yaml
llm:
  provider: openai
  model: gpt-4o
  api_key: ${OPENAI_API_KEY}

workspace:
  name: "Team Rohit"
  admin: "Utkarsh Sinha"

integrations:
  slack:
    enabled: true
    bot_token: ${SLACK_BOT_TOKEN}
    channel: "#ai-agents"
```

---

## 🔬 Optional: Experimenting with OmniRoute

### What is OmniRoute?
**OmniRoute** is an intelligent LLM routing system that automatically selects the best AI model (GPT-4, Claude, Gemini, Mistral, etc.) based on:
- Task complexity
- Cost optimization
- Speed requirements
- Model capabilities

### Installation
```bash
pip install omniroute
```

### Basic Usage
```python
from omniroute import OmniRouter

router = OmniRouter(
    providers={
        "openai": {"api_key": "sk-...", "models": ["gpt-4o", "gpt-4o-mini"]},
        "anthropic": {"api_key": "sk-ant-...", "models": ["claude-3-5-sonnet"]},
        "google": {"api_key": "...", "models": ["gemini-1.5-pro"]}
    },
    strategy="cost_optimized"  # or "speed", "quality", "balanced"
)

response = router.chat(
    messages=[{"role": "user", "content": "Explain quantum computing in simple terms"}],
    task_type="explanation"  # helps routing decisions
)

print(f"Used model: {response.model_used}")
print(f"Response: {response.content}")
```

### Routing Strategies
| Strategy | Best For | Cost | Speed |
|---|---|---|---|
| `cost_optimized` | Bulk processing, simple tasks | ⭐⭐⭐⭐⭐ Low | Medium |
| `speed` | Real-time apps, chatbots | Medium | ⭐⭐⭐⭐⭐ Fast |
| `quality` | Complex reasoning, code gen | High | Slow |
| `balanced` | General purpose | Medium | Medium |

### Integration with Multica
```python
from multica import Multica
from omniroute import OmniRouter

router = OmniRouter(strategy="balanced")

multica = Multica(
    llm_router=router,
    workspace="Team Rohit"
)
```

---

## 📝 Key Learnings
1. Docker is preferred for Multica as it isolates dependencies and makes team sharing easier
2. OmniRoute reduces LLM costs by 40-70% by routing simple tasks to cheaper models
3. Always use environment variables for API keys — never hardcode them
4. Docker Compose makes it easy to spin up the full stack (Multica + Redis cache) with one command
