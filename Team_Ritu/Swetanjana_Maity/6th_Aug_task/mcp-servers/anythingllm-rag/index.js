#!/usr/bin/env node
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const BASE_URL = (process.env.ANYTHINGLLM_BASE_URL || "http://localhost:3001").replace(/\/+$/, "");
const API_KEY = process.env.ANYTHINGLLM_API_KEY;

if (!API_KEY) {
  console.error("ANYTHINGLLM_API_KEY is not set. Generate one in AnythingLLM under Settings > API Keys.");
  process.exit(1);
}

async function allm(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    ...options,
    headers: {
      Authorization: `Bearer ${API_KEY}`,
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
  });
  if (!res.ok) {
    throw new Error(`AnythingLLM API ${path} failed: ${res.status} ${await res.text()}`);
  }
  return res.json();
}

const server = new McpServer({ name: "anythingllm-rag", version: "1.0.0" });

server.registerTool(
  "list_workspaces",
  {
    title: "List AnythingLLM workspaces",
    description: "List all workspaces (document collections) available in AnythingLLM, with their slugs.",
    inputSchema: {},
  },
  async () => {
    const data = await allm("/api/v1/workspaces");
    const summary = (data.workspaces || []).map((w) => ({ name: w.name, slug: w.slug, id: w.id }));
    return { content: [{ type: "text", text: JSON.stringify(summary, null, 2) }] };
  }
);

server.registerTool(
  "query_workspace",
  {
    title: "Query AnythingLLM RAG workspace",
    description:
      "Ask a question against a specific AnythingLLM workspace's embedded documents (RAG-only mode: answers are grounded in retrieved document chunks, not general chat memory). Use list_workspaces first to find the right slug.",
    inputSchema: {
      workspaceSlug: z.string().describe("Slug of the workspace to query, e.g. 'my-workspace'"),
      question: z.string().describe("The question to ask against the workspace's documents"),
    },
  },
  async ({ workspaceSlug, question }) => {
    const data = await allm(`/api/v1/workspace/${encodeURIComponent(workspaceSlug)}/chat`, {
      method: "POST",
      body: JSON.stringify({ message: question, mode: "query" }),
    });
    return {
      content: [
        {
          type: "text",
          text: data.textResponse || JSON.stringify(data, null, 2),
        },
      ],
    };
  }
);

const transport = new StdioServerTransport();
await server.connect(transport);
