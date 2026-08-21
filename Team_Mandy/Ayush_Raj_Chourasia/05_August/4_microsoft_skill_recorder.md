# Microsoft Skill Recorder

The **Microsoft Skill Recorder** (`https://github.com/microsoft/skill-recorder`) is a revolutionary tool for teaching agents new tasks without writing manual code.

## How It Works
1. You run the recorder on your machine.
2. You manually perform a task (e.g., navigating to a web portal, downloading a CSV, and running a python script on it).
3. The recorder captures the DOM elements, clicks, keystrokes, and terminal commands.
4. It compiles this sequence into an AI-readable "Skill" file (often JSON or Python automation code).
5. You upload this Skill to an agent in Multica.

## Why This Matters
Instead of spending hours writing brittle Selenium or Playwright scripts, you simply *show* the agent what to do once, and the skill recorder translates human action into agentic code. This drastically accelerates the onboarding of non-technical workflows into the AI ecosystem.
