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
