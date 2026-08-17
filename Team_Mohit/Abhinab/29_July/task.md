# 8. 29 July Tasks

## 8.1 Positive and negative aspects of coding agents in Visual Studio Code / GitHub Copilot

GitHub Copilot agent mode can autonomously work through multi-step
tasks, determine files to change, use terminal commands, and iterate.

Source:
https://docs.github.com/en/copilot/how-tos/chat-with-copilot/chat-in-ide

### Positives

1.  Faster development
2.  Repository-aware changes
3.  Multi-step execution
4.  Terminal/tool integration
5.  Good for repetitive tasks
6.  Can generate tests/documentation
7.  Can work with MCP integrations

### Negatives

1.  Incorrect changes
2.  Permission risk
3.  Hallucinated implementation
4.  Hidden dependency changes
5.  Token/model cost
6.  Security risks
7.  Human review is still required

GitHub documents that autonomous modes are best for well-defined tasks
and warns about trust, permissions, and cost.

Source:
https://docs.github.com/en/copilot/concepts/agents/copilot-cli/autopilot

------------------------------------------------------------------------

# 9. OAuth Dynamic/Session-Based vs API Key Static/Permanent

## OAuth

OAuth is a delegated authorization framework.

``` text
User
 |
 v
Authorization Server
 |
 | access token
 v
Application
 |
 v
Resource API
```

OAuth access tokens are credentials used to access protected resources.

Source: https://oauth.net/2/access-tokens/

## API key

A static API key is a secret credential:

``` text
Application
 |
 | API key
 v
API
```

## Comparison

  Feature           OAuth                              Static API key
  ----------------- ---------------------------------- -------------------------
  User delegation   Strong                             Usually absent
  Expiration        Usually supported                  Often long-lived
  Rotation          Token lifecycle                    Manual/key rotation
  Scope             Fine-grained scopes possible       Provider-dependent
  Revocation        Authorization/token revocation     Key revocation
  Identity          Can represent user authorization   Usually app/project
  Complexity        Higher                             Lower
  Best use          User-facing apps                   Simple server-to-server

### OAuth positives

-   short-lived access tokens
-   user consent
-   scoped permissions
-   refresh-token workflow
-   delegation
-   separation of identity and application

Refresh tokens can obtain new access tokens without requiring user
interaction.

Source: https://oauth.net/2/refresh-tokens/

### OAuth negatives

-   more implementation complexity
-   redirect/callback flow
-   token lifecycle management
-   refresh-token security
-   provider-specific behavior

### API key positives

-   simple
-   easy to implement
-   good for server-to-server
-   low complexity

### API key negatives

-   leaked keys may remain useful until revoked
-   poor user-level authorization model
-   manual rotation
-   accidental Git commits are common
-   generally less granular

### Recommendation

``` text
User-facing app -> OAuth
Internal service -> API key/service credential
```

Use short-lived and scoped credentials whenever possible.

------------------------------------------------------------------------

# 10. OpenClaw Installation/Onboarding

Recommended sequence:

``` text
1. Install runtime
2. Install OpenClaw
3. Initialize configuration
4. Configure model provider
5. Configure channels
6. Configure tools
7. Configure skills
8. Test low-risk task
9. Apply sandbox/permission controls
10. Test multi-agent workflow
```

Do not immediately give a new agent unrestricted filesystem, shell,
email, cloud, GitHub-write, or production access.
