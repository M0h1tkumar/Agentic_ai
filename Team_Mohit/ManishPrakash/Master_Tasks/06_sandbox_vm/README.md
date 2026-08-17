# Sandbox and VM isolation for agentic work

**Master task 6 (optional):** shift agentic AI work to a virtual machine for safety.

Listed as optional. It is the item every other document in this repository ends up
depending on, so it is treated here as a prerequisite rather than an extra.

---

## The argument, in one paragraph

Every tool in this program executes code. OpenClaw runs shell commands. OpenCode
edits files and runs builds. Multica's daemon spawns agent CLIs. MCP servers are
subprocesses launched with your privileges. Copilot agent mode runs terminal
commands. Each is bounded by what its process can reach — which, on a normal
developer laptop, is your SSH keys, your cloud credentials, your git remotes, your
browser session cookies, and your production kubeconfig.

**An agent's blast radius is its environment, not its intent.** You cannot make an
agent safe by prompting it carefully, because the failure modes that matter are not
about intent at all.

---

## What actually goes wrong

Four distinct failure modes, only one of which involves a malicious actor:

**1. Prompt injection.** An agent reads a file, a web page, an issue comment, a
dependency README, or a Telegram message. That text is instruction to the model.
Untrusted input plus real capability is the whole vulnerability class, and it is
structural — it does not get fixed by a better model.

**2. Mistakes.** A wrong path in a delete command. A `git push --force` to the wrong
branch. No malice, same result.

**3. Third-party code.** MCP servers and skills are code from strangers, one config
line away from running as you. This is what
[`../05_skill_spector/`](../05_skill_spector/) exists to triage, and static analysis
only catches what it recognises.

**4. Data exposure.** An agent sends its accessible environment to a provider, not
just your prompt. An agent that runs `cat .env` while debugging has transmitted your
secrets. Sandboxing is a **privacy** control as much as a security one.

---

## Isolation options

Ordered by strength, and the right choice depends on what you are defending against.

| Approach | Isolates | Effort | Escape difficulty |
|---|---|---|---|
| Separate user account | Files, some processes | Low | Low |
| Container (Docker/Podman) | Filesystem, network, processes | Low | Medium |
| Rootless container (Podman) | Same, without root daemon | Low | Medium-high |
| VM (KVM, VirtualBox, UTM) | **Full kernel boundary** | Medium | High |
| Dedicated hardware | Everything | High | Highest |
| Cloud dev box | Everything on your machine | Medium | High |

**A container is not a security boundary in the way a VM is.** Containers share the
host kernel; a kernel vulnerability crosses that line. For running your own agent on
your own code, a container is proportionate. For running code you have not read, a
VM is the honest answer.

---

## The practical setup

A VM as the agentic workspace, with the host kept clean.

**1. Provision.** 4 vCPU, 8–16 GB RAM, 60 GB disk. Ubuntu or Fedora. KVM/virt-manager
on Linux, UTM on Apple Silicon, VirtualBox anywhere.

**2. Snapshot immediately after setup.** Before installing a single agent tool. This
is the highest-value five minutes in the whole exercise: recovery from anything
becomes a rollback rather than a rebuild, which changes how freely you can
experiment.

**3. Credentials — the part that matters most.**

- **No SSH keys with access to anything real.** Generate a VM-only key, deploy it to
  the VM-only repositories, nothing else.
- **Scoped API keys with spend caps**, separate from your personal ones. When (not
  if) one leaks, rotation is a five-minute job.
- **No cloud CLI credentials.** No `~/.aws/credentials`, no `gcloud` login, no
  production kubeconfig.
- **Read-only database users only** — the point made in
  [`../01_anythingllm_setup/`](../01_anythingllm_setup/).

The test to apply: *if this VM were fully compromised right now, what would I have
to rotate?* Keep that list short enough to write down.

**4. Network.** NAT by default. Never bridge a VM running autonomous agents onto a
network with production hosts. If the agent only needs a model API, egress filtering
to that host is worth the effort.

**5. File sharing.** One narrow shared folder, mounted read-write, containing only
the project. Not your home directory. The convenience of `-v $HOME:/home` undoes
most of the isolation you just built.

**6. Nested containers inside the VM** for individual tools. Defence in depth, and
the composition is not redundant: the VM protects the host, the container limits
what a single misbehaving tool reaches.

---

## Container isolation for a single tool

When a full VM is disproportionate:

```bash
docker run -it --rm \
  --network none \
  --read-only \
  --tmpfs /tmp \
  --cap-drop ALL \
  --security-opt no-new-privileges \
  --memory 4g --cpus 2 \
  -v "$PWD/project:/work" \
  -w /work \
  python:3.12-slim
```

Each flag removes a specific capability: `--network none` prevents exfiltration
entirely, `--read-only` with a tmpfs limits persistence, `--cap-drop ALL` removes
privileged operations, and the memory and CPU limits bound a runaway loop.

**Two anti-patterns that undo all of it:**

- `-v /var/run/docker.sock:/var/run/docker.sock` — grants container-management
  rights, which is close to host root. Sometimes genuinely required (Open Hands
  needs it to spawn its own sandboxes); never incidental.
- `--privileged` — removes essentially every boundary. If a tool needs it, that is
  information about the tool.

---

## Fitting it to the rest of this repository

| Tool | Minimum |
|---|---|
| OpenClaw with a public channel binding | **VM.** Public input plus shell access |
| MCP servers from a directory | **VM** until the source has been read |
| OpenCode / terminal coding agents | Container, VM if the repo is untrusted |
| Multica + Postgres + daemon | Containers, already the deployment model |
| AnythingLLM | Container, on an internal network |
| Copilot agent mode | Container or VM; never blanket auto-approve |

---

## What isolation does not fix

Being honest about the limits, because a boundary you over-trust is worse than one
you understand:

- **Data you deliberately put inside.** The VM protects the host, not the documents
  you copied in.
- **Anything reachable from inside.** Credentials in the VM are credentials the
  agent has.
- **Provider transmission.** The model API sees whatever the agent sends. Isolation
  bounds what the agent can *read*; it does not encrypt what it chooses to send.
- **Your own approval.** Approving a destructive command inside a VM still runs it.
- **Kernel escapes**, for containers specifically.

---

## Summary

- **Blast radius is environment, not intent.** Careful prompting is not a security
  control.
- **Snapshot before you start.** It converts every incident into a rollback.
- **The credential inventory is the real work**, not the hypervisor choice. Ask what
  you would have to rotate if the VM were compromised, and shorten that list.
- **Containers bound a tool; VMs bound a kernel.** Match the boundary to whether you
  have read the code.
- **Sandboxing is a privacy control too** — an agent transmits its whole accessible
  environment, not just your prompt.
- The optional label on this task is misleading. Everything else in this program
  assumes it.
