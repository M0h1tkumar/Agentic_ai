# 3 August Tasks — Multica Installation & OmniRoute

> **Date:** 3 August 2026
> **Author:** Rohit Kumar

---

## Task 1: Cloning and Installation of Multica

### What is Multica?

**Multica** is a platform for building and coordinating multi-agent AI workflows. It allows different agents to work together, use tools, and handle specialized tasks as part of a larger workflow.

Key capabilities include:

* Multi-agent coordination
* Agent task assignment
* Task handoff between agents
* Workspace management
* Integration with external tools and services

---

## Cloning Multica

Clone the Multica repository provided by the project or training team:

```bash
git clone <MULTICA_REPOSITORY_URL>
cd <MULTICA_DIRECTORY>
```

The exact repository URL and installation instructions should be taken from the project's official documentation.

---

## Installation Options

### Method 1: Local Installation

If the Multica repository provides a Python-based installation, a virtual environment can be created:

```bash
python3 -m venv multica_env
```

Activate the environment.

### Linux/macOS

```bash
source multica_env/bin/activate
```

### Windows

```bash
multica_env\Scripts\activate
```

Install the dependencies provided by the project:

```bash
pip install -r requirements.txt
```

If the project supports editable installation:

```bash
pip install -e .
```

Verify the installation using the command documented by the project.

---

## Method 2: Docker Installation

Docker is useful for Multica because it isolates application dependencies and makes the environment easier to reproduce.

A typical Docker workflow is:

```bash
docker pull <MULTICA_IMAGE>
```

Run the container using the configuration specified by the project's documentation:

```bash
docker run -d \
  --name multica \
  -p 8080:8080 \
  -e OPENAI_API_KEY=YOUR_API_KEY \
  -v "$(pwd)/workspace:/app/workspace" \
  <MULTICA_IMAGE>
```

Check whether the container is running:

```bash
docker ps
```

View logs when troubleshooting:

```bash
docker logs multica
```

The exact image name, ports, environment variables, and startup commands depend on the Multica version being used.

---

## Docker Compose

For a multi-service setup, Docker Compose can be used.

Example structure:

```yaml
services:
  multica:
    image: <MULTICA_IMAGE>
    ports:
      - "8080:8080"
    environment:
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY}
    volumes:
      - ./workspace:/app/workspace
    restart: unless-stopped

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
```

Start the services:

```bash
docker compose up -d
```

Check the running services:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs -f multica
```

---

## Environment Variables

API keys should never be hardcoded in source code or committed to GitHub.

Example:

```env
OPENAI_API_KEY=your_api_key
ANTHROPIC_API_KEY=your_api_key
SLACK_BOT_TOKEN=your_token
```

A `.env` file or another secure secret-management mechanism can be used during local development.

---

## Initial Configuration

After installation, configure Multica according to the project's documentation.

A configuration may include:

```yaml
llm:
  provider: openai
  model: <MODEL_NAME>
  api_key: ${OPENAI_API_KEY}

workspace:
  name: "Team Rohit"

integrations:
  slack:
    enabled: false
```

The actual configuration keys depend on the Multica version being used.

---

## Verification

A successful installation should allow the following:

```text
Clone Repository
       ↓
Install Dependencies
       ↓
Configure Environment
       ↓
Start Multica
       ↓
Verify Services
       ↓
Create/Test Agent
```

Basic Docker verification:

```bash
docker ps
```

If the service starts successfully and the Multica interface or daemon is accessible, the installation is complete.

---

# Optional Task: Experiment with OmniRoute

## What is OmniRoute?

OmniRoute is an LLM routing concept in which requests can be directed to different models or providers based on factors such as:

* Task type
* Model capability
* Cost
* Latency
* Availability

The goal is to choose an appropriate model instead of sending every request to the same provider.

---

## Example Routing Strategy

A simple routing architecture can look like this:

```text
User Request
      |
      v
   Router
      |
      +---- Simple Task ----> Lower-cost Model
      |
      +---- Complex Task ---> More Capable Model
      |
      +---- Fast Task ------> Low-latency Model
```

---

## Possible Routing Criteria

| Strategy       | Goal                             |
| -------------- | -------------------------------- |
| Cost Optimized | Minimize inference cost          |
| Speed          | Minimize response latency        |
| Quality        | Prefer stronger models           |
| Balanced       | Combine cost, speed, and quality |

---

## Example

A routing system could use:

```text
Simple classification
        ↓
Small / low-cost model

Complex reasoning
        ↓
More capable model

Code generation
        ↓
Code-specialized model
```

---

## Benefits of Model Routing

* Better cost control
* Lower latency for simple tasks
* Ability to use multiple model providers
* Flexible model selection
* Better resource utilization

---

## Integration Concept with Multica

OmniRoute-style model routing can be placed between the agent runtime and the LLM provider:

```text
User
  |
  v
Multica Agent
  |
  v
LLM Router
  |
  +---- Provider A
  |
  +---- Provider B
  |
  +---- Provider C
```

The router decides which model should process the request.

The exact integration depends on whether the Multica version being used supports external model routing.

---

## Key Learnings

1. Multica should be installed using the official project instructions.
2. Docker can provide a reproducible and isolated deployment environment.
3. API keys should always be stored as environment variables or secrets.
4. Model routing can select different LLMs according to cost, speed, or capability.
5. OmniRoute was an optional experiment for understanding multi-provider LLM routing.
