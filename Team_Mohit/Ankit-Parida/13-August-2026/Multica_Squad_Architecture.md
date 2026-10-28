# Multica Squad Architecture & Delegation Framework

This document outlines the production **Multica Squad Architecture**, establishing a multi-agent hierarchy consisting of a lead **Orchestrator Agent** and specialized worker agents across **Research**, **Architecture**, and **Engineering**.

---

## 🏗 1. Squad Architecture Diagram

```mermaid
graph TD
    Orchestrator[Orchestrator Agent]
    Research[Research Agent]
    Architecture[Architecture Agent]
    Engineering[Engineering Agent]

    Orchestrator -->|Delegates Context Retrieval| Research
    Orchestrator -->|Delegates System Blueprint| Architecture
    Orchestrator -->|Delegates Implementation & Testing| Engineering

    Research -->>Orchestrator: Market & Technical Research Findings
    Architecture -->>Orchestrator: System Blueprints & Interface Specs
    Engineering -->>Orchestrator: Verified Code & Test Artifacts
```

### Exact Squad Hierarchy Structure

```
         Orchestrator Agent
                 |
                 |
 ---------------------------------
 |               |               |
Research    Architecture    Engineering
```

---

## 👥 2. Squad Creation & Role Breakdown

The squad is initialized in Multica via `multica squad create --config squad.json`:

### Role Specifications & Capabilities

| Squad Role | Agent ID | Model Provider | Key Tools & Skills Assigned |
| :--- | :--- | :--- | :--- |
| **Orchestrator Agent** | `squad-orchestrator-lead` | `gpt-4o` | `delegate_task`, `evaluate_subtask`, `synthesize_final_output` |
| **Research Agent** | `squad-worker-research` | `claude-3-5-sonnet` | `wikipedia_search`, `hackernews_digest`, `web_search` |
| **Architecture Agent** | `squad-worker-arch` | `claude-3-5-sonnet` | `generate_mermaid_diagram`, `spec_validator` |
| **Engineering Agent** | `squad-worker-eng` | `gpt-4o` | `opencode_interpreter`, `github_repo_tool`, `unit_tester` |

---

## 🔄 3. Inter-Agent Coordination & Delegation Workflow

```mermaid
sequenceDiagram
    autonumber
    actor User as User / Client App
    participant Orch as Orchestrator Agent
    participant Res as Research Agent
    participant Arch as Architecture Agent
    participant Eng as Engineering Agent

    User->>Orch: Submits Goal: "Build RAG Feature for Multica"
    
    rect rgb(240, 248, 255)
        note right of Orch: Phase 1: Research
        Orch->>Res: Delegate: "Gather RAG & Vector DB Specs"
        Res->>Res: Query Wikipedia & HackerNews MCP Tools
        Res-->>Orch: Return Research Report
    end

    rect rgb(255, 245, 238)
        note right of Orch: Phase 2: Architecture
        Orch->>Arch: Delegate: "Design AnythingLLM MCP Diagram & API Schemas"
        Arch->>Arch: Synthesize Mermaid Diagrams & JSON Schemas
        Arch-->>Orch: Return Architecture Specs
    end

    rect rgb(245, 255, 250)
        note right of Orch: Phase 3: Engineering
        Orch->>Eng: Delegate: "Write & Verify Sandbox Implementation Code"
        Eng->>Eng: Execute OpenCode Python/JS Unit Tests
        Eng-->>Orch: Return Tested Code Artifacts
    end

    Orch->>User: Compiles & Delivers Final Project Package
```

---

## ⚙ 4. Squad Configuration (`squad.json`)

```json
{
  "squadName": "Multica-Core-Engineering-Squad",
  "leadAgentId": "squad-orchestrator-lead",
  "coordinationStrategy": "phase-gated-sequential",
  "agents": [
    {
      "agentId": "squad-orchestrator-lead",
      "role": "Orchestrator",
      "systemPrompt": "You are Orchestrator Lead. Decompose user requests into Research, Architecture, and Engineering sub-tasks. Validate outputs before advancing phases."
    },
    {
      "agentId": "squad-worker-research",
      "role": "Research",
      "systemPrompt": "You are Research Agent. Conduct deep-dive context retrieval using assigned MCP tools."
    },
    {
      "agentId": "squad-worker-arch",
      "role": "Architecture",
      "systemPrompt": "You are Architecture Agent. Convert research findings into clean system diagrams and API schemas."
    },
    {
      "agentId": "squad-worker-eng",
      "role": "Engineering",
      "systemPrompt": "You are Engineering Agent. Synthesize code and run sandboxed tests via OpenCode runtime."
    }
  ]
}
```
