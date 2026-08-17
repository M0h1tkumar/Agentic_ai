# Integrating AnythingLLM RAG with Multica/OpenClaw

**The Problem:** Our AnythingLLM instance has successfully ingested corporate documents and stored them in a Vector Database (LanceDB / Qdrant). However, our agents running in Multica or VSCode/OpenClaw operate in a separate environment and cannot natively read those documents.

## The Solution Architecture

To allow an OpenClaw agent to query the AnythingLLM RAG database, we must build a bridge. There are two ways to do this:

### 1. The Standard API Route
AnythingLLM exposes a robust REST API.
1. We create a custom tool in OpenClaw (e.g., `query_internal_kb`).
2. The tool accepts a search string.
3. The tool executes an HTTP POST request to `http://localhost:3001/api/v1/workspace/{slug}/chat`.
4. It passes the API Key generated in the AnythingLLM developer settings.
5. AnythingLLM performs the vector search, generates a response with citations, and returns it.
6. The OpenClaw tool parses the JSON and feeds it back to the agent.

### 2. The MCP Route (Advanced)
Instead of writing a custom REST tool for every single agent, we expose the AnythingLLM database as an **MCP (Model Context Protocol) Server**.
- We wrap the AnythingLLM API inside an MCP Server script.
- The server exposes a tool called `search_knowledge_base`.
- Now, *any* MCP-compatible client (Multica, Claude Desktop, Cursor, OpenCode) can instantly connect to the server and gain the ability to search our private documents without us writing any additional glue code!
