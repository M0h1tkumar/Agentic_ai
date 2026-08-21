# API vs MCP

## What is an API?

An **API (Application Programming Interface)** is a contract between two software systems. One side exposes endpoints (URLs), the other calls them with HTTP requests. The caller must know *in advance* what endpoints exist, what parameters they take, and how to parse the response.

Example: to get Bhubaneswar's weather, you call:
```
GET https://api.open-meteo.com/v1/forecast?latitude=20.29&longitude=85.82&current_weather=true
```
You wrote that URL. You knew the parameter names. You parsed the JSON yourself.

---

## What is MCP?

**MCP (Model Context Protocol)** is a protocol that lets an AI model *discover and call tools at runtime* without being hardcoded to any specific endpoint.

An MCP server exposes **named tools** with typed schemas. The AI reads the schema, understands what the tool does from its description, and decides when and how to call it — all on its own.

Example: the `bhubaneswar-weather` MCP server in this folder exposes a tool called `get_bhubaneswar_weather`. Claude reads its description and input schema, then calls it when the user asks *"what's the weather like in Bhubaneswar?"* — no hardcoded URL, no manual parsing.

---

## Side-by-Side Comparison

| | API | MCP |
|---|---|---|
| Who decides when to call it? | The developer (hardcoded logic) | The AI model (at runtime) |
| How does the caller know what's available? | Docs / OpenAPI spec (read by humans) | Tool schema (read by the model) |
| Integration effort | Write HTTP client code per endpoint | Register the server once in `mcp-config.json` |
| Composability | Manual — you chain calls in code | Automatic — the model chains tools as needed |
| Context passing | You manage state between calls | The model carries context across tool calls |

---

## Drawbacks of API over MCP

1. **Hardcoded knowledge** — The developer must read the API docs, understand every endpoint, and bake that knowledge into code. If the API changes, the code breaks.

2. **No self-discovery** — An API cannot tell the AI "here is what I can do." The AI has zero awareness of available capabilities unless a human writes a wrapper.

3. **Manual orchestration** — Chaining multiple API calls (e.g., fetch weather → summarise → send to Telegram) requires explicit glue code. With MCP, the model orchestrates this itself.

4. **Rigid input/output handling** — You write parsers for every response format. MCP tools return structured content the model already knows how to interpret.

5. **No context continuity** — APIs are stateless by design. Passing context between sequential calls is your problem. MCP keeps the model in the loop across the entire tool-use chain.

6. **Scaling complexity** — Adding a new capability means writing more HTTP client code, error handling, and tests. Adding a new MCP tool means writing one `registerTool()` block and the model picks it up automatically.

---

## In Short

> An API is a door that *you* must open manually every time.  
> MCP is a door the AI can open by itself, once you tell it the door exists.

MCP doesn't replace APIs — the `bhubaneswar-weather` MCP server *internally* calls the Open-Meteo API. MCP is the layer that makes those APIs accessible to an AI agent without human-written glue code for every interaction.
