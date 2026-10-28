# HackerNews Digest Agent

This document details the specification, MCP server integration, test issue, and output verification for the **HackerNews Digest Agent**.

---

## 🎯 1. Objective

To build an autonomous tech news digest agent capable of fetching top HackerNews stories, extracting comment threads, evaluating community sentiment, and compiling executive summaries.

---

## ⚡ 2. MCP Server

- **MCP Server Package**: `@mcp-tools/hackernews-digest-server`
- **Transport**: STDIO (`npx -y @mcp-tools/hackernews-digest-server`)
- **Exposed Tools**: `get_top_stories`, `get_item_details`, `get_story_comments`

---

## 🤖 3. Agent Responsibility

- **Agent ID**: `hackernews-digest-agent-01`
- **Primary Function**: Queries the official Firebase HackerNews API via MCP server primitives, filters stories by point thresholds, parses top comment threads, and categorizes tech trends.

---

## 🧪 4. Test Issue / Prompt

> **Test Issue**: *"Fetch top 3 trending stories on HackerNews related to AI/LLMs today, summarize their key points, and report community sentiment from top comments."*

---

## 📤 5. Expected Output

```markdown
### 📰 HackerNews Tech Digest - AI & Agent Focus

#### 1. 🚀 [Model Context Protocol v1.0 Spec Released](https://news.ycombinator.com/item?id=99281)
- **Points**: 482 | **Comments**: 184
- **Summary**: Anthropic releases open spec for connecting LLMs to external tools and data stores over STDIO and HTTP.
- **Community Sentiment**: Highly positive (85%). Developers praise standardizing tool integration over custom REST wrappers.

#### 2. ⚡ [OpenCode Sandbox Benchmarks Exceed Docker Execution](https://news.ycombinator.com/item?id=99342)
- **Points**: 310 | **Comments**: 95
- **Summary**: Benchmark evaluation showing gVisor sandboxes executing Python interpreter sub-tasks 3x faster than full containers.
- **Community Sentiment**: Mixed/Cautious. Concerns raised around memory limits under extreme multi-tenant concurrency.
```
