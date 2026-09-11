# OpenClaw Agent Framework: Setup & Onboarding Guide

**OpenClaw** is a lightweight, high-performance runtime for building, deploying, and managing self-hosted autonomous AI agents. This guide details local installation, system configuration, environment initialization, and agent onboarding workflows.

---

## 📥 1. Installation

### Prerequisites
- Node.js `v20.0.0` or higher
- npm `v10.0.0` or yarn / pnpm
- Git & Docker Desktop (optional, for containerized execution)

### Installation Steps

```bash
# Clone the OpenClaw core framework repository
git clone https://github.com/openclaw/openclaw-core.git
cd openclaw-core

# Install global OpenClaw CLI and local dependencies
npm install -g @openclaw/cli
npm install

# Verify CLI installation
openclaw --version
```

---

## ⚙ 2. System Configuration

Initialize the local runtime configuration file `openclaw.config.json` in the project root:

```json
{
  "runtime": {
    "name": "Local-OpenClaw-Daemon",
    "port": 7432,
    "logLevel": "debug",
    "environment": "development"
  },
  "providers": {
    "defaultModel": "gpt-4o",
    "router": "omniroute",
    "fallbackModel": "claude-3-5-sonnet"
  },
  "security": {
    "authMode": "oauth-session",
    "allowLocalExecution": true,
    "maxSubprocesses": 5
  },
  "storage": {
    "type": "sqlite",
    "dbPath": "./data/openclaw_state.db"
  }
}
```

Set environment variables in `.env`:

```env
OPENCLAW_ENV=development
OPENCLAW_PORT=7432
OPENAI_API_KEY=sk-proj-YOUR_OPENAI_KEY
ANTHROPIC_API_KEY=sk-ant-YOUR_ANTHROPIC_KEY
```

---

## 🚀 3. Agent Onboarding & Lifecycle Management

### Onboarding Steps

1. **Agent Definition Creation**: Define `bootstrap-agent-01.json` under `agents/`:

```json
{
  "agentId": "bootstrap-agent-01",
  "name": "Bootstrap Verification Agent",
  "role": "System Inspector & Health Checker",
  "systemPrompt": "You are OpenClaw Bootstrap Agent. Inspect local environment, verify runtime status, and return structured system diagnostics.",
  "tools": [
    "system_info",
    "file_read",
    "ping_host"
  ],
  "maxTokens": 2048,
  "temperature": 0.2
}
```

2. **Register & Launch Agent**:

```bash
# Register agent with the daemon
openclaw agent register ./agents/bootstrap-agent-01.json

# Start the OpenClaw background daemon
openclaw daemon start

# Verify running agent instances
openclaw agent list
```

3. **Execution Test**:

```bash
openclaw run --agent bootstrap-agent-01 --prompt "Perform system health audit and report available disk space and Node version."
```

### Output Verification
```
[INFO] Agent bootstrap-agent-01 initialized successfully.
[INFO] Tool Invoked: system_info ()
[SUCCESS] System Audit Complete: Node v20.12.0 | Memory: 16GB | Disk Available: 120GB.
```
