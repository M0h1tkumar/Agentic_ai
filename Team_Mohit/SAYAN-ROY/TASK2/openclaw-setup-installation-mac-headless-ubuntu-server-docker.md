# OpenClaw Setup and Installation inside a Mac using a Headless Ubuntu Server and Docker Containerization
**Date:** 2026-08-02

---

# Objective
Provide a concise, actionable installation guide for OpenClaw from a Mac targeting a headless Ubuntu server with Docker containerization, including SSH-based terminal and VS Code connection.

---

# Summary

- **Use SSH from macOS** to access the headless Ubuntu server and prepare Docker prerequisites.
- **Install Docker Engine and Docker Compose** on Ubuntu to host OpenClaw in containers.
- **Run OpenClaw from a Docker Compose stack** with mounted configuration and persistent storage.
- **Connect VS Code remotely** via SSH to edit files and manage containers from the Mac.
- **Secure the environment** by using SSH keys, firewall rules, and Docker user namespaces where possible.

---

# OpenClaw installation flow

OpenClaw installation on a headless Ubuntu server uses Docker to isolate dependencies and simplify deployment. The Mac is used only as the management workstation.

| Step | Description |
|---|---|
| 1 | Configure SSH access from Mac to Ubuntu server |
| 2 | Install Docker Engine and Docker Compose on Ubuntu |
| 3 | Clone OpenClaw repository or obtain Docker manifest |
| 4 | Create Docker Compose stack with required volumes and ports |
| 5 | Start and verify containers | 

---

# Prerequisites

- macOS with Terminal and VS Code installed.
- Headless Ubuntu server reachable via SSH.
- User account on Ubuntu with sudo privileges.
- OpenClaw repository access or Docker image references.

---

# Server preparation and Docker installation

1. Connect to Ubuntu server from macOS:

```bash
ssh user@ubuntu-server.example.com
```

2. Update package metadata and install Docker prerequisites:

```bash
sudo apt update && sudo apt install -y ca-certificates curl gnupg lsb-release
```

3. Add Docker’s official GPG key and repository:

```bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmour -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
```

4. Install Docker Engine and Compose:

```bash
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

5. Add the user to the docker group to run Docker without sudo:

```bash
sudo usermod -aG docker $USER
newgrp docker
```

6. Verify Docker installation:

```bash
docker version
docker compose version
```

---

# OpenClaw Docker deployment

1. On the Ubuntu server, clone or prepare the OpenClaw deployment files:

```bash
git clone https://github.com/openclaw/openclaw.git /opt/openclaw
cd /opt/openclaw
```

2. Create or validate a `docker-compose.yml` file with service definitions, volumes, and ports:

```yaml
version: '3.8'
services:
  openclaw:
    image: openclaw/openclaw:latest
    restart: unless-stopped
    ports:
      - "8080:8080"
    volumes:
      - ./config:/app/config
      - ./data:/app/data
    environment:
      - OPENCLAW_ENV=production
```

3. Start the stack:

```bash
docker compose up -d
```

4. Check container status and logs:

```bash
docker compose ps
docker compose logs -f
```

5. Confirm OpenClaw is reachable on the mapped port from the Mac:

```bash
curl http://ubuntu-server.example.com:8080/health
```

---

# SSH connection from Terminal and VS Code

## SSH terminal connection

1. Generate or reuse an SSH key on macOS:

```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_openclaw
ssh-copy-id -i ~/.ssh/id_ed25519_openclaw.pub user@ubuntu-server.example.com
```

2. Connect using the private key:

```bash
ssh -i ~/.ssh/id_ed25519_openclaw user@ubuntu-server.example.com
```

3. Optionally add a host entry in `~/.ssh/config`:

```text
Host openclaw-server
  HostName ubuntu-server.example.com
  User user
  IdentityFile ~/.ssh/id_ed25519_openclaw
  ServerAliveInterval 60
```

4. Then connect with:

```bash
ssh openclaw-server
```

## VS Code remote SSH connection

1. Install the VS Code `Remote - SSH` extension.
2. Open the Command Palette and select `Remote-SSH: Add New SSH Host...`.
3. Enter the same config host alias or direct SSH command.
4. Open the remote folder `/opt/openclaw` or your project directory.
5. Use VS Code terminal to run Docker Compose commands and edit files directly on the server.

---

# Security and maintenance notes

- **Use SSH keys** instead of passwords to harden access.
- **Enforce firewall rules** on Ubuntu to restrict ports to known addresses.
- **Rotate Docker credentials and keys** periodically.
- **Monitor container logs** and restart failed services using Docker Compose restart policies.
- **Back up persistent volumes** for `config` and `data` directories before upgrades.

---

# Recommendation

For Mac-based management of OpenClaw on a headless Ubuntu server, use SSH plus Docker Compose as the deployment model. This isolates OpenClaw in containers, keeps the host lean, and enables a secure, remote VS Code development workflow.

---

# Next Steps

- Validate the OpenClaw service endpoint from the Mac after deployment.
- Add CI/CD or script automation for Docker Compose start/restart.
- Harden the Ubuntu server with SSH key restrictions and a minimal open port set.