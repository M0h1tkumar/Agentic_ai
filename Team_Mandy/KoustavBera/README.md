# Hi, It's Koustav

Assignment and learning log for the Agentic AI program.

## Log

| Date | Topic / Assignment | Learnings |
| :--- | :--- | :--- |
| 2026-07-27 | Unsloth & GGUF Fine-Tuning Workflow | Learned to construct resource-efficient fine-tuning workflows. Understood how to extract Q&A datasets from raw documents using helper smart models, load pre-quantized 4-bit base models, train with Unsloth in the cloud (Google Colab), and convert/export the resulting model into GGUF format. Created a skeleton notebook `unsloth_workflow.ipynb`. |
| 2026-07-29 | OpenClaw | OpenClaw installation guide, OAuth vs API, OpenClaw vs VSCode. Created an ASCII Art skill file (`SKILL.md`) covering pyfiglet, cowsay, boxes, and image-to-ASCII tools. |
| 2026-07-30 | OpenClaw on Fedora | Documented clean OpenClaw installation on Fedora 44 using the local prefix installer (`install-cli.sh`) to avoid NodeSource conflicts. Covered PATH setup, Claude CLI integration, systemd gateway management, and compared OpenClaw vs Claude Code. |
| 2026-08-03 | OpenClaw Multi-Agent System | Built a 4-agent marketing team (Nova, Sage, Iris, Rex) in OpenClaw. Debugged `openclaw.json` bindings schema, enabled cross-agent `sessions_send` via `agentToAgent` config, bootstrapped sub-agent sessions, set up Telegram bot with security pairing, and handled small-model hallucination during delegation. |
| 2026-08-06 | MCP Servers | Built two custom MCP servers: a Bhubaneswar weather server (using Open-Meteo API, no key required) and an AnythingLLM RAG server. Configured both in `mcp-config.json` for use with Claude/OpenClaw. |
