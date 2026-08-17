# Exploring MCP directories — mcpservers.org and mcpmarket.com

**Manish Prakash · Team Mohit · 6 August 2026**

Task 2 for the day: *try mcpservers.org and mcpmarket.com/submit.*

---

## 1. What these sites are

Because MCP standardises the protocol but not distribution, a set of community
directories has grown up to answer "which servers exist and how do I install them?"
They are to MCP roughly what npm's registry page is to Node packages — a catalogue,
not the runtime.

| Site | What it is | Notes |
|---|---|---|
| **mcpservers.org** | Open, community-curated index of MCP servers | Browse by category, links to each server's repo. Mostly a discovery front-end over GitHub. |
| **mcpmarket.com** | Marketplace-style directory with a submission flow | `/submit` is the form for listing your own server. |
| **modelcontextprotocol/servers** (GitHub) | The **official** reference + community list | The authoritative starting point; the directories largely mirror it. |

**Practical takeaway:** treat the directories as discovery, and the official GitHub
org as the trust anchor. A listing on a directory is not a security review.

---

## 2. Categories that show up repeatedly

Browsing the catalogues, the useful servers cluster into a handful of groups:

- **Filesystem / local** — read and write files in a sandboxed directory. Usually
  the first server anyone installs.
- **Version control** — GitHub / GitLab: issues, PRs, code search.
- **Databases** — Postgres, SQLite, MySQL. Read-only modes are common and wise.
- **Search & fetch** — web search, page fetching, documentation lookup.
- **Communication** — Slack, Discord, email.
- **Knowledge / memory** — vector stores and persistent-memory servers. Directly
  relevant to the 5 August advanced task of exposing AnythingLLM's RAG as MCP.
- **Browser automation** — Puppeteer/Playwright control.
- **Cloud & infra** — AWS, Kubernetes, Docker.

---

## 3. What a server listing needs to be useful

Reading a lot of these back to back, the ones worth installing all provide:

1. **Clear tool descriptions** — written for a model, not a human. This is the
   single biggest quality differentiator; see §3.3 of [`api_vs_mcp.md`](api_vs_mcp.md).
2. **Explicit transport** — stdio (local subprocess) or HTTP+SSE (remote).
3. **Copy-pasteable config** — the JSON block for the client's config file.
4. **Stated scope and permissions** — what it can read, what it can write.
5. **An auth story** — env vars for local, OAuth for remote.

A server that lists only "10 tools" and no descriptions is a red flag: the model
will not know when to call them.

---

## 4. Typical install shape

Local servers are almost always a subprocess launched by the client. The config
pattern is consistent across clients:

```jsonc
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/home/manish/sandbox"]
    },
    "weather-bhubaneswar": {
      "command": "python3",
      "args": ["/path/to/weather_mcp_server.py"]
    }
  }
}
```

Two things worth noticing:

- The **path argument is the sandbox boundary** for the filesystem server. Point it
  at a scratch directory, never at `/` or `$HOME`. This is the practical link to
  the "sandbox / VM" item on the master task list.
- `npx -y` downloads and executes code from the network on every launch. Convenient
  for a demo, not something to do casually on a machine with credentials on it.

For Claude Code specifically the same thing is done with `claude mcp add`, which
writes this config for you.

---

## 5. Submitting a server (mcpmarket.com/submit)

The submission flow wants, in substance:

| Field | What to supply |
|---|---|
| Name | Short, descriptive (`bhubaneswar-weather`) |
| Repository URL | Public source. Nobody should install a closed-source MCP server. |
| Description | One line on what it does |
| Category | From their taxonomy |
| Tools exposed | Names + one-line purpose each |
| Installation | The config block above |
| Auth requirements | Keys/env vars needed, or "none" |

Everything a submission asks for is content that should already be in the server's
README. If the README is good, submission is copy-paste — which is a decent
argument for writing the README first.

The weather predictor in this folder is the natural candidate to wrap and submit:
it needs no API key, so it has no credential story to get wrong.

---

## 6. Security notes — read before installing anything

Directories lower the friction of installing third-party code that runs **on your
machine, with your tokens, inside your model's trust boundary.** That deserves care.

- **An MCP server is arbitrary code.** A stdio server is a process you launch with
  your user's privileges. Read the source, or don't run it.
- **Prompt injection is a live risk class.** Content a server returns enters the
  model's context. A malicious or compromised server can attempt to steer the agent.
- **Tool-description poisoning.** Descriptions are model-facing instructions by
  design — which means a hostile description is an instruction-injection vector.
- **Confused-deputy / cross-server risk.** With several servers connected, one
  server's output can influence a call to another. Connect the minimum set.
- **Pin versions.** `npx -y` fetching latest on every launch means today's audit
  does not cover tomorrow's run.
- **Scope credentials down.** Read-only DB users, fine-grained GitHub tokens,
  narrow filesystem roots.

This connects directly to the **Skill Spector** item on the master task list —
auditing downloaded skills/servers for vulnerabilities is the same discipline
applied to a different artifact.

---

## 7. Conclusions

1. The directories solve **discovery**, and discovery was a genuine gap — the
   protocol says nothing about how you find a server.
2. Quality varies widely. Description quality is the best proxy for whether a
   server will actually work well with a model.
3. The ecosystem's convenience is also its risk: one config line to grant an agent
   real capability on your machine. Audit before installing.
4. Publishing is cheap, which is good for the ecosystem and a reason to treat
   listings as advertisements rather than endorsements.

---

## References

- <https://mcpservers.org>
- <https://mcpmarket.com> and <https://mcpmarket.com/submit>
- Official server list: <https://github.com/modelcontextprotocol/servers>
- Protocol docs: <https://modelcontextprotocol.io>
