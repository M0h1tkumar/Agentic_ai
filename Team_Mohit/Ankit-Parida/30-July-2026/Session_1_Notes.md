# Session 1 Notes: OpenClaw Multi-Agent Concepts & Fundamentals

This document records core concepts, execution models, and architectural patterns of multi-agent systems in the **OpenClaw** runtime framework.

---

## 🧠 1. Core Multi-Agent Paradigm in OpenClaw

Traditional single-agent architectures rely on a single model context window to handle problem decomposition, code execution, web retrieval, and validation. This creates context congestion and degraded performance.

OpenClaw addresses this through **Specialized Multi-Agent Distribution**:
- Decomposition of complex goals into discrete sub-tasks handled by narrow, hyper-specialized agents.
- Independent system prompts and tool constraints for each agent.
- Ephemeral sub-agent spawning to maintain clean context windows.

---

## 🏗 2. Topologies & Communication Models

OpenClaw supports three primary multi-agent topologies:

```mermaid
graph LR
    subgraph 1. Hierarchical (Orchestrator Pattern)
        O[Orchestrator] --> W1[Worker A]
        O --> W2[Worker B]
    end

    subgraph 2. Sequential (Pipeline Pattern)
        P1[Step 1 Agent] --> P2[Step 2 Agent] --> P3[Step 3 Agent]
    end

    subgraph 3. Peer Mesh (Collaborative Pattern)
        M1[Peer Agent A] <--> M2[Peer Agent B]
        M2 <--> M3[Peer Agent C]
    end
```

### Topology Comparison Matrix

| Topology | Best Used For | Message Passing Overhead | Failure Resilience |
| :--- | :--- | :--- | :--- |
| **Hierarchical (Orchestrator-Worker)** | Complex software engineering & research tasks | Moderate (Centralized routing) | High (Orchestrator can re-assign failing sub-tasks) |
| **Sequential (Pipeline)** | Data transformation & sequential document drafting | Low (Direct forward push) | Medium (Breakage at stage N halts downstream stages) |
| **Peer Mesh** | Multi-perspective debate & consensus building | High (N-to-N message broadcast) | Low/Moderate (Risk of cyclical infinite chatter) |

---

## ✉ 3. OpenClaw Inter-Agent Messaging Primitive

OpenClaw implements a JSON-RPC based internal message bus (`claw-bus`) for inter-agent communication.

### Message Envelope Structure
```json
{
  "messageId": "msg_9948271048",
  "senderAgentId": "orchestrator-lead-01",
  "recipientAgentId": "research-worker-01",
  "sessionId": "sess_20260730_01",
  "timestamp": "2026-07-30T10:15:30Z",
  "payload": {
    "action": "EXECUTE_SUBTASK",
    "taskDescription": "Extract recent research papers on MCP transport security",
    "constraints": {
      "maxSearchDepth": 3,
      "timeLimitSeconds": 120
    }
  }
}
```

---

## 💾 4. Shared State vs Isolated Memory

- **Isolated Ephemeral Memory**: Each sub-agent maintains its own local chat history during sub-task execution. Upon task return, local context is garbage collected.
- **Shared State Store**: Long-lived key-value metadata and intermediate artifacts are persisted to SQLite/Redis accessible by all agents via shared keys.
