# World Clock Agent

This document details the specification, MCP server integration, test issue, and output verification for the **World Clock Agent**.

---

## 🎯 1. Objective

To provide an autonomous timezone manager agent capable of resolving current local times across international cities, calculating UTC offsets, and scheduling cross-border meeting windows.

---

## ⚡ 2. MCP Server

- **MCP Server Package**: `@mcp-tools/world-clock-server`
- **Transport**: STDIO (`npx -y @mcp-tools/world-clock-server`)
- **Exposed Tools**: `get_current_time`, `calculate_time_difference`, `find_overlapping_slots`

---

## 🤖 3. Agent Responsibility

- **Agent ID**: `world-clock-agent-01`
- **Primary Function**: Resolves city/country names to IANA timezone identifiers (e.g., `America/New_York`, `Asia/Tokyo`, `Europe/London`), computes time differences, and recommends optimal meeting times.

---

## 🧪 4. Test Issue / Prompt

> **Test Issue**: *"Compare the current time in San Francisco, London, Dubai, and Tokyo. Recommend a 1-hour meeting window that falls between 09:00 and 18:00 local time for all participants if possible."*

---

## 📤 5. Expected Output

```markdown
### ⏰ Global Timezone Comparison

| Location | IANA Timezone | Current Local Time | UTC Offset | Business Hours Status |
| :--- | :--- | :--- | :--- | :--- |
| **San Francisco** | `America/Los_Angeles` | 07:30 AM | UTC-7 | 🟡 Early Morning |
| **London** | `Europe/London` | 03:30 PM | UTC+1 | 🟢 Business Hours |
| **Dubai** | `Asia/Dubai` | 06:30 PM | UTC+4 | 🟡 Evening |
| **Tokyo** | `Asia/Tokyo` | 11:30 PM | UTC+9 | 🔴 Night |

#### 📅 Recommended Meeting Slot
- **Optimal Window**: **15:00 UTC** (08:00 AM San Francisco / 04:00 PM London / 07:00 PM Dubai / 12:00 AM Tokyo).
```
