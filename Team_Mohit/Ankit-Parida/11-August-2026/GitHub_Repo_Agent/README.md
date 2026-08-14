# GitHub Repository Manager Agent

This document details the specification, MCP server integration, test issue, and output verification for the **GitHub Repo Agent**.

---

## 🎯 1. Objective

To provide an autonomous software engineering assistant agent capable of inspecting GitHub repositories, auditing open issues, reviewing pull requests, and tracking commit histories.

---

## ⚡ 2. MCP Server

- **MCP Server Package**: `@modelcontextprotocol/server-github`
- **Transport**: STDIO (`npx -y @modelcontextprotocol/server-github`)
- **Exposed Tools**: `search_repositories`, `list_issues`, `get_pull_request`, `list_commits`

---

## 🤖 3. Agent Responsibility

- **Agent ID**: `github-repo-agent-01`
- **Primary Function**: Integrates with GitHub REST & GraphQL APIs via MCP, analyzes code changes in PR diffs, triages open issue labels, and reports repository metrics.

---

## 🧪 4. Test Issue / Prompt

> **Test Issue**: *"Inspect open issue #42 on repository 'multica/multica-core', summarize the reported bug, and suggest a resolution based on recent commit history."*

---

## 📤 5. Expected Output

```markdown
### 🐙 GitHub Issue Audit Report

**Repository**: `multica/multica-core`  
**Issue #42**: *Memory leak during long-running sub-agent RPC communication loop*  
**Status**: 🔴 Open | **Labels**: `bug`, `high-priority`, `runtime`

#### 1. Issue Breakdown
The user reports that after ~2 hours of continuous agent delegation, the Multica daemon memory consumption spikes from 256MB to over 3.2GB.

#### 2. Root Cause Analysis
Inspecting recent commits (`git log -n 5` via MCP tool):
- Commit `8f3a1b`: *Added unbounded message buffer to claw-bus RPC listener.*
- The event buffer fails to release completed sub-agent message payloads after response transmission.

#### 3. Recommended Resolution
Apply memory flush hook inside `claw-bus/index.js` immediately following event dispatch confirmation:
```javascript
// Add explicit stream cleanup
clawBus.on('message_delivered', (msgId) => {
  eventBuffer.delete(msgId);
});
```
