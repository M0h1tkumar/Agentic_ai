# HackerNews Digest Agent

## Completion Status
Successfully created and tested in Multica as part of the five-agent MCP exercise.

## Model
**DeepSeek — via OpenCode**

## MCP Server
**Hacker News MCP**

The agent uses a public Hacker News MCP server to retrieve live Hacker News stories and their metadata.

## MCP JSON

```json
{
  "mcpServers": {
    "hackernews": {
      "command": "npx",
      "args": [
        "-y",
        "@isteam/hackernews-mcp"
      ]
    }
  }
}
```

## SKILL.md

```md
# Skill: hacker-news-digest

## Objective
Retrieve and present current Hacker News stories and their associated metadata using the available MCP tools.

## Instructions
- Use the Hacker News MCP tools for live story data.
- Retrieve the requested number of highest-ranked or top stories.
- Present each story with its title and score.
- Include the author when the MCP tool provides it.
- Preserve the ranking order returned by the source.
- Do not invent scores, titles, authors, or rankings.
- Mention that rankings can change when appropriate.
- Keep the final digest structured and easy to scan.
```

## Verification
The agent successfully called the Hacker News MCP tool and returned ranked stories with scores and authors.
