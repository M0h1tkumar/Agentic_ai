# Driving an agent from a messaging app instead of the CLI

**Manish Prakash · Team Mohit · 30 July 2026** *(optional task)*

---

## Why bother

The CLI is fine for development and wrong for everything after it:

- **Availability.** A messaging bot works from a phone, on the move, without a
  terminal.
- **Persistence.** The gateway keeps running; the conversation survives your laptop
  closing.
- **Multi-user.** Colleagues can use the agent without shell access to your machine.
- **A real interface test.** The CLI hides bad UX. Anything confusing in a chat
  window is genuinely confusing.

There is also a less comfortable reason it is worth doing: **it forces you to
confront the security model.** A CLI agent is driven only by you. A bot is driven by
whoever can message it.

---

## Telegram — the shortest path

Telegram is the easiest of the options: no app review, no OAuth, one token.

### 1. Create the bot

Message **@BotFather** on Telegram:

```
/newbot
→ name:     Atlas Research Assistant
→ username: manish_atlas_bot
```

BotFather returns a token like `8123456789:AAH...`. **That token is a permanent
static credential with full control of the bot** — the exact pattern discussed in
[`../29_July_2026/oauth_vs_api_key.md`](../29_July_2026/oauth_vs_api_key.md). Never
commit it. `/revoke` in BotFather if it leaks.

Useful settings while you are there:

```
/setprivacy   → Enable    (bot only sees messages addressed to it, in groups)
/setcommands  → register a command list so users see what exists
/setdescription
```

### 2. Wire it into OpenClaw

```jsonc
{
  "channels": {
    "telegram": { "token": "8123456789:AAH..." }
  },
  "bindings": [
    { "agent": "atlas", "channel": "telegram" }
  ]
}
```

Both keys are **root-level**. Bind only the orchestrator — users should talk to one
front door, not to four agents.

### 3. Restart and test

```bash
openclaw gateway restart
journalctl --user -u openclaw -f     # where the real errors appear
```

Then message the bot. If nothing happens, the gateway log will say why; the chat
window never will.

---

## Discord — when you need structure

Better than Telegram when you want channels, roles, and threads.

1. Discord Developer Portal → New Application → Bot → copy token.
2. Enable the **Message Content Intent** under Privileged Gateway Intents. Without
   it the bot receives empty message bodies and appears silently broken — this is
   the single most common Discord bot mistake.
3. OAuth2 → URL Generator → scopes `bot` + `applications.commands`, permissions
   `Send Messages`, `Read Message History`. Use the generated URL to invite it.
4. Add the token under `channels.discord` and bind it.

Discord's advantage is real: threads give each task its own conversation, and role
permissions let you restrict who can invoke the agent — something Telegram handles
much less gracefully.

---

## Slack — for a workplace

Heaviest setup, best fit for a team. Covered as part of the
[5 August Multica–Slack task](../05_August_2026/03_multica_slack_integration.md),
since the mechanics are the same: an app manifest, bot scopes
(`chat:write`, `app_mentions:read`), Event Subscriptions or Socket Mode, and
installation to the workspace.

---

## Security — the part that actually matters

A bot turns your agent's input from "me, at a keyboard" into "anyone who finds the
bot." If that agent can run shell commands, that is a serious exposure.

1. **Allow-list users.** Restrict by Telegram user ID / Discord role. Do this first,
   before anything else. An open bot with `bash` access is a remote shell you
   published.
2. **Treat every message as untrusted input.** Prompt injection via chat is trivial
   — someone types instructions and the model reads them as instructions, because
   that is exactly what they are.
3. **Narrow the tool allow-list** on any channel-bound agent. A research bot does
   not need to write files outside its workspace.
4. **Run in a VM or container.** Same argument as everywhere else in these notes.
5. **Never log message contents** to a shared location — users will paste secrets
   into a chat with a bot, reliably.
6. **Rate-limit.** Both to control cost and to blunt abuse.

---

## What I took away

- Integration is genuinely easy — for Telegram it is one token and two config keys.
  The work is not the plumbing.
- **The interface change is a security change**, and that is the real content of
  this task. Going from CLI to bot converts a single-user tool into a networked
  service, and nothing about the config makes that transition obvious.
- Chat is a better interface than the CLI for agent work specifically because
  agents are slow. A conversation tolerates a 30-second reply; a blocking terminal
  prompt feels broken.
- Bind one agent, not the whole team. Users should never have to know the topology.
