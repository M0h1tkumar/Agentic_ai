# Currency Converter Agent

## Completion Status
Successfully created and tested in Multica as part of the five-agent MCP exercise.

## Model
**DeepSeek — via OpenCode**

## MCP Server
**ExchangeRate.dev MCP**

The MCP endpoint used for currency-rate access was:

`https://api.exchangerate.dev/v1/mcp`

## MCP JSON

```json
{
  "mcpServers": {
    "exchangerate-dev": {
      "url": "https://api.exchangerate.dev/v1/mcp"
    }
  }
}
```

## SKILL.md

```md
# Skill: currency-converter

## Objective
Provide accurate currency conversion and exchange-rate information by using the available MCP currency tools.

## Instructions
- Use the MCP currency tools for exchange-rate information rather than guessing or relying on memory.
- Identify the source and target currencies and the amount to convert.
- Use the conversion tool for the requested conversion.
- When asked for a current exchange rate, retrieve the current rate through the MCP server.
- Clearly state the converted amount and the relevant exchange rate.
- Do not invent a rate when the MCP server cannot provide one.
- Keep the final response concise and easy to read.
```

## Verification
The agent was tested through Multica with currency-conversion requests and MCP tool calling.
