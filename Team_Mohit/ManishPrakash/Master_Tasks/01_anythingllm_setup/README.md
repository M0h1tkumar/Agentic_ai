# AnythingLLM setup

**Master task 1:** multi-user, browser search, NVIDIA API / OpenRouter, vector DB,
database connection, trial run.

> **Status:** configuration reference. The Docker deployment and settings below are
> the configuration I use. Items I could not verify end to end on this machine are
> marked *(unverified)*.

---

## What AnythingLLM is, and where it sits

A self-hosted document chat application: ingest documents, it chunks and embeds
them into a vector store, and a chat interface answers questions grounded in that
corpus with citations.

Its role in this repository is specific. AnythingLLM does **ingestion and
retrieval**; it does not do agentic work. The full path:

```
documents -> docmd -> AnythingLLM (chunk, embed, store) -> MCP server -> agents
             task 2                    this task              5 Aug task
```

Understanding that division early avoids the common mistake of trying to make
AnythingLLM the whole system. It is one component, and the seam on either side is
what makes it replaceable.

---

## Deployment

Docker, for the same reasons as everywhere else in this repository: reproducible
across a team, isolated from the host, and a clean uninstall.

```bash
docker run -d --name anythingllm \
  --network agentic-net \
  -p 3001:3001 \
  -v anythingllm-storage:/app/server/storage \
  -e STORAGE_DIR=/app/server/storage \
  mintplexlabs/anythingllm
```

Three notes that matter more than they look:

- **Named volume, not a bind mount.** All state — the vector store, uploaded
  documents, users, settings — lives in `/app/server/storage`. Lose it and you lose
  everything except the original files.
- **`agentic-net`** is the shared external network from
  [`../../05_August_2026/01_multica_docker_install.md`](../../05_August_2026/01_multica_docker_install.md),
  so OpenClaw and the MCP server can reach it by service name.
- **Do not publish port 3001 to the internet** without a reverse proxy and TLS. The
  API key is a static bearer token.

---

## 1. Multi-user mode

Settings → Security → **Multi-User Mode**.

This changes the product materially rather than just adding logins:

| | Single-user | Multi-user |
|---|---|---|
| Access | Anyone who can reach the port | Named accounts |
| Workspaces | All shared | Per-user permissions |
| Roles | None | Admin / Manager / Default |
| Audit | None | Actions attributable to a person |

**Enable it before inviting anyone**, not after. The migration is straightforward
but the window in between is an unauthenticated instance holding your documents.

Roles worth using deliberately: **Admin** manages users and provider keys — that is
the billing surface, so keep it small. **Manager** creates workspaces. **Default**
uses workspaces they are granted.

---

## 2. Browser search

Agent Skills → **Web Search**, then pick a provider (SearXNG, Google PSE, Serper,
Bing). SearXNG is the one worth preferring: self-hostable, so search queries do not
leave your network either.

The point of enabling it is coverage of the gap in RAG. Retrieval answers "what do
my documents say?" and returns nothing useful for "what happened this week?" Web
search covers the second question, and the workspace prompt should say which to
prefer, or the model will pick inconsistently.

**Security note:** enabling web search means fetched web content enters the model's
context. That is untrusted input by definition, and it is a prompt-injection surface
in exactly the way an ingested document is.

---

## 3. LLM provider — NVIDIA NIM or OpenRouter

Settings → LLM Preference. Both are OpenAI-compatible, so they configure identically:

| Provider | Base URL | Notes |
|---|---|---|
| **OpenRouter** | `https://openrouter.ai/api/v1` | One key, many models, per-request routing |
| **NVIDIA NIM** | `https://integrate.api.nvidia.com/v1` | NVIDIA-hosted open models, generous free tier |
| **Local (Ollama)** | `http://host.docker.internal:11434/v1` | Nothing leaves the machine |

From inside Docker, a local Ollama is **not** at `localhost` — that is the container
itself. Use `host.docker.internal` (or the host's LAN address on Linux without that
alias). This is the same class of mistake as the Compose database host.

Because all three speak the same protocol, an LLM router in front turns provider
choice into a config edit rather than a settings change —
[`../../03_August_2026/omniroute_notes.md`](../../03_August_2026/omniroute_notes.md).

**Embedding model is a separate setting**, and it is the one people forget.
Changing it invalidates every existing embedding: old vectors and new queries land
in different spaces, so retrieval silently degrades rather than failing. **Choose it
before ingesting at volume, and re-embed everything if you change it.**

---

## 4. Vector database

Settings → Vector Database. Default is **LanceDB**, embedded, no separate service.

| Option | When |
|---|---|
| **LanceDB** | Default. Embedded, zero ops, fine to tens of thousands of chunks |
| **Qdrant** | Separate service, better filtering and scale, real ops story |
| **pgvector** | You already run Postgres and want one backup story |
| **Chroma / Milvus / Weaviate** | Supported; pick if already in use |

```bash
docker run -d --name qdrant --network agentic-net \
  -p 6333:6333 -v qdrant-storage:/qdrant/storage qdrant/qdrant
```

Then point AnythingLLM at `http://qdrant:6333` — service name, not localhost.

**Start with LanceDB.** Migrating later means re-embedding, which costs an
afternoon; standing up Qdrant on day one for a corpus of two hundred documents is
infrastructure without a job.

---

## 5. Database connection

Agent Skills → **SQL Connector**. Supports Postgres, MySQL, and SQL Server.

The one rule that matters: **connect with a read-only user, scoped to the schema the
agent needs.**

```sql
CREATE USER llm_reader WITH PASSWORD '...';
GRANT CONNECT ON DATABASE app TO llm_reader;
GRANT USAGE ON SCHEMA public TO llm_reader;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO llm_reader;
```

An LLM generating SQL against a write-capable connection is a bad combination:
the model can be steered by prompt injection, and `DROP TABLE` is a plausible token
sequence. Read-only is not a precaution, it is the design.

---

## 6. Trial run

The sequence that actually establishes it works:

1. **Create a workspace.** One per subject; a single workspace holding unrelated
   corpora retrieves badly because everything is a weak match for everything.
2. **Upload documents** — ideally the markdown from
   [`../02_doc_to_markdown/`](../02_doc_to_markdown/), which arrives with
   provenance frontmatter already attached.
3. **Move them into the workspace and embed.** Upload and embed are separate
   operations. A document in storage but not in a workspace is never retrieved, and
   this is the single most common reason ingestion appears to work while search
   finds nothing.
4. **Ask a question you know the answer to.** Verify the citation points at the
   right document.
5. **Ask a question the corpus does not cover.** This test matters more than the
   first. Set the workspace to **Query mode** and confirm the model says it does not
   know instead of answering from its own training. Chat mode will happily fill the
   gap, which is the wrong behaviour for a document assistant.

**Query vs Chat mode** is the setting most worth understanding: Query restricts
answers to retrieved context, Chat allows the model's general knowledge. For a
document assistant, Query is almost always correct.

---

## Troubleshooting

| Symptom | Cause |
|---|---|
| Retrieval returns nothing | Documents uploaded but never moved into the workspace and embedded |
| Answers ignore the documents | Workspace is in Chat mode, not Query mode |
| Retrieval degraded after a settings change | Embedding model changed; old vectors are in a different space. Re-embed |
| Cannot reach local Ollama | Used `localhost` from inside the container |
| Everything lost after a restart | No named volume on `/app/server/storage` |
| Citations point at the wrong chunk | Chunk size too large; reduce it and re-embed |

---

## Security summary

- Enable multi-user **before** exposing the instance.
- **Read-only database users**, always.
- Never publish port 3001 without TLS and a reverse proxy.
- The API key is a **static bearer token** — environment variables only, never
  committed. See [`../../29_July_2026/oauth_vs_api_key.md`](../../29_July_2026/oauth_vs_api_key.md).
- **Ingestion is a privileged operation.** Anything in a workspace is readable by
  every agent connected to it, and retrieved text enters the model's context. A
  poisoned document is a prompt-injection vector, so what you ingest is part of your
  trust boundary.
