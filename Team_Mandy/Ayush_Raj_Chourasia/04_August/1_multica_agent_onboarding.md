# Multica Agent Onboarding Process

This document outlines the end-to-end process of defining an agent within the Multica ecosystem and tightly integrating it with an Agent Runtime (OpenClaw) and an underlying LLM.

## Step 1: Agent Definition & System Prompt
The first step in Multica is giving the agent an identity. I created a **Research Analyst Agent**.
- **System Prompt:** *"You are an expert technical researcher. Your goal is to gather data, summarize findings, and present them in a structured markdown format. You do not hallucinate; if you do not know the answer, you use your web search tool."*

## Step 2: Runtime Integration
Multica is the orchestrator, but it needs a runtime to actually execute the agent's logic. 
- I bound this agent to **OpenClaw**. 
- In the Multica dashboard, under `Runtime Configurations`, I selected `OpenClaw` and linked the underlying LLM to `gpt-4o`. (Alternatively, OpenCode or Claude Desktop could be selected).

## Step 3: Skill Alignment
Skills enforce consistent behavior. 
- I created a skill called `Markdown_Formatter` which dictates exactly how headers, tables, and lists should be structured. 
- I uploaded this skill into the agent's memory bank within Multica.

## Step 4: Tool Provisioning
An agent without tools is just a chatbot.
- I assigned the `Web_Search` and `Database_Query` tools to the agent.
- Multica injects these into the OpenClaw environment, allowing the LLM to trigger them via function calling.

## Step 5: Access Control
Finally, security. I defined exactly which users (by email/ID) are allowed to invoke this specific agent in the Multica settings, preventing unauthorized API usage.
