# 3 — Connecting Multica to Slack

**Manish Prakash · Team Mohit · 5 August 2026**

---

## What the integration buys you

Slack becomes the **interface** to the agent system while Multica stays the
**system of record**:

- Issue created, assigned, completed, or failed → a message in the team channel.
- `@agent` mention in Slack → an issue in Multica, executed by the daemon.
- Agent output posted back into the thread that requested it.

The valuable direction is the second one. Notifications are nice; **creating work
from where the conversation already happens** is what changes behaviour. Nobody
opens a project management tool to file the thought they just had in a thread.

---

## Slack app setup

### 1. Create the app

<https://api.slack.com/apps> → **Create New App** → **From scratch** (or from a
manifest, which is more reproducible and worth preferring for a team).

### 2. Bot token scopes

**OAuth & Permissions → Bot Token Scopes:**

| Scope | Why |
|---|---|
| `chat:write` | Post messages |
| `app_mentions:read` | See `@agent` mentions |
| `channels:history` | Read thread context for a mention |
| `channels:read` | Resolve channel names to IDs |
| `users:read` | Map Slack users to Multica users |
| `files:write` | Upload longer outputs as snippets |

Request only what you use. Slack shows the scope list to whoever installs the app,
and a long list gets refused.

### 3. Install

**Install to Workspace** → approve → copy the **Bot User OAuth Token**
(`xoxb-...`). Also copy the **Signing Secret** from Basic Information.

Note what just happened: this is a real OAuth 2.0 authorization-code flow —
consent screen, scopes, revocable per-app. Exactly the model described in
[`../29_July_2026/oauth_vs_api_key.md`](../29_July_2026/oauth_vs_api_key.md). The
resulting `xoxb-` token, however, is then used as a **long-lived bearer token**, so
it needs API-key-grade handling: env var, never committed, rotated on exposure.

### 4. Receiving events — pick a transport

**Socket Mode** (recommended for self-hosted):
- Enable Socket Mode, generate an **App-Level Token** with `connections:write`.
- Slack connects outbound over a WebSocket. **No public URL needed**, which is the
  deciding advantage for a local Docker install — no ngrok, no reverse proxy, no
  inbound firewall hole.

**Events API** (HTTP):
- Requires a publicly reachable HTTPS endpoint that answers Slack's URL
  verification challenge within 3 seconds.
- Correct for a production deployment with a real domain; painful for localhost.

I used Socket Mode. For a stack that lives behind a laptop firewall it is the only
sane choice.

### 5. Subscribe to events

`app_mention`, and `message.channels` only if you genuinely need non-mention
messages — it is a much noisier and more privacy-sensitive subscription.

---

## Wiring it into Multica

```bash
SLACK_BOT_TOKEN=xoxb-...
SLACK_APP_TOKEN=xapp-...          # Socket Mode
SLACK_SIGNING_SECRET=...
SLACK_DEFAULT_CHANNEL=C0123456789
```

Then in the Multica workspace settings, connect the Slack integration and map:

| Slack event | Multica action |
|---|---|
| `@agent <task>` | Create issue, assign to that agent |
| Thread reply | Comment on the linked issue |
| — | Post status changes back to the originating thread |

**Always reply in-thread.** A channel where every agent update is a top-level
message becomes unusable within a day.

---

## Verifying

1. Invite the bot: `/invite @multica`.
2. Post `@multica hello` — expect an acknowledgement.
3. Post a real task — expect an issue in Multica.
4. Confirm the daemon picks it up and the result returns to the thread.

If step 2 works but step 3 does not, the Slack side is fine and the problem is
Multica or the daemon. That split is the fastest way to bisect the failure.

---

## Failure modes

| Symptom | Cause |
|---|---|
| Bot ignores mentions | Not invited to the channel, or `app_mentions:read` missing |
| `not_in_channel` on post | Same — invite the bot |
| Events API URL verification fails | Endpoint not publicly reachable, or slower than 3 s |
| Duplicate responses | Slack retries on timeout; ack immediately, process async |
| Mention creates issue, nothing runs | Daemon not running — see [`../03_August_2026/multica_setup.md`](../03_August_2026/multica_setup.md) |
| `invalid_auth` | Wrong token type — `xoxb` for API calls, `xapp` for Socket Mode |

The duplicate-response one is worth internalising: **Slack requires an
acknowledgement within 3 seconds, and agent work takes far longer than that.** Ack
first, then do the work asynchronously and post the result. Any integration that
does the work before acking will double-fire under load.

---

## Security

- **Restrict which channels the bot is in.** It reads message history in every
  channel it joins.
- **Map Slack users to Multica users** and check permissions before creating an
  issue — otherwise anyone in the workspace can trigger agent work on your key.
- **Treat Slack messages as untrusted input.** Same prompt-injection surface as any
  chat channel; a message is an instruction to whatever reads it.
- **Verify the signing secret** on HTTP transport so only Slack can post to you.
- **Rate-limit.** A busy channel plus an eager trigger rule is an expensive
  afternoon.

---

## Takeaway

The mechanics are straightforward; **Socket Mode is what makes it practical for a
self-hosted stack**, because it removes the public-URL requirement entirely.

The real design lesson is the 3-second ack: agent latency and chat-platform
expectations are fundamentally mismatched, and every integration in this space has
to reconcile them by acknowledging fast and answering later.
