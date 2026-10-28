# 💡 Agentic AI Tips & Short Hacks That Save Hours

> **Author:** Mohit Kumar — Team Mohit Lead  
> **Topic:** Practical battle-tested tricks to eliminate freezes, streamline CLI tools, and build bulletproof agent pipelines.

---

## ⚡ Hack 1: Bypassing the Interactive "Planning Freeze"

### The Issue:
Most modern coding assistants (Antigravity, Cursor, Claude Code) pause constantly to ask:
> *"I have planned 5 steps. Would you like me to proceed with Step 1?"*  
This halts unattended automation completely.

### The Fix:
Add an explicit override rule in your workspace's `GEMINI.md`, `AGENTS.md`, or custom instructions:
```markdown
### Autonomous Execution Rule
- When triggered by an inbox file or user command, bypass manual confirmation dialogs.
- Do NOT pause to ask "Can I proceed?".
- Proactively write code, run builds, fix diagnostics, and commit changes.
- Provide a clear post-execution summary only after the task is working.
```

---

## ⚡ Hack 2: Eliminating Browser OAuth Freezes in Headless CLIs

### The Issue:
Running commands like `vercel`, `supabase login`, or `gh auth login` in an agent's terminal hangs indefinitely because the CLI attempts to launch an interactive desktop browser.

### The Fix:
Always pass non-interactive flags and pre-configured programmatic access tokens:

```bash
# ❌ BAD (hangs forever waiting for browser click):
npx vercel --prod

# ✅ GOOD (autonomous, zero popups, instant):
npx vercel --prod --token $VERCEL_TOKEN --yes

# ✅ GOOD (for npm/npx installations):
npx -y create-next-app@latest ./ --non-interactive

# ✅ GOOD (for git operations):
git -c core.longpaths=true commit -m "feat: auto update"
```

---

## ⚡ Hack 3: The Asynchronous File-Queue Pattern (`inbox.md` & `outbox.md`)

### The Issue:
Synchronous HTTP calls between agents fail when tasks take more than 60–90 seconds (resulting in timeout errors: `openclaw returned no parseable output / Failed after 1m 35s`).

### The Fix:
Decouple inter-agent communication using local files:
1. **Producer Agent** writes the payload to `antigravity_inbox.md`.
2. **Consumer Agent** monitors the file, processes the task locally, and writes completion logs to `antigravity_outbox.md`.
3. Consumer sends a lightweight 1-line MCP ping: `notify_multica("Task completed")`.

*Benefits:* If either agent restarts or networks glitch, the task state is never lost.

---

## ⚡ Hack 4: Docker Socket Passthrough for Dev Containers

### The Issue:
When your agent runs inside an isolated Docker container (e.g. `kali-multica-bridge`), it cannot control host containers or inspect other microservices.

### The Fix:
Pass the host Docker daemon socket into the container:
```yaml
version: '3.8'
services:
  agent-bridge:
    image: kali-multica-ready
    container_name: agent-bridge
    volumes:
      - .:/workspace
      - //var/run/docker.sock:/var/run/docker.sock  # Grants host Docker control
    stdin_open: true
    tty: true
```
Now your containerized agent can run `docker ps`, `docker logs`, and restart companion containers safely!

---

## ⚡ Hack 5: Enabling Long Paths on Windows Git

### The Issue:
Deeply nested Next.js or node_modules paths cause git clone or checkout to crash on Windows with:
`Filename too long / fatal: cannot create directory`.

### The Fix:
Run this once globally:
```powershell
git config --global core.longpaths true
```
Or per repository:
```powershell
git config core.longpaths true
```
