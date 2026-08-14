# Multica Installation & Runtime Configuration Guide

This guide provides step-by-step instructions for installing and configuring the **Multica Engine** across Desktop GUI environments and Docker container instances.

---

## 💻 1. Desktop Setup

### System Requirements
- **macOS**: Apple Silicon (M1/M2/M3/M4) or Intel, macOS 13.0+
- **Memory**: Minimum 16 GB RAM (32 GB recommended for local vector processing)
- **Disk Space**: 10 GB free space

### Desktop Installation Steps

1. **Download & Install Package**:
   - Download the latest `Multica-Desktop-macOS.dmg` from the official repository releases.
   - Drag `Multica.app` into `/Applications`.

2. **CLI Initialization**:
   Open terminal and link the binary:
   ```bash
   sudo ln -s /Applications/Multica.app/Contents/Resources/multica /usr/local/bin/multica
   multica --version
   ```

3. **Desktop Initial Launch**:
   - Launch Multica from Applications.
   - Navigate to **Preferences -> Engine Settings**.
   - Input system credentials and set default workspace directory to `~/MulticaWorkspaces`.

---

## 🐳 2. Docker Containerized Setup

For headless server deployments or team sandbox environments, deploy Multica via Docker.

### `docker-compose.yml`
```yaml
version: '3.8'

services:
  multica-engine:
    image: multica/engine:latest
    container_name: multica-engine-daemon
    restart: unless-stopped
    ports:
      - "8080:8080"
      - "9090:9090"
    environment:
      - MULTICA_ENV=production
      - MULTICA_PORT=8080
      - OMNIROUTE_ENABLED=true
      - DATABASE_URL=sqlite:///var/lib/multica/multica.db
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    volumes:
      - multica_data:/var/lib/multica
      - multica_config:/etc/multica
      - ./workspaces:/var/multica/workspaces
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 10s
      timeout: 5s
      retries: 3

volumes:
  multica_data:
  multica_config:
```

### Docker Deployment Command
```bash
# Export API Keys
export OPENAI_API_KEY="sk-proj-YOUR_KEY"
export ANTHROPIC_API_KEY="sk-ant-YOUR_KEY"

# Spin up containers
docker compose up -d

# Verify logs
docker compose logs -f multica-engine
```

---

## ⚙ 3. Runtime Configuration (`multica.runtime.yaml`)

The Multica runtime daemon is configured via `multica.runtime.yaml`:

```yaml
runtime:
  id: multica-daemon-node-01
  cluster: production-us-west
  listenAddress: 0.0.0.0
  port: 8080

executor:
  type: sandboxed
  timeoutSeconds: 300
  maxConcurrentAgents: 10
  memoryLimitMb: 4096

security:
  enableAuth: true
  jwtSecret: "SUPER_SECRET_HMAC_KEY_2026"
  allowedIPs:
    - 127.0.0.1
    - 10.0.0.0/8

omniroute:
  strategy: cost-optimized
  defaultProvider: openai
  fallbackProvider: anthropic
```

---

## 🔍 4. Verification & Diagnostics

Run validation checks against the running daemon:

```bash
# Check daemon health endpoint
curl -X GET http://localhost:8080/api/v1/health

# Run runtime diagnostic tool
multica status --verbose
```

### Expected Output
```
[MULTICA ENGINE DIAGNOSTICS]
Daemon Status:   RUNNING (PID 48219)
Listen Port:     8080
Docker Driver:   ACTIVE
OmniRoute:       ENABLED (2 Providers Ready)
Workspaces:      1 Active Workspace Loaded
Health Check:    PASSED (HTTP 200 OK)
```
