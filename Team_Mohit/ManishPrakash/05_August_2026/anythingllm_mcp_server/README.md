# AnythingLLM RAG → MCP server

Runnable source for the advanced task. Full design rationale, client wiring, test
plan, and security notes: [`../06_anythingllm_rag_as_mcp.md`](../06_anythingllm_rag_as_mcp.md).

## What it does

Wraps AnythingLLM's REST API in an MCP server so any MCP-speaking agent
(OpenClaw, Multica-driven agents, IDEs) can retrieve from your document corpus
without any client-side integration code.

## Tools

| Tool | Returns |
|---|---|
| `list_knowledge_bases` | Available workspaces |
| `search_documents` | Raw matching passages + sources + similarity scores |
| `ask_knowledge_base` | Synthesised RAG answer with citations |
| `list_documents` | Ingested document list |

Read-only by design — no ingestion or deletion tools.

## Install

```bash
pip install -r requirements.txt
export ANYTHINGLLM_BASE_URL=http://localhost:3001
export ANYTHINGLLM_API_KEY=...        # AnythingLLM → Settings → API Keys
python3 anythingllm_mcp_server.py
```

Communicates over stdio, so it is normally launched by the MCP client rather than
run by hand — running it directly just confirms it starts without error.

## Client config

```jsonc
{
  "mcpServers": {
    "anythingllm-rag": {
      "command": "python3",
      "args": ["/absolute/path/to/anythingllm_mcp_server.py"],
      "env": {
        "ANYTHINGLLM_BASE_URL": "http://anythingllm:3001",
        "ANYTHINGLLM_API_KEY": "${ANYTHINGLLM_API_KEY}"
      }
    }
  }
}
```

Absolute path — clients do not expand `~` or resolve relative paths.

## One thing that is easy to miss

Granting the tools is not enough. Add an explicit instruction to the agent's
`AGENTS.md`:

> Before answering from your own knowledge, search the knowledge base with
> `search_documents`. If the answer is there, cite the source document.

Without it the agent has the capability and never thinks to use it. This is the most
common reason a correct RAG integration appears to do nothing.

## Note on the code

The Python is ~120 lines of HTTP plumbing. The actual engineering is in the
docstrings — they are model-facing documentation, and they are what determines
whether the agent picks the right tool.
