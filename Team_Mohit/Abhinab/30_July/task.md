# 7. 30 July Tasks

## Session 1 and Session 2

Once the provided files are available:

1.  Read Session 1.
2.  Extract objectives.
3.  Complete exercises.
4.  Read Session 2.
5.  Complete exercises.
6.  Record commands/results.
7.  Commit notes to GitHub.

Suggested format:

``` markdown
# Session 1

## Objective
## Commands
## Result
## Issues
## Learning

# Session 2

## Objective
## Commands
## Result
## Issues
## Learning
```

## OpenClaw multi-agent team

Recommended architecture:

``` text
                    Orchestrator
                         |
          +--------------+--------------+
          |              |              |
          v              v              v
      Researcher       Coder         Reviewer
          |              |              |
          +--------------+--------------+
                         |
                         v
                     Finalizer
```

Roles:

  Agent          Responsibility
  -------------- --------------------------
  Orchestrator   Break task into subtasks
  Researcher     Research
  Coder          Implement
  Tester         Test
  Reviewer       Review
  Finalizer      Final output

## Messaging bot alternative

``` text
Telegram / Discord
        |
        v
Bot
        |
        v
OpenClaw
        |
        v
Tools / Skills / MCP
        |
        v
Result
```

Security:

-   restrict allowed users
-   no unrestricted shell access
-   keep tokens in environment variables
-   log tool calls
-   sandbox risky operations
