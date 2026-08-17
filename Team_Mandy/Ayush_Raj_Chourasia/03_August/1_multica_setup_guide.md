# Multica Cloning & Installation Guide

Multica is a powerful daemon-based agent orchestration platform. This guide covers the process of cloning the repository and running the initialization scripts.

## 1. Repository Setup
First, we clone the master repository into our local workspace.
```bash
git clone https://github.com/multica-ai/multica.git
cd multica
```

## 2. Using the Provided Scripts
Multica ships with several shell scripts that handle the lifecycle of the daemon. It is highly recommended to use these rather than manually starting the Python processes.

1. **Update Local Repo:**
   ```bash
   ./Latest_Upgrade-multica.sh
   ```
   This script performs a `git pull`, checks for missing Python dependencies, and reinstalls them if the `requirements.txt` was updated.

2. **Start the Daemon:**
   ```bash
   ./start-multica.sh
   ```
   This boots up the backend and frontend components. It runs in the background.

3. **Authentication via OTP:**
   Currently, Multica uses an OTP generation script for login rather than standard email/password, as SMTP isn't fully integrated yet.
   ```bash
   ./get-otp.sh
   ```
   Copy the output code and paste it into the Multica login screen at `http://localhost:3000`.

## 3. Stopping the Daemon
When you are done testing, always shut down the service cleanly to prevent database locks.
```bash
./stop-multica.sh
```
