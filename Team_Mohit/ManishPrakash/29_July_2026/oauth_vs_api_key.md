# OAuth (dynamic, session-based) vs API keys (static, permanent)

**Manish Prakash · Team Mohit · 29 July 2026**

---

## 1. The distinction in one line

An **API key** is a *bearer secret* — whoever holds the string is treated as the
owner, forever, with the owner's full permissions.

**OAuth 2.0** is a *delegated authorisation framework* — a user grants an
application limited, scoped, time-bounded access to their resources without ever
handing over their password, and the resulting token expires.

The key difference is not "which is more secure" but **what question each answers**:

| | Question it answers |
|---|---|
| API key | *Which application is calling?* |
| OAuth token | *Which user authorised which application to do what, and until when?* |

---

## 2. API keys — static and permanent

### How they work
A long random string issued by the provider, sent on each request (usually
`Authorization: Bearer sk-...` or an `X-API-Key` header). The server looks it up and
grants the associated permissions. No handshake, no expiry.

### Positives

- **Trivially simple.** One header. Any language, any tool, `curl` included. This
  simplicity is the reason API keys remain everywhere.
- **No round trips.** No token exchange, no refresh call — lower latency and one
  fewer failure mode.
- **Ideal for server-to-server.** Cron jobs, backend services, and CI have no user
  present to complete an interactive consent flow.
- **Easy to reason about and debug.** Requests are reproducible; a failing call can
  be replayed exactly.
- **Stateless on the client.** No token storage, no expiry handling, no refresh
  logic to get wrong.
- **Usually good enough for attribution** — per-key rate limits, usage metering, and
  billing all work fine.

### Negatives

- **Permanent by default.** A leaked key stays valid until someone notices and
  revokes it. Median time-to-detection for leaked secrets is measured in months.
- **Full-privilege bearer token.** Classically all-or-nothing; anyone holding it has
  everything the owner has. Finer-grained keys exist now but are opt-in and often
  unused.
- **Leaks constantly, in predictable ways.** Committed to git, pasted into Slack,
  baked into a Docker image layer, logged in a URL query string, left in a
  `.env` that got shipped.
- **Cannot be embedded in a client.** Any key in a mobile app, SPA, or browser
  extension is public — decompilation and DevTools both trivially expose it.
- **No user identity.** The key identifies an application, not a person. Poor for
  per-user audit trails.
- **Rotation is painful.** Manual, coordinated, and disruptive, so in practice it
  rarely happens on schedule.
- **No standard consent model.** Nothing tells an end user "this app can read your
  files"; there is nothing to review and nothing to revoke selectively.

---

## 3. OAuth 2.0 — dynamic and session-based

### How it works
Roles: **resource owner** (the user), **client** (the app), **authorisation server**
(issues tokens), **resource server** (holds the data).

Standard Authorization Code flow with PKCE:

1. App redirects the user to the provider's consent screen with the scopes it wants.
2. User authenticates *with the provider* and approves.
3. Provider redirects back with a short-lived **authorization code**.
4. App exchanges the code (plus its client secret / PKCE verifier) for an
   **access token** (short-lived, e.g. 1 hour) and a **refresh token** (long-lived).
5. App calls APIs with the access token; when it expires, it silently uses the
   refresh token to get a new one.

### Positives

- **Scoped access.** `read:files` is not `delete:everything`. Least privilege is
  built into the protocol rather than bolted on.
- **Short-lived access tokens.** A leaked token is useless within the hour. This is
  the single biggest security advantage over static keys.
- **Revocable per grant.** A user can revoke one app without changing their password
  or affecting any other app.
- **The password is never shared.** The third-party app never sees the user's
  credentials — the original problem OAuth was invented to solve.
- **User identity and audit.** Actions attribute to a real person, which regulated
  environments require.
- **Explicit consent UI.** The user sees and approves what is being granted.
- **Safe for public clients.** PKCE makes the flow safe for mobile apps and SPAs
  that cannot hold a secret.
- **Industry standard.** Widely implemented, widely reviewed, with mature libraries.
  OpenID Connect adds authentication on top of it.
- **Now the standard for remote MCP servers**, which matters directly for the
  agentic work in this repo.

### Negatives

- **Substantially more complex.** Multiple flows (authorization code, PKCE, client
  credentials, device code), redirect URIs, state parameters, token storage,
  refresh handling. Far more surface to implement incorrectly.
- **Requires a browser and a present user** for the interactive flows — awkward or
  impossible for headless services, though `client_credentials` covers that case.
- **Refresh-token handling is a common bug source.** Race conditions when several
  processes refresh at once; a mishandled rotation logs everyone out.
- **The refresh token is itself a long-lived secret.** It must be stored as
  carefully as an API key — the problem is reduced, not eliminated.
- **More moving parts, more failure modes.** Clock skew, misconfigured redirect
  URIs, expired client secrets, consent-screen changes.
- **Implementation quality varies.** "OAuth" on the tin does not guarantee a correct
  or consistent implementation between providers.
- **Consent fatigue.** Users approve broad scopes without reading them, which
  weakens the model's central protection.
- **Higher latency and infrastructure cost.** Extra round trips and an
  authorisation server to run.

---

## 4. Side-by-side

| Dimension | API key (static) | OAuth (dynamic) |
|---|---|---|
| Lifetime | Permanent until revoked | Access token minutes–hours |
| Granularity | Usually all-or-nothing | Scoped per permission |
| Identifies | The application | The user *and* the application |
| Setup complexity | Very low | High |
| Leak blast radius | Total, until noticed | Bounded by scope + expiry |
| Safe in a browser/mobile client | **No** | Yes (with PKCE) |
| Works headless | Yes | Only `client_credentials` / device flow |
| Revocation | Rotate the key, break all users | Per-user, per-app |
| End-user consent | None | Explicit screen |
| Audit trail | Per key | Per user |
| Latency | One request | Extra handshake + refresh |
| Best for | Server-to-server, CI, scripts | Third-party access to user data |

---

## 5. Practical guidance

**Use an API key when:**
- Backend-to-backend, no end user involved.
- CI/CD pipelines and cron jobs.
- Internal services on a trusted network.
- Rapid prototyping.

**Use OAuth when:**
- Your app acts on behalf of a user's account.
- The client is a mobile app, SPA, or anything running on a device you don't control.
- You need per-user audit trails or regulatory compliance.
- Users must be able to revoke access independently.

**Whichever you use:**
1. Never commit secrets. Use environment variables or a secret manager; add
   pre-commit secret scanning.
2. Rotate on a schedule and treat any exposure as compromise.
3. Scope down aggressively — read-only unless writes are genuinely needed.
4. Never put a secret in a URL query string; it lands in logs, proxies, and browser
   history.
5. Use separate credentials per environment and per service.
6. Monitor for anomalous usage — volume spikes and unfamiliar source IPs.
7. Set expiry even on API keys where the provider supports it.

---

## 6. Relevance to agentic AI

This is not an abstract comparison for this course. Agents amplify both failure
modes:

- An agent with a **static API key** has that key's full permissions, permanently,
  and may be steered by prompt injection into using it in ways nobody intended.
- **Scoped, expiring OAuth tokens** bound the damage of a compromised or manipulated
  agent to what was actually granted, for as long as it was granted.

That is precisely why remote MCP servers standardise on OAuth 2.1, and why local
stdio servers — which run as a subprocess with your privileges and often read a
plain API key from the environment — deserve the security scrutiny described in
[`../06_August_2026/mcp_directories_exploration.md`](../06_August_2026/mcp_directories_exploration.md).

---

## 7. Verdict

Neither is universally better; they solve different problems.

- **API keys** trade security for simplicity. Correct for machine-to-machine work,
  wrong anywhere near an end user's data or an untrusted client.
- **OAuth** trades simplicity for security and delegation. Correct whenever a user's
  data is accessed by software the user does not own.

The most common real-world mistake is not choosing wrongly in principle — it is
using a static key where a scoped token belonged, because the key was faster to
implement.
