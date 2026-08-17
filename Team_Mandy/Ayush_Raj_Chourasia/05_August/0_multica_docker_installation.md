# Compulsory Installation of Multica (Docker Method)

While Multica can be run via standard shell scripts and Python virtual environments, deploying it via **Docker** is the preferred and most stable method for production environments. Docker ensures that the Node.js frontend and Python backend environments are completely isolated and consistent across all team members' machines.

## Prerequisites
- Docker Desktop installed and running.
- Docker Compose installed.

## Installation Steps
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/multica-ai/multica.git
   cd multica
   ```

2. **Configure Environment Variables:**
   Copy the example environment file and configure the necessary keys (like OpenAI API keys or local LM Studio endpoints).
   ```bash
   cp .env.example .env
   ```

3. **Deploy via Docker Compose:**
   Run the following command to build the images and spin up the containers in detached mode:
   ```bash
   docker-compose up -d --build
   ```

4. **Verify Deployment:**
   - Check the running containers: `docker ps`
   - Access the Multica Dashboard at `http://localhost:3000`
   - The backend API will be running on `http://localhost:8000`

## Why Docker is Preferable
- **Dependency Isolation:** No conflicts with global Python packages.
- **Easy Updates:** Pulling the latest Multica version is as simple as `git pull` followed by `docker-compose up -d --build`.
- **Cross-Platform:** Works identically on Windows, Mac, and Linux without worrying about system-level libraries.
