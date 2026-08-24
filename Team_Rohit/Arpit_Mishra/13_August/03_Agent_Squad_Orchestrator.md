# 3. Agent Squad: Orchestrator + Specialized Agents

## Objective

Create a multi-agent squad where an **Orchestrator Agent** coordinates specialized agents.

The important design principle is:

> The Orchestrator should coordinate work, not try to perform every specialized task itself.

A useful architecture is:

```text
                         User
                          |
                          v
                 +------------------+
                 |  Orchestrator    |
                 |      Agent       |
                 +------------------+
                    /    |    |    \
                   /     |    |     \
                  v      v    v      v
             Research  MCP  Coding  Reviewer
              Agent   Agent  Agent    Agent
```

## Agents

### 1. Orchestrator Agent

**Role:** Project manager / coordinator.

Responsibilities:

- Understand the user's objective.
- Break the objective into subtasks.
- Select the appropriate specialist.
- Dispatch tasks.
- Track task status.
- Combine outputs.
- Detect missing or contradictory information.
- Ask another agent for verification when necessary.
- Produce the final response.

The Orchestrator should not duplicate every specialist's work.

### 2. Research Agent

**Role:** Information gathering and source verification.

Responsibilities:

- Search documentation.
- Find authoritative sources.
- Extract relevant facts.
- Compare multiple sources.
- Identify outdated information.
- Return concise research findings with sources.

Example task:

```text
"Find the current MCP transport specifications
and explain STDIO vs Streamable HTTP."
```

Output:

```text
Research Result
- Finding 1
- Finding 2
- Finding 3
- Sources
- Confidence / uncertainty
```

### 3. MCP Specialist Agent

**Role:** MCP architecture and protocol specialist.

Responsibilities:

- Explain MCP concepts.
- Analyze MCP architecture.
- Explain Host / Client / Server.
- Analyze tools, resources and prompts.
- Explain STDIO and Streamable HTTP.
- Identify protocol/version differences.
- Review MCP implementation decisions.

Example task:

```text
"Determine which MCP transport is appropriate
for a local development tool."
```

### 4. Coding / Implementation Agent

**Role:** Build the technical implementation.

Responsibilities:

- Write implementation code.
- Create MCP servers/clients.
- Design APIs.
- Handle configuration.
- Implement error handling.
- Create tests.
- Explain how to run the implementation.

Example task:

```text
"Create a minimal MCP server exposing
a calculator tool."
```

### 5. Reviewer Agent

**Role:** Quality control.

Responsibilities:

- Check technical correctness.
- Detect unsupported assumptions.
- Check code for bugs.
- Verify that requirements were satisfied.
- Identify security issues.
- Compare the final result against authoritative documentation.

Example:

```text
Input:
Research Agent + MCP Specialist + Coding Agent outputs

Reviewer:
- Is this technically correct?
- Is anything outdated?
- Are there contradictions?
- Are security concerns missing?
```

## Optional Sixth Agent: Security Agent

For serious MCP systems, a dedicated security agent is useful.

Responsibilities:

- Authentication analysis.
- Authorization analysis.
- Tool permission review.
- Prompt injection risk analysis.
- SSRF/DNS rebinding analysis.
- Secret management.
- Network exposure review.

This is particularly relevant for Streamable HTTP MCP servers because the official specification explicitly discusses Origin validation, localhost binding, and authentication. citeturn0search4

## Communication Model

The squad should not allow every agent to communicate with every other agent without control.

That creates unnecessary complexity.

Prefer:

```text
                Orchestrator
                /    |    |    \
               /     |    |     \
         Research   MCP  Coding  Reviewer
```

Instead of:

```text
Research <----> MCP
   ^  \          /  ^
   |   \        /   |
   v    \      /    v
Coding <----> Reviewer
```

The first architecture is easier to reason about and debug.

## Task Lifecycle

### Step 1: Receive Request

```text
User:
"Research MCP and design an MCP-based agent system."
```

### Step 2: Orchestrator Decomposes Task

```text
Task A -> Research MCP
Task B -> Analyze transports
Task C -> Design agent architecture
Task D -> Review architecture
```

### Step 3: Delegate

```text
Research Agent:
Task A

MCP Specialist:
Task B

Coding Agent:
Task C
```

### Step 4: Collect Results

```text
             +----------------+
             | Orchestrator   |
             +----------------+
               ^    ^     ^
               |    |     |
             Research MCP Coding
```

### Step 5: Review

The Orchestrator sends the combined design to the Reviewer.

```text
Research
   |
MCP -----> Orchestrator -----> Reviewer
   |              ^
Coding ----------/
```

### Step 6: Finalize

The Orchestrator resolves review feedback and generates the final output.

## Example Squad Task

User asks:

> "Build an AI application that can access files, search documentation, and execute approved developer tools."

### Orchestrator

Breaks it into:

```text
1. Research MCP capabilities.
2. Determine appropriate transport.
3. Design MCP server architecture.
4. Design agent delegation.
5. Implement tools.
6. Security review.
```

### Research Agent

Finds:

```text
MCP supports tools/resources/prompts.
STDIO is appropriate for local process-based integrations.
Streamable HTTP is appropriate for networked services.
```

### MCP Specialist

Designs:

```text
AI Host
   |
MCP Clients
   |
   +---- File MCP Server
   +---- Documentation MCP Server
   +---- Developer Tools MCP Server
```

### Coding Agent

Implements:

```text
tools:
- read_file
- search_docs
- run_approved_command
```

### Security Agent

Rejects:

```text
run_any_command(command)
```

and recommends:

```text
run_approved_command(tool_name, validated_arguments)
```

because unrestricted shell execution gives the agent excessive authority.

### Reviewer

Checks:

```text
[✓] MCP architecture
[✓] Transport selection
[✓] Tool boundaries
[✓] Security controls
[✓] Error handling
[✓] Requirements
```

## Orchestrator Decision Logic

A simple decision flow:

```text
                    User Request
                         |
                         v
                  Understand Task
                         |
                         v
                  Break Into Tasks
                         |
              +----------+----------+
              |          |          |
              v          v          v
           Research    Design     Coding
              |          |          |
              +----------+----------+
                         |
                         v
                     Integrate
                         |
                         v
                      Review
                         |
                 +-------+-------+
                 |               |
               Failed           Passed
                 |               |
                 v               v
            Re-delegate       Final Answer
```

## Task Contract

Every agent should receive a structured task.

Example:

```json
{
  "task_id": "mcp-transport-001",
  "agent": "mcp_specialist",
  "objective": "Compare STDIO and Streamable HTTP",
  "context": "We are designing a multi-agent MCP system",
  "requirements": [
    "Explain architecture",
    "Explain deployment",
    "Explain security",
    "Recommend use cases"
  ],
  "output_format": "markdown"
}
```

## Agent Output Contract

Every agent should return something structured:

```json
{
  "task_id": "mcp-transport-001",
  "status": "completed",
  "summary": "STDIO is suited to local process-based MCP servers.",
  "findings": [],
  "risks": [],
  "sources": [],
  "needs_review": false
}
```

This prevents the Orchestrator from having to parse completely arbitrary responses.

## How MCP Fits Into the Squad

MCP should be treated as the **connectivity layer**, not the orchestration brain.

For example:

```text
                 Orchestrator Agent
                         |
                  MCP Client Layer
               /          |          \
              /           |           \
             v            v            v
      Research MCP   Developer MCP   Database MCP
          Server          Server          Server
             |              |              |
         search_web     run tools      query DB
```

The Orchestrator decides **what should happen**.

MCP provides a standardized mechanism for **accessing external capabilities**.

That distinction is critical.

## Recommended Final Architecture

```text
                              USER
                               |
                               v
                    +---------------------+
                    |   ORCHESTRATOR      |
                    |       AGENT         |
                    +---------------------+
                       /      |       \
                      /       |        \
                     v        v         v
              +---------+ +--------+ +---------+
              |Research | |   MCP  | | Coding  |
              | Agent   | |Special.| | Agent   |
              +---------+ +--------+ +---------+
                   \          |          /
                    \         |         /
                     +---------+--------+
                               |
                               v
                        +-------------+
                        |   Reviewer  |
                        |    Agent    |
                        +-------------+
                               |
                               v
                         Final Result
```

For production systems, add:

```text
                    Security Agent
                          |
                          v
                 Security Validation
```

before sensitive tool execution or final approval.

## Key Design Rules

1. **One Orchestrator owns task coordination.**
2. **Specialist agents should have narrow responsibilities.**
3. **Do not let every agent freely call every other agent.**
4. **Use structured task and result contracts.**
5. **Require review for high-impact operations.**
6. **Keep tool permissions narrow.**
7. **Treat MCP as a connectivity/protocol layer, not as the multi-agent orchestration framework.**
8. **Use authoritative MCP documentation when protocol behavior matters.**
9. **Version-pin or verify MCP specifications because protocol revisions can change transport behavior.**
10. **Do not give an agent unrestricted shell/database/file-system access just because MCP makes the tool available.**

## Final Mental Model

Think of the architecture as three separate layers:

```text
Layer 1: Intelligence
--------------------------------
Orchestrator + Specialist Agents


Layer 2: Connectivity
--------------------------------
MCP Client + MCP Protocol


Layer 3: Capabilities
--------------------------------
Tools + Resources + External Services
```

The agents decide **what to do**.

MCP standardizes **how the AI application connects to capabilities**.

The external services actually **perform the work or provide the data**.
