# OmniRoute — experiment notes

**Manish Prakash · Team Mohit · 3 August 2026** *(optional task)*

> **Status:** exploratory notes. Treat specific commands as indicative — the value
> here is the concept and the evaluation criteria, both of which transfer to any
> tool in this category.

---

## 1. The problem it addresses

Once you run agents seriously, you hit the same three walls:

1. **Vendor lock-in.** Code written against one provider's SDK does not move.
2. **Cost.** Sending every request to the strongest model is wasteful; most steps in
   an agent loop are mechanical.
3. **Reliability.** One provider having a bad afternoon takes your whole system down.

An **LLM router / gateway** sits between your application and the providers and
solves all three by presenting one endpoint and deciding, per request, which model
actually serves it.

```
Your app ──> Router ──┬──> Anthropic
                      ├──> OpenAI
                      ├──> Google
                      └──> local (Ollama / LM Studio)
```

OmniRoute is one such router. LiteLLM and OpenRouter occupy the same category, and
what I learned applies across all of them.

---

## 2. What a router gives you

| Capability | Why it matters |
|---|---|
| **One API surface** | Usually OpenAI-compatible, so existing clients work unchanged |
| **Model routing** | Cheap model for simple steps, strong model for hard ones |
| **Fallback chains** | Provider down or rate-limited → next in the chain, transparently |
| **Load balancing** | Spread across keys/regions to stay under rate limits |
| **Unified cost tracking** | Spend per model, per key, per project — in one place |
| **Caching** | Identical requests served without a provider call |
| **Central key management** | Provider keys live in the router, not in every service |
| **Observability** | Every request logged in one format |

That last point is quietly the biggest one for agent work. Agents make many model
calls per task, and without a central log you cannot answer "why did that cost ₹40?"
or "which step went wrong?"

---

## 3. Typical setup shape

Routers are almost always a container plus a config file:

```bash
docker run -d --name omniroute \
  -p 8000:8000 \
  -v $(pwd)/config.yaml:/app/config.yaml \
  --env-file .env \
  omniroute/omniroute:latest
```

```yaml
models:
  - name: fast
    provider: anthropic
    model: claude-haiku-4-5
  - name: strong
    provider: anthropic
    model: claude-sonnet-5
  - name: local
    provider: ollama
    model: llama3.1:8b
    base_url: http://host.docker.internal:11434

routing:
  default: fast
  rules:
    - if: { tokens_gt: 8000 }
      use: strong
    - if: { task: code }
      use: strong

fallbacks:
  strong: [fast, local]
```

Because the endpoint is OpenAI-compatible, pointing an existing client at it is a
base-URL change and nothing else:

```python
from openai import OpenAI
client = OpenAI(base_url="http://localhost:8000/v1", api_key="router-key")
```

That compatibility is the whole adoption story. A router that required rewriting
client code would not be worth it.

---

## 4. Fit with the rest of this work

- **OpenClaw** takes a model per agent. Pointing all agents at the router means the
  orchestrator/worker split from
  [`../30_July_2026/multi_agent_team.md`](../30_July_2026/multi_agent_team.md)
  becomes a *config* decision in one file rather than a change across four agent
  definitions.
- **Multica's daemon** spawns agent CLIs. One router endpoint means one place to
  rotate keys and one place to see the bill.
- **AnythingLLM** accepts a custom OpenAI-compatible base URL, so it slots in too.

The pattern is the same one MCP applies to tools: **standardise the interface, then
swap the implementation freely.** Router : models :: MCP : tools. Noticing that
symmetry was the most useful thing to come out of this task.

---

## 5. Trade-offs

**Gains:** provider independence, meaningful cost reduction from routing cheap steps
to cheap models, resilience through fallbacks, one place for keys and logs.

**Costs:**
- **A new single point of failure.** The router being down means everything is down.
- **Added latency.** One extra network hop per call, small but real in a loop.
- **Lowest-common-denominator features.** Provider-specific capabilities (prompt
  caching, extended thinking, computer use) may not be exposed through a generic
  OpenAI-shaped interface. This is the most likely reason to skip a router.
- **Another service to operate**, monitor, and secure.
- **A concentrated secret store.** Every provider key in one place is convenient and
  also a high-value target.

---

## 6. Verdict

Worth it once you have **more than one model, more than one application, or a real
cost problem.** Before that, it is infrastructure without a job.

For a single-developer project calling one provider, a router adds a failure mode
and solves nothing. For the setup this program builds toward — several agents,
several tools, real spend — the cost tracking and fallback behaviour justify it on
their own.

The caveat worth remembering: **check that the router exposes the provider features
you actually rely on.** Losing prompt caching to gain provider independence is a bad
trade if caching is what makes your workload affordable.
