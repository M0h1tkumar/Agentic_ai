# GitHub Repo Agent

## Completion Status
Successfully created and tested in Multica as part of the five-agent MCP exercise.

## Model
**DeepSeek — via OpenCode**

## MCP Server
**GitHub MCP Server**

The GitHub MCP server was installed as a native Linux binary inside the Multica worker because Docker and Go were not available inside that container. The x86_64 Linux release was downloaded and extracted successfully.

## MCP JSON

```json
{
  "mcpServers": {
    "github": {
      "command": "/usr/local/bin/github-mcp-server",
      "args": [
        "stdio"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}",
        "GITHUB_READ_ONLY": "1"
      }
    }
  }
}
```

> The actual GitHub token is intentionally not included in this documentation. It should remain an environment secret.

## SKILL.md

```md
# Skill: github-repo-info

## Objective
Retrieve and analyze GitHub repository and issue information using the available GitHub MCP tools.

## Instructions
- Use the GitHub MCP tools for repository and issue information.
- Identify the requested repository precisely.
- For issue counts, distinguish open issues from pull requests when the tool/API provides that distinction.
- For recently updated issues, request or sort by update time rather than relying on issue creation time.
- Return issue numbers, titles, and update timestamps when relevant.
- Do not fabricate repository statistics or issue data.
- Clearly indicate when information is retrieved live from GitHub.
- Keep the final response structured and concise.
```

## Verification
The agent successfully called the GitHub MCP `github_list_issues` tool and retrieved live issue data from `anthropics/claude-code`, including the open-issue count and recently updated issues.
