# Definition Agent

This document details the specification, MCP server integration, test issue, and output verification for the **Definition Agent**.

---

## 🎯 1. Objective

To provide an autonomous lexical and technical definition agent capable of looking up dictionary definitions, synonyms, etymology, and domain-specific technical terminology.

---

## ⚡ 2. MCP Server

- **MCP Server Package**: `@mcp-tools/dictionary-definition-server`
- **Transport**: STDIO (`npx -y @mcp-tools/dictionary-definition-server`)
- **Exposed Tools**: `lookup_word`, `get_synonyms`, `parse_technical_jargon`

---

## 🤖 3. Agent Responsibility

- **Agent ID**: `definition-agent-01`
- **Primary Function**: Parses user requests for term definitions, differentiates between general linguistic meaning vs software/engineering context, and provides concise summaries with example usage sentences.

---

## 🧪 4. Test Issue / Prompt

> **Test Issue**: *"Define the term 'Idempotency' in the context of REST APIs and Distributed Systems, and provide synonyms and example code usage."*

---

## 📤 5. Expected Output

```markdown
### 📖 Term Definition: Idempotency

**Category**: Software Engineering / Distributed Systems / REST API Architecture  
**Phonetic**: `/ˌaɪdɛmˈpoʊtənsi/`

#### 1. Technical Definition
**Idempotency** is the property of certain operations in mathematics and computer science whereby they can be applied multiple times without changing the result beyond the initial application. In REST APIs, `GET`, `PUT`, and `DELETE` requests must be idempotent.

#### 2. Synonyms & Related Terms
- *Repeatable Operation*, *State-Invariant Execution*, *Deterministic Mutation*.

#### 3. API Code Context Example
```http
-- Invoking DELETE /api/v1/users/42 once: HTTP 204 No Content (User deleted)
-- Invoking DELETE /api/v1/users/42 second time: HTTP 204 No Content or HTTP 404 (State remains unchanged)
```
