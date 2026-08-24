# Definition Agent

## Completion Status
Successfully created and verified in Multica as part of the five-agent MCP exercise.

## Model
**DeepSeek — via OpenCode**

## MCP Server
**Dictionary Server**

The agent was configured to use a public dictionary MCP server for word definitions and examples.

## MCP JSON

```json
{
  "mcpServers": {
    "dictionary-server": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-server-dictionary"
      ],
      "disabled": false
    }
  }
}
```

## SKILL.md

```md
# Skill: definition

## Objective
Provide clear and accurate definitions of words and demonstrate their usage in context.

## Instructions
- Use the available dictionary MCP tool when a definition is requested.
- Return the primary meaning in clear language.
- Include relevant parts of speech when available.
- Provide an example sentence demonstrating natural usage.
- Do not fabricate dictionary information when the MCP tool cannot retrieve the requested word.
- Keep the explanation concise unless the user asks for more detail.
```

## Verification
The Definition Agent was manually verified after MCP configuration.
