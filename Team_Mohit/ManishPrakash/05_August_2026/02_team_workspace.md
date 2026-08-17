# 2 — Team workspace creation

**Manish Prakash · Team Mohit · 5 August 2026**

> **Task status:** marked *"to be implemented by respective team leaders only."*
> I am not the team leader, so I did not create the Team Mohit workspace. These are
> my notes on the workspace model and how I set up my own for testing — useful when
> the shared workspace arrives and I need to understand its structure.

---

## The hierarchy

```
Instance                    one deployment
 └── Workspace              a team — members, agents, settings
      └── Project           a body of work
           └── Issue        a unit of work, assignable to a human or an agent
                └── Comments / status / history
```

The workspace is the **permission and isolation boundary**. Members, agents,
provider keys, and projects all belong to a workspace, and nothing crosses between
them. That makes it the right unit for a team.

---

## Creating one

1. Sign in as the instance admin (the first account created).
2. **Workspaces → New**; name it after the team.
3. **Invite members** by email.
4. **Register agents** as assignable identities.
5. **Configure the model provider** — keys are workspace-scoped.
6. **Create the first project.**

---

## What I would argue for in the Team Mohit workspace

**Roles.** Admin (leader), Member (create/assign issues), and read-only Viewer for
anyone observing. Not everyone should be able to change provider keys — that is the
billing surface.

**Agent registration.** Register agents by *function*, not by owner:
`researcher`, `writer`, `reviewer`. Agents named after people become that person's
private tool, which defeats the point of a shared workspace.

**Projects.** One per deliverable stream rather than one per person. Per-person
projects reproduce individual folders and lose the shared visibility that made the
workspace worth creating.

**Issue conventions.** An issue assigned to an agent *is* its prompt. Vague issues
produce vague output, and unlike a chat you cannot iterate mid-run. What worked:

- Title = the deliverable, not the topic.
- Body states **acceptance criteria** explicitly.
- Link related issues rather than restating context.

**Key management.** One workspace-level provider key with usage caps, not personal
keys. Central rotation, and spend is attributable — see
[`../29_July_2026/oauth_vs_api_key.md`](../29_July_2026/oauth_vs_api_key.md).

---

## My own test workspace

To understand the model before the team one exists, I created a personal workspace
with one project and two registered agents, then ran a small issue end to end.

What that exercise taught me, and the reason it was worth doing:

- **An agent-assigned issue is a prompt with a database row around it.** All the
  usual prompt-quality rules apply, plus you lose interactivity — you cannot nudge
  a running issue the way you can nudge a chat.
- **Acceptance criteria in the issue body are the single highest-leverage habit.**
  Without them there is no way to judge whether the agent's output is done.
- **The workspace boundary is genuinely useful** for keeping experiments from
  polluting real work — my broken test issues stayed in my own workspace.
- **Nothing happens without the daemon.** Worth stating again because the UI gives
  no hint: the issue sits in "assigned" indefinitely and looks like a platform bug.

---

## Handover note for the team leader

When creating the Team Mohit workspace, the decisions that are hard to change later:

1. **Workspace name and slug** — appears in URLs.
2. **Role assignment** — who can touch provider keys.
3. **Project structure** — per-deliverable, not per-person.
4. **Agent naming** — by function, not by owner.
5. **A written issue template** with acceptance criteria, agreed before the first
   issue rather than retrofitted after twenty.
