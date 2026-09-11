# Wikipedia Explainer Agent

This document details the configuration, skill definitions, and test execution for the **Wikipedia Explainer Agent**, built to autonomously retrieve, summarize, and explain complex concepts using Wikipedia articles.

---

## 🎯 1. Objective

To build an agent capable of performing multi-step background research, fetching article summaries, searching topic categories, and synthesizing structured educational explanations from Wikipedia data.

---

## ⚡ 2. Wikipedia MCP Server Integration

The agent utilizes the official Model Context Protocol Wikipedia server package: `@modelcontextprotocol/server-wikipedia`.

### Server Configuration (`wikipedia_mcp.json`)
```json
{
  "mcpServers": {
    "wikipedia": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-wikipedia"
      ]
    }
  }
}
```

---

## 🛠 3. Skill Definition (`wikipedia_explainer_skill.json`)

```json
{
  "skillName": "Wikipedia-Concept-Explainer",
  "agentId": "wikipedia-explainer-agent-01",
  "tools": [
    "wikipedia_search",
    "wikipedia_get_summary",
    "wikipedia_get_sections"
  ],
  "systemInstruction": "Given a subject query, search Wikipedia, extract top matching summaries, parse key section headings, and formulate a clear 3-part structured breakdown (Overview, Key Pillars, Historical Context)."
}
```

---

## 🧪 4. Testing Query

> **Test Query**: *"Explain the concept of Quantum Entanglement using Wikipedia context and list its core physical principles."*

---

## 📤 5. Execution Output

### Tool Call Log
```json
{
  "invokedTool": "wikipedia_get_summary",
  "args": { "title": "Quantum_entanglement" }
}
```

### Formatted Agent Output

```markdown
### ⚛️ Concept Explanation: Quantum Entanglement

**Source**: Wikipedia - [Quantum entanglement](https://en.wikipedia.org/wiki/Quantum_entanglement)

#### 1. Overview
**Quantum Entanglement** is a phenomenon in quantum physics where a group of particles interact in ways such that the quantum state of each particle cannot be described independently of the state of the others, even when the particles are separated by a large distance.

#### 2. Core Physical Principles
- **Non-Locality**: Measurement of one entangled particle instantly determines the state of its paired particle, famously dubbed "spooky action at a distance" by Albert Einstein.
- **State Superposition**: Entangled systems remain in a superposition of states until an observation forces a collapse into a definitive state.
- **Applications**: Fundamental to Quantum Computing, Quantum Cryptography (QKD), and Quantum Teleportation protocols.

#### 3. Key Section Breakdown
1. *History & EPR Paradox*
2. *Bell's Theorem & Experimental Tests*
3. *Modern Applications in Quantum Information Science*
```
