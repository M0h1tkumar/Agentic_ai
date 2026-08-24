# World Clock Agent

## Completion Status
Successfully created and tested in Multica as part of the five-agent MCP exercise.

## Model
**DeepSeek — via OpenCode**

## MCP Server
**time-mcp by yokingma**

The server was used through `npx` and exposed time-awareness tools including current time, relative time, and timezone conversion.

## MCP JSON

```json
{
  "mcpServers": {
    "time-mcp": {
      "command": "npx",
      "args": [
        "-y",
        "time-mcp"
      ]
    }
  }
}
```

## SKILL.md

```md
# Skill: world-clock

## Objective
Provide accurate current-time and timezone information using the available MCP time tools.

## Instructions
- Use the MCP time tools whenever the user asks for a current time or timezone-related calculation.
- Resolve a city to its appropriate IANA timezone when necessary.
- Use the current-time tool for current local time.
- Use timezone-conversion tools when converting between locations.
- Use relative-time tools for requests involving a past or future time.
- Do not guess the current time from memory.
- Clearly identify the location, local date, local time, and timezone when relevant.
- Keep the final answer concise.
```

## Verification
The agent successfully called the time MCP tools. Tests included current local time and relative-time calculations.
