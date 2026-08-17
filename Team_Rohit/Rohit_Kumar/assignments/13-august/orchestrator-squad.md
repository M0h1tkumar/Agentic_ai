# Orchestrator Agent and Multi-Agent Squad

## Introduction

An AI Agent can perform a specific task, but complex systems often require multiple specialized agents.

Instead of creating one large agent that performs every task, a **Multi-Agent Squad** can be created where each agent has a specific responsibility.

An **Orchestrator Agent** coordinates these specialized agents and decides which agent should handle a particular task.

---

## What is an Orchestrator Agent?

An Orchestrator Agent is a central agent responsible for:

* Understanding the user's request
* Breaking complex requests into tasks
* Selecting the appropriate agent
* Assigning tasks
* Combining results
* Handling failures
* Returning the final response to the user

The orchestrator does not need to perform every task itself.

Its main responsibility is **coordination**.

---

## Multi-Agent Squad

The existing Multica agents can be organized into a squad:

```text
                         User
                           |
                           v
                    Orchestrator Agent
                           |
       +-------------------+-------------------+
       |         |         |         |         |
       v         v         v         v         v
   Weather    Wikipedia  GitHub   Currency   HackerNews
    Agent      Agent      Agent     Agent      Agent
       |
       +--------------------------------------+
       |                                      |
       v                                      v
 Definition Agent                       World Clock Agent
```

---

## Squad Members

### 1. Weather Agent

**Purpose:** Provide current weather and forecasts.

Example:

```text
"What is the weather in Bhubaneswar?"
```

Possible tools:

* AccuWeather MCP
* Weather APIs

---

### 2. Explainer Agent

**Purpose:** Explain people, places, topics, and events.

It can use the Wikipedia MCP server.

Example:

```text
"Give me a summary of Mahatma Gandhi."
```

Possible tool:

```text
@cyanheads/wikipedia-mcp-server
```

---

### 3. Currency Converter Agent

**Purpose:** Convert currencies and provide current exchange rates.

Example:

```text
"Convert 500 USD to INR."
```

Possible tools:

* Currency API
* Exchange-rate MCP server

---

### 4. World Clock Agent

**Purpose:** Provide current time for different locations.

Example:

```text
"What time is it in Tokyo?"
```

---

### 5. Definition Agent

**Purpose:** Explain words and provide examples.

Example:

```text
"Define ubiquitous and use it in a sentence."
```

---

### 6. HackerNews Agent

**Purpose:** Retrieve and summarize current Hacker News stories.

Example:

```text
"Give me the top 5 Hacker News stories."
```

Possible tool:

* Hacker News API
* Hacker News MCP server

---

### 7. GitHub Repository Agent

**Purpose:** Retrieve GitHub repository information.

Example:

```text
"How many open issues does anthropics/claude-code have?"
```

Possible tools:

* GitHub API
* GitHub MCP server

---

### 8. World Clock Agent

**Purpose:** Provide current times across different cities and time zones.

Example:

```text
"What time is it in Tokyo, London, and New York?"
```

---

## Role of the Orchestrator

The Orchestrator receives the user's request and determines which specialized agent should handle it.

### Example 1

User:

```text
What is the weather in Bhubaneswar?
```

The orchestrator identifies this as a weather-related request.

```text
User
  |
  v
Orchestrator
  |
  v
Weather Agent
  |
  v
Weather MCP
  |
  v
Result
```

---

## Example 2

User:

```text
How many open issues does anthropics/claude-code have?
```

The orchestrator identifies this as a GitHub request.

```text
User
  |
  v
Orchestrator
  |
  v
GitHub Repo Agent
  |
  v
GitHub API / MCP
  |
  v
Result
```

---

## Example 3

User:

```text
Convert 500 USD to INR and tell me the current time in Tokyo.
```

This request contains two independent tasks.

The orchestrator can split the request:

```text
                   User
                     |
                     v
              Orchestrator
                /        \
               /          \
              v            v
       Currency Agent   World Clock Agent
              |            |
              v            v
        Exchange API    Time Service
              |            |
              +------┬-----+
                     |
                     v
              Combined Result
```

The orchestrator combines both results and returns one response.

---

## Orchestrator Workflow

A simplified workflow is:

```text
1. Receive user request
          |
          v
2. Understand request
          |
          v
3. Identify required task(s)
          |
          v
4. Select agent(s)
          |
          v
5. Send task(s)
          |
          v
6. Receive results
          |
          v
7. Validate / combine results
          |
          v
8. Return final response
```

---

## Agent Communication

The orchestrator should pass clear instructions to each agent.

Example:

```text
Task:
Retrieve the current weather for Bhubaneswar.

Assigned Agent:
Weather Agent

Expected Result:
Current temperature, conditions, and forecast.
```

This keeps responsibilities clear.

---

## Agent Specialization

Each agent should have:

### System Prompt

Defines what the agent is responsible for.

### Skills

Defines how the agent should behave.

### Tools

Defines what external capabilities the agent can use.

### Permissions

Defines what the agent is allowed to access.

Example:

```text
Weather Agent
     |
     +-- System Prompt
     |
     +-- Weather Skill
     |
     +-- Weather MCP Tool
     |
     +-- API Permission
```

---

## Benefits of the Squad Architecture

### Specialization

Each agent focuses on one domain.

### Modularity

Agents can be developed independently.

### Reusability

The same agent can be used by multiple workflows.

### Easier Debugging

A failure can be isolated to a particular agent or tool.

### Scalability

New agents can be added without redesigning the complete system.

For example:

```text
Existing Squad
     |
     +-- News Agent
     +-- Weather Agent
     +-- GitHub Agent
     |
     v
Add Finance Agent
```

The orchestrator can then route finance-related requests to the new agent.

---

## Possible Squad Architecture in Multica

```text
                         ┌───────────────────┐
                         │       User        │
                         └─────────┬─────────┘
                                   |
                                   v
                         ┌───────────────────┐
                         │   Orchestrator    │
                         │      Agent        │
                         └─────────┬─────────┘
                                   |
          +------------------------+------------------------+
          |            |            |          |            |
          v            v            v          v            v
     Weather       Explainer      GitHub    Currency     HackerNews
      Agent          Agent         Agent      Agent        Agent
          |            |            |          |            |
          v            v            v          v            v
      Weather        Wiki         GitHub     Currency     HackerNews
       MCP           MCP           MCP        MCP/API        API
          |
          +-------------------+-------------------+
                              |
                              v
                     Definition / Clock
                          Agents
```

---

## Example Multi-Agent Request

User:

```text
Tell me the weather in Bhubaneswar,
convert 500 USD to INR,
and tell me the current time in Tokyo.
```

The orchestrator decomposes the task:

```text
Task 1 → Weather Agent
Task 2 → Currency Agent
Task 3 → World Clock Agent
```

The agents execute their tasks independently.

The orchestrator then combines:

```text
Weather Result
+
Currency Result
+
Time Result
```

and generates the final response.

---

## Error Handling

The orchestrator should also handle failures.

Example:

```text
Currency Agent
      |
      X
Exchange API unavailable
      |
      v
Orchestrator
      |
      v
Tell user that currency data
could not be retrieved
```

The orchestrator should not invent missing tool results.

---

## Security Considerations

Each agent should have only the permissions required for its task.

For example:

```text
Weather Agent
     |
     +-- Weather API
     X-- GitHub Write Access
```

A read-only GitHub agent should not receive permission to delete repositories or modify issues.

This follows the principle of least privilege.

---

## Conclusion

A Multi-Agent Squad divides a large AI system into specialized agents.

The **Orchestrator Agent** acts as the central coordinator that:

* Understands the request
* Selects agents
* Splits tasks
* Coordinates execution
* Combines results
* Handles failures
* Returns the final response

For the Multica project, a squad containing the Weather, Explainer, Currency, World Clock, Definition, HackerNews, and GitHub agents provides a practical demonstration of multi-agent orchestration.

The architecture can later be extended by adding new specialized agents without changing the entire system.

## References

* Model Context Protocol Documentation
* Multica Agent Architecture
* MCP Tool and Agent Integration Concepts
