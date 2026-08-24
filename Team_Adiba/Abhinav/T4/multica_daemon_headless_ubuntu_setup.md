# Multica Daemon Setup on a Headless Ubuntu Server

## Overview

This guide documents a Multica daemon setup where:

- The **Multica GUI is used from macOS** to obtain the daemon setup instructions.
- The **Multica daemon itself runs inside a Docker container** on a headless Ubuntu server.
- Multica provides commands that must be executed **inside the Bash terminal of the daemon container** to install/configure the daemon.
- API credentials are supplied through a `.env` file.
- **OpenCode is currently used as the primary LLM provider**.
- NVIDIA NIM, OpenRouter, and Gemini credentials are also made available for services/models that require them.

The important distinction is that the Docker container is the runtime environment, while the Multica-provided installation commands are executed **inside that already-running container**.

---

## 1. Architecture

The resulting setup looks approximately like this:

```text
┌──────────────────────────────┐
│            macOS             │
│                              │
│        Multica GUI           │
│                              │
│  • Generate daemon setup     │
│  • Configure/connect daemon  │
└──────────────┬───────────────┘
               │
               │ SSH / network
               ▼
┌──────────────────────────────┐
│      Headless Ubuntu         │
│                              │
│  ┌────────────────────────┐  │
│  │         Docker         │  │
│  │                        │  │
│  │  ┌──────────────────┐  │  │
│  │  │ Multica Daemon   │  │  │
│  │  │ Container        │  │  │
│  │  │                  │  │  │
│  │  │ Bash terminal    │  │  │
│  │  │      │           │  │  │
│  │  │      ▼           │  │  │
│  │  │ Multica-provided │  │  │
│  │  │ install commands │  │  │
│  │  └──────────────────┘  │  │
│  │                        │  │
│  │  └── .env / secrets    │  │
│  └────────────────────────┘  │
└──────────────────────────────┘
               │
               ▼
       ┌─────────────────┐
       │     OpenCode    │
       │ Primary LLM     │
       │    Provider     │
       └─────────────────┘
               │
       ┌───────┼────────┐
       ▼       ▼        ▼
    NVIDIA  OpenRouter Gemini
      NIM
```

---

# 2. Prerequisites

You need:

- A Mac with the **Multica GUI** installed.
- A headless Ubuntu server accessible through SSH.
- Docker installed on the Ubuntu server.
- Access to the Multica GUI's daemon installation workflow.
- API credentials for the services you want the daemon/agents to use.
- OpenCode configured as the primary LLM provider.

Verify Docker on Ubuntu:

```bash
docker --version
```

If Docker Compose is part of the Multica-provided setup, also verify:

```bash
docker compose version
```

---

# 3. Prepare the Ubuntu Server

Connect to the server from macOS:

```bash
ssh <ubuntu-user>@<server-ip>
```

Create a working directory:

```bash
mkdir -p ~/multica-daemon
cd ~/multica-daemon
```

The exact directory is not important; keeping the deployment in a dedicated directory simply makes it easier to manage.

---

# 4. Use the Multica GUI to Obtain the Daemon Commands

On the Mac:

1. Open the Multica GUI.
2. Go to the daemon/server setup workflow.
3. Follow the installation instructions shown by Multica.
4. Select the Docker/container deployment method if prompted.
5. Copy the commands/configuration supplied by Multica.

These commands are the **authoritative installation instructions** for the particular Multica version being used.

Do not replace Multica's commands with generic Docker commands from this guide.

---

# 5. Start the Multica Daemon Container

Use the Docker command or Docker Compose configuration provided by Multica.

For example, Multica may provide a command conceptually similar to:

```bash
docker run ...
```

or a Compose deployment such as:

```bash
docker compose up -d
```

The exact command, image, ports, volumes, and arguments should come from the Multica GUI.

After starting the container:

```bash
docker ps
```

Identify the Multica daemon container.

For example:

```text
CONTAINER ID   IMAGE              NAMES
xxxxxxxxxxxx   <multica-image>   multica-daemon
```

The actual container name will depend on the Multica configuration.

---

# 6. Enter the Multica Daemon Container

This is the key part of the setup.

The Multica installation commands are intended to be run **inside the daemon container's Bash environment**.

From the Ubuntu host:

```bash
docker exec -it <container-name> bash
```

For example:

```bash
docker exec -it multica-daemon bash
```

You should now be inside the container.

Your shell prompt will change to something resembling:

```text
root@<container-id>:/#
```

At this point, commands are being executed inside the Multica daemon container rather than directly on the Ubuntu host.

---

# 7. Run the Multica Installation Commands

Inside the container's Bash terminal, run the commands provided by the Multica GUI.

The workflow is:

```text
Multica GUI
     │
     │ installation commands
     ▼
macOS
     │
     │ copy commands
     ▼
Ubuntu SSH terminal
     │
     │ docker exec
     ▼
Multica daemon container
     │
     │ run Multica commands HERE
     ▼
Multica daemon installation/configuration
```

For example, if Multica provides commands such as:

```bash
<command-provided-by-multica>
```

execute them from the container shell.

**Do not substitute the placeholder above with guessed commands.**

The actual commands may change between Multica releases, so the GUI-generated instructions should always take precedence.

---

# 8. Why the Commands Must Be Run Inside the Container

There are two different environments:

### Ubuntu host

```text
Ubuntu
├── Docker
├── SSH
└── Multica daemon container
```

### Inside the container

```text
Multica daemon container
├── daemon runtime
├── Multica dependencies
├── agent configuration
├── MCP/tool configuration
└── Multica installation
```

Running a Multica installation command on the Ubuntu host when it was intended for the container can result in:

- dependencies being installed in the wrong environment,
- files being created outside the daemon runtime,
- missing packages inside the container,
- configuration being unavailable to the daemon.

Therefore, always check which shell you are currently in before running the Multica commands.

---

# 9. Configure the `.env`

The daemon requires credentials for the external services used by the agents and model providers.

A `.env` file can contain the required credentials, for example:

```env
# Primary LLM / OpenCode
OPENCODE_API_KEY=<your-opencode-credential>

# NVIDIA NIM
NVIDIA_NIM_API_KEY=<your-nvidia-nim-key>

# OpenRouter
OPENROUTER_API_KEY=<your-openrouter-key>

# Google Gemini
GEMINI_API_KEY=<your-gemini-key>
```

These names are **illustrative**.

Use the exact variable names required by:

- Multica,
- OpenCode,
- the relevant MCP servers,
- and the relevant agent configurations.

If Multica's documentation or GUI specifies different names, use those names.

---

# 10. Where the `.env` Lives

The important requirement is that the variables must be available to the process that actually needs them.

Depending on how the Multica Docker setup is generated, this can mean:

```text
Ubuntu host
└── .env
     │
     │ Docker environment injection
     ▼
Multica daemon container
└── environment variables
```

or the `.env` may be created/configured directly inside the container if the Multica setup specifically requires that.

Follow the environment-file location specified by the Multica Docker configuration.

Do not assume that a `.env` on the Ubuntu host automatically becomes available inside the container.

---

# 11. Verify Environment Variables

Inside the container, verify that the required variables are available.

For example:

```bash
test -n "$OPENROUTER_API_KEY" && echo "OpenRouter key loaded"
```

For NVIDIA NIM:

```bash
test -n "$NVIDIA_NIM_API_KEY" && echo "NVIDIA NIM key loaded"
```

For Gemini:

```bash
test -n "$GEMINI_API_KEY" && echo "Gemini key loaded"
```

For OpenCode:

```bash
test -n "$OPENCODE_API_KEY" && echo "OpenCode credential loaded"
```

These checks intentionally avoid printing the actual secret.

---

# 12. OpenCode as the Primary LLM Provider

This setup currently uses **OpenCode as the primary LLM provider**.

The architecture should therefore be understood as:

```text
Multica Agent
      │
      ▼
Multica Daemon
      │
      ▼
    OpenCode
      │
      ▼
Selected LLM / model
```

NVIDIA NIM, OpenRouter, and Gemini credentials being present does **not** automatically make them the primary provider.

Provider selection is determined by the OpenCode/Multica configuration.

Before testing an agent, verify:

- OpenCode is configured correctly.
- The intended OpenCode model is selected.
- The daemon can access OpenCode.
- The required OpenCode credentials are available.
- Agent configuration does not override the intended provider.

---

# 13. MCP Servers and Tools

If an agent requires an MCP server, the relevant MCP server configuration must also be available to the Multica daemon environment.

Conceptually:

```text
Multica Agent
     │
     ├── LLM → OpenCode
     │
     └── Tools
          │
          └── MCP Server
               │
               └── External API / service
```

The MCP server may require its own credentials in `.env`.

For example:

```env
<YOUR_MCP_API_KEY>=<secret>
```

Again, use the exact environment variable name expected by the MCP server.

Never put API keys directly into:

- `skill.md`,
- agent prompts,
- Git repositories,
- public configuration files,
- screenshots,
- documentation intended for publication.

---

# 14. Verify the Multica Daemon

Exit the container:

```bash
exit
```

From the Ubuntu host:

```bash
docker ps
```

Confirm that the Multica container is still running.

Check logs:

```bash
docker logs <container-name>
```

If Docker Compose is being used:

```bash
docker compose logs --tail=100
```

Follow logs live:

```bash
docker logs -f <container-name>
```

or:

```bash
docker compose logs -f
```

Look for successful daemon initialization and the absence of authentication/configuration errors.

---

# 15. Re-enter the Container When Needed

Whenever you need to perform maintenance or inspect the Multica installation:

```bash
docker exec -it <container-name> bash
```

Then:

```bash
cd <relevant-directory>
```

The exact directory depends on where the Multica installation commands place the daemon files.

---

# 16. Important Docker Consideration

Changes made **inside a running container** may disappear if the container is destroyed and recreated unless the relevant files are stored in a Docker volume or mounted from the host.

For example:

```text
Container filesystem
       │
       ├── temporary container data
       │
       └── may disappear after recreation
```

versus:

```text
Host directory / Docker volume
       │
       ▼
Persistent storage
       │
       ▼
Container
```

Therefore, if Multica's official setup specifies volumes or bind mounts, keep those exactly as provided.

Do not remove/recreate the container casually after completing the installation without understanding where Multica stores its persistent state.

---

# 17. Updating the Daemon

When Multica releases an updated daemon/setup:

1. Check the current installation instructions in the Multica GUI.
2. Back up important configuration.
3. Follow the new Docker/container instructions.
4. Enter the daemon container:

```bash
docker exec -it <container-name> bash
```

5. Run the updated Multica-provided commands inside the container.
6. Verify the daemon.
7. Test the agents and MCP servers.

Avoid assuming that an old installation command remains valid for a newer daemon version.

---

# 18. Troubleshooting

## Container is not running

On the Ubuntu host:

```bash
docker ps -a
```

Then inspect:

```bash
docker logs <container-name>
```

---

## Multica command says a dependency is missing

First confirm that you are inside the container:

```bash
hostname
```

and:

```bash
cat /etc/os-release
```

Then run the command supplied by Multica again from the container shell.

Do not immediately install random packages on the Ubuntu host.

---

## Environment variable is missing

Inside the container:

```bash
test -n "$VARIABLE_NAME" && echo "loaded"
```

If it is missing, verify how the Docker configuration passes the `.env` file into the container.

---

## OpenCode is not being used

Check:

1. OpenCode configuration.
2. Selected OpenCode model/provider.
3. OpenCode credentials.
4. Multica agent configuration.
5. Whether the agent has its own provider/model override.

Having NVIDIA NIM, OpenRouter, or Gemini keys in `.env` does not by itself determine which LLM is selected.

---

## MCP server is not being used

Check:

1. MCP server configuration.
2. MCP server command.
3. Required environment variables.
4. Whether the MCP server is available from the daemon container.
5. Whether the agent's `skill.md`/configuration instructs the agent to use the appropriate tool.
6. Daemon logs for MCP initialization errors.

---

# 19. Security

Never commit secrets.

Your repository should contain something like:

```text
.gitignore
.env
```

with:

```text
.env
```

inside `.gitignore`.

On Linux:

```bash
chmod 600 .env
```

Do not publish:

```text
API keys
access tokens
private credentials
.env files
SSH keys
```

Also avoid putting credentials directly into `skill.md` files.

---

# 20. Complete Setup Workflow

The entire process can be summarized as:

```text
STEP 1
Open Multica GUI on macOS
        │
        ▼
STEP 2
Use Multica's daemon setup workflow
        │
        ▼
STEP 3
Obtain Multica's Docker/container commands
        │
        ▼
STEP 4
SSH into headless Ubuntu
        │
        ▼
STEP 5
Run the Multica-provided Docker commands
        │
        ▼
STEP 6
Confirm the daemon container is running
        │
        ▼
STEP 7
Enter the container
        │
        │ docker exec -it <container> bash
        ▼
STEP 8
Run the Multica-provided installation commands
INSIDE THE CONTAINER
        │
        ▼
STEP 9
Configure required environment variables
        │
        ├── OpenCode
        ├── NVIDIA NIM
        ├── OpenRouter
        └── Gemini
        │
        ▼
STEP 10
Configure OpenCode as the primary LLM provider
        │
        ▼
STEP 11
Configure required MCP servers/tools
        │
        ▼
STEP 12
Restart/reload the daemon if required
        │
        ▼
STEP 13
Verify logs and connectivity
        │
        ▼
STEP 14
Connect/test through Multica GUI
```

---

# 21. Final Checklist

- [ ] Multica GUI is installed on macOS.
- [ ] Headless Ubuntu server is reachable over SSH.
- [ ] Docker is installed on Ubuntu.
- [ ] Multica-provided Docker/container setup has been executed.
- [ ] Multica daemon container is running.
- [ ] A Bash shell has been opened inside the daemon container.
- [ ] Multica-provided installation commands have been executed **inside the container**.
- [ ] Required `.env` configuration is available to the daemon.
- [ ] OpenCode is configured as the primary LLM provider.
- [ ] The intended OpenCode model is selected.
- [ ] NVIDIA NIM credentials are configured where required.
- [ ] OpenRouter credentials are configured where required.
- [ ] Gemini credentials are configured where required.
- [ ] Required MCP servers are configured.
- [ ] MCP credentials are available to the relevant processes.
- [ ] No credentials are stored in Git.
- [ ] Daemon logs show successful initialization.
- [ ] Multica GUI can communicate with the daemon.
- [ ] A test agent successfully executes through the daemon.
