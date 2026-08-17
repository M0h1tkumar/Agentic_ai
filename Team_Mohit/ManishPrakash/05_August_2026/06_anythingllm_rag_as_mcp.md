# 6 — Exposing AnythingLLM's RAG database as an MCP server

**Manish Prakash · Team Mohit · 5 August 2026** *(advanced task)*

**Goal:** let Multica / OpenClaw agents retrieve documents from AnythingLLM's vector
store during execution, by putting an MCP server in front of AnythingLLM's API.

---

## 1. Why this is the right shape

AnythingLLM is a document ingestion and RAG system: you drop in PDFs and docs, it
chunks, embeds, and stores them in a vector database (LanceDB by default, or
Qdrant/pgvector), and answers questions over them. It already solves the hard part —
parsing, chunking, embedding, and retrieval.

The agents in OpenClaw and Multica cannot reach any of that. They have no knowledge
of the documents.

Three ways to connect them:

| Approach | Verdict |
|---|---|
| Re-embed the documents inside the agent stack | Duplicates the corpus, duplicates the ingestion pipeline, guarantees drift. No. |
| Hard-code AnythingLLM API calls into each agent | Works, but is the M×N problem from [`../06_August_2026/api_vs_mcp.md`](../06_August_2026/api_vs_mcp.md) — new glue per client. |
| **Wrap the AnythingLLM API in one MCP server** | One implementation, usable by every MCP-speaking client. |

The third is the task, and it is the right answer for exactly the reason MCP exists:
**one server, many clients, discovered at runtime.**

```
Documents → AnythingLLM (chunk, embed, store)
                   │  REST API
                   ▼
            MCP server (this task)
                   │  JSON-RPC / stdio
      ┌────────────┼────────────┐
   OpenClaw     Multica      any MCP client
```

---

## 2. Prerequisites

1. **AnythingLLM running** with a workspace and documents embedded.
2. **An API key** — Settings → API Keys → Generate. Static bearer token; treat it
   accordingly ([`../29_July_2026/oauth_vs_api_key.md`](../29_July_2026/oauth_vs_api_key.md)).
3. **Network reachability.** If both are in Docker, put them on the shared
   `agentic-net` network from
   [`01_multica_docker_install.md`](01_multica_docker_install.md) and use the
   service name as the host.
4. Python 3.10+ and the MCP SDK: `pip install mcp httpx`.

The relevant AnythingLLM endpoints:

| Endpoint | Purpose |
|---|---|
| `GET /api/v1/workspaces` | List workspaces |
| `POST /api/v1/workspace/{slug}/chat` | Ask a question — RAG-answered |
| `POST /api/v1/workspace/{slug}/vector-search` | Raw similarity search, returns chunks |
| `GET /api/v1/documents` | List ingested documents |

**`vector-search` is the important one.** It returns the retrieved chunks without
running them through AnythingLLM's own LLM. That is what an agent wants: the agent
has its own model and should reason over the raw evidence rather than over another
model's summary of it. Summarising twice loses detail and hides the sources.

---

## 3. Server design

Four tools, deliberately narrow:

| Tool | Purpose |
|---|---|
| `list_knowledge_bases` | Discover available workspaces |
| `search_documents` | Semantic search → raw chunks with sources and scores |
| `ask_knowledge_base` | Full RAG answer, when a synthesised answer is genuinely wanted |
| `list_documents` | See what has been ingested |

Two design decisions worth stating:

- **Both `search_documents` and `ask_knowledge_base` exist**, because they answer
  different questions. Search gives evidence the agent reasons over; ask gives a
  quick synthesised answer. The tool descriptions must make the difference obvious,
  or the model will pick wrongly.
- **No write tools.** Ingestion is a human decision. A retrieval server that cannot
  modify the corpus has a much smaller blast radius, and this server is exposed to
  agents driven by public chat channels.

---

## 4. Implementation

```python
#!/usr/bin/env python3
"""
anythingllm_mcp_server.py — expose AnythingLLM's RAG store over MCP.

Env:
  ANYTHINGLLM_BASE_URL   e.g. http://anythingllm:3001
  ANYTHINGLLM_API_KEY
"""
import os
import httpx
from mcp.server.fastmcp import FastMCP

BASE = os.environ["ANYTHINGLLM_BASE_URL"].rstrip("/")
KEY = os.environ["ANYTHINGLLM_API_KEY"]
HEADERS = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}

mcp = FastMCP("anythingllm-rag")


async def _post(path: str, payload: dict) -> dict:
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(f"{BASE}{path}", headers=HEADERS, json=payload)
        r.raise_for_status()
        return r.json()


async def _get(path: str) -> dict:
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(f"{BASE}{path}", headers=HEADERS)
        r.raise_for_status()
        return r.json()


@mcp.tool()
async def list_knowledge_bases() -> str:
    """List the AnythingLLM workspaces available to search.

    Call this FIRST if you do not already know which workspace holds the
    documents you need. Each workspace is a separate document collection.
    """
    data = await _get("/api/v1/workspaces")
    lines = [
        f"- {w['slug']}: {w.get('name', '')} ({len(w.get('documents', []))} documents)"
        for w in data.get("workspaces", [])
    ]
    return "\n".join(lines) or "No workspaces found."


@mcp.tool()
async def search_documents(workspace: str, query: str, limit: int = 5) -> str:
    """Semantic search over a workspace. Returns the raw matching passages
    with their source documents and similarity scores.

    Use this when you want the underlying evidence so you can reason over it
    and cite sources yourself. Prefer this over `ask_knowledge_base` for
    research, fact-checking, and anything where the source matters.

    Args:
        workspace: workspace slug from `list_knowledge_bases`
        query: natural-language description of what you are looking for
        limit: number of passages to return (1-20, default 5)
    """
    limit = max(1, min(limit, 20))
    data = await _post(
        f"/api/v1/workspace/{workspace}/vector-search",
        {"query": query, "topN": limit},
    )
    results = data.get("results", [])
    if not results:
        return f"No passages in '{workspace}' matched: {query}"

    out = [f"{len(results)} passage(s) for: {query}\n"]
    for i, r in enumerate(results, 1):
        src = r.get("title") or r.get("metadata", {}).get("title", "unknown source")
        score = r.get("score")
        score_str = f" (similarity {score:.3f})" if isinstance(score, (int, float)) else ""
        out.append(f"[{i}] {src}{score_str}\n{r.get('text', '').strip()}\n")
    return "\n".join(out)


@mcp.tool()
async def ask_knowledge_base(workspace: str, question: str) -> str:
    """Ask the knowledge base a question and get a synthesised answer with citations.

    Use this only when you want a quick answer and do not need to inspect the
    source passages. For research or anything you must cite accurately, use
    `search_documents` instead — it returns the evidence rather than another
    model's summary of it.

    Args:
        workspace: workspace slug from `list_knowledge_bases`
        question: the question to answer
    """
    data = await _post(
        f"/api/v1/workspace/{workspace}/chat",
        {"message": question, "mode": "query"},
    )
    answer = data.get("textResponse", "").strip() or "No answer returned."
    sources = data.get("sources", [])
    if sources:
        names = sorted({s.get("title", "unknown") for s in sources})
        answer += "\n\nSources: " + ", ".join(names)
    return answer


@mcp.tool()
async def list_documents() -> str:
    """List the documents ingested into AnythingLLM.

    Use this to check whether a specific document is available before
    searching for its contents.
    """
    data = await _get("/api/v1/documents")
    items = data.get("localFiles", {}).get("items", [])
    names = [i.get("title", i.get("name", "?")) for i in items]
    return "\n".join(f"- {n}" for n in names) or "No documents ingested."


if __name__ == "__main__":
    mcp.run(transport="stdio")
```

Note `mode: "query"` on the chat call — it restricts the answer to the documents
instead of letting the model fall back on its own knowledge. Without it the tool
will confidently answer questions your corpus says nothing about, which is the worst
possible behaviour for a retrieval tool.

**Tool descriptions carry the real design.** Each one says *when* to use it and,
where it matters, when to prefer the other. That is the difference between a tool a
model uses correctly and one it uses at random — the point argued at length in
[`../06_August_2026/api_vs_mcp.md`](../06_August_2026/api_vs_mcp.md) §5.3.

---

## 5. Connecting clients

**OpenClaw / any MCP client:**

```jsonc
{
  "mcpServers": {
    "anythingllm-rag": {
      "command": "python3",
      "args": ["/opt/mcp/anythingllm_mcp_server.py"],
      "env": {
        "ANYTHINGLLM_BASE_URL": "http://anythingllm:3001",
        "ANYTHINGLLM_API_KEY": "${ANYTHINGLLM_API_KEY}"
      }
    }
  }
}
```

Then grant the tools in the agent's `tools.allow` list, and add a line to its
`AGENTS.md`:

> Before answering from your own knowledge, search the knowledge base with
> `search_documents`. If the answer is there, cite the source document.

Without that instruction the agent has the tool and does not think to use it. This
is the most common reason a correctly-built RAG integration appears to do nothing.

**Multica:** the daemon spawns the agent CLI, so the agent's MCP config is what
matters — configure OpenClaw and Multica-assigned issues inherit the capability.
No Multica-side change at all, which is precisely the M+N benefit in practice.

---

## 6. Testing

1. **Server alone** — run it and confirm it starts without an exception.
2. **Tool listing** — connect a client, confirm all four tools appear with their
   descriptions. Missing descriptions mean the docstrings are not being read.
3. **Each tool by hand** — `list_knowledge_bases`, then a `search_documents` call
   with a query you know the answer to.
4. **Agent end-to-end** — ask the agent something answerable only from the
   documents. A correct, cited answer proves the whole chain.
5. **Negative test** — ask something the corpus does not cover. The agent should say
   so rather than inventing an answer. This test matters more than the positive one.

---

## 7. Security

This server hands agents a query interface to your document corpus. That deserves
care:

- **Read-only by design.** No ingestion or deletion tools. Retrieval cannot corrupt
  the corpus.
- **Scope the API key** to the minimum AnythingLLM permits, and keep it in the
  environment, never in the config file in git.
- **Workspace boundaries are your access control.** Anything in a workspace the
  server can reach is readable by any agent connected to it. Keep sensitive
  documents in a separate workspace and a separate server instance.
- **Retrieved text enters the model's context** — so a poisoned document is a
  prompt-injection vector. Ingested documents are part of your trust boundary; treat
  ingestion as a privileged operation.
- **Bind the AnythingLLM API to the internal Docker network**, not to a host port.
- **Cap `limit`.** Enforced in code above; an unbounded `topN` is a context-window
  denial of service.

---

## 8. What this demonstrates

This task is the clearest illustration in the whole program of why MCP matters:

- **One server, every client.** OpenClaw, Multica, an IDE, a future agent — all get
  document retrieval from a single implementation. The M×N → M+N reduction, made
  concrete.
- **The API did not change.** AnythingLLM's REST endpoints are unchanged and
  unaware. MCP is a *wrapper*, not a replacement — the central claim of
  [`api_vs_mcp.md`](../06_August_2026/api_vs_mcp.md).
- **Discovery is the feature.** Agents were not compiled against these tools. They
  connect, call `tools/list`, and can use them.
- **Descriptions are the product.** The Python here is ~120 lines of HTTP calls. The
  engineering is in the docstrings that tell a model when to use each tool.
- **Separation of concerns holds.** AnythingLLM does ingestion and retrieval;
  OpenClaw does reasoning and action; MCP is the seam. Each can be replaced without
  touching the others.
