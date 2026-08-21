# Developing Agents in Visual Studio Code with GitHub Copilot

## 1. Introduction

GitHub Copilot started mainly as a coding assistant that could suggest lines of code while you were typing. But inside Visual Studio Code, it has evolved into something much more capable with **Agent Mode**.

Instead of asking Copilot to complete one small piece of code at a time, you can give it an entire development task. The agent can understand the project, create or modify multiple files, run commands in the terminal, execute tests, inspect errors, and make additional changes based on the results.

In simple terms, it feels less like an autocomplete tool and more like having a **junior developer working beside you**.

There is another feature called the **Coding Agent**, but it works differently. Rather than operating directly inside your VS Code workspace, it works in the cloud. You can assign it a GitHub Issue, and it can work on the task in the background before returning a pull request that you can review.

Agent Mode can also work with **MCP (Model Context Protocol)**. MCP allows the agent to interact with external tools and information sources, such as databases, GitHub, APIs, or documentation systems.

---

## 2. How Agent Mode Works

The biggest difference between traditional Copilot and Agent Mode is the level of responsibility given to the AI.

With normal autocomplete, the workflow is roughly:

> **You write code → Copilot suggests code → You accept or modify it**

With Agent Mode, the process is closer to:

> **You describe the goal → Agent plans the work → Changes files → Runs commands/tests → Checks errors → Makes corrections**

For example, instead of manually creating an Express project, installing packages, configuring TypeScript, creating routes, and writing tests, you could give Copilot a request such as:

> **“Create a TypeScript Express API with basic authentication, testing, and proper project structure.”**

The agent can then work through the different steps required to reach that goal.

This makes it particularly useful for tasks that involve multiple files or several connected changes.

---

## 3. Major Advantages

### 🔹 1. Handles Multi-Step Development Tasks

One of the biggest benefits is that you don't have to break every task into tiny instructions.

You can describe the desired outcome, and the agent can determine many of the steps required to achieve it.

For example:

> “Add authentication to this application and include tests for login and registration.”

The agent may need to modify routes, controllers, middleware, database models, configuration files, and tests to complete the task.

---

### 🔹 2. Works Across the Entire Project

Agent Mode isn't limited to the file currently open in your editor.

It can inspect the project structure and make related changes across multiple files.

This becomes particularly useful during:

* Refactoring
* Feature development
* Dependency updates
* API changes
* Project restructuring
* Test implementation

Instead of manually finding every file that needs modification, the agent can identify many of those dependencies itself.

---

### 🔹 3. Can Learn From Its Mistakes

Another useful feature is its ability to work iteratively.

Suppose the agent modifies the application and runs the tests. If a test fails, it can inspect the error, identify a possible cause, modify the code, and run the tests again.

The workflow can therefore look like:

> **Modify → Run → Detect error → Analyse → Fix → Test again**

This doesn't guarantee that every problem will be solved correctly, but it can significantly reduce the amount of manual debugging required for straightforward issues.

---

### 🔹 4. Reduces Repetitive Work

Developers spend a lot of time on tasks that are necessary but not particularly creative.

Examples include:

* Creating project boilerplate
* Setting up configuration files
* Writing basic tests
* Adding linting rules
* Creating repetitive components
* Updating similar code across files

Agent Mode can automate much of this work, allowing developers to spend more time on architecture, product decisions, and complex problems.

---

### 🔹 5. Can Follow Project-Specific Rules

AI-generated code can sometimes conflict with the way a particular project is organized.

To reduce this problem, developers can provide project-specific instructions describing things such as:

* Coding conventions
* Naming patterns
* Folder structure
* Preferred libraries
* Testing practices
* Architectural rules

This gives the agent additional context instead of making it guess how the project should be maintained.

---

### 🔹 6. Can Connect to External Tools Through MCP

**Model Context Protocol (MCP)** extends what an agent can access.

Instead of only working with the files in VS Code, an MCP connection can allow an agent to interact with external systems and tools.

Depending on the setup, this could include:

* Databases
* GitHub
* Documentation
* APIs
* Development tools

This makes the agent more useful for workflows where information or actions exist outside the local codebase.

However, additional access also means additional security responsibility.

---

## 4. Disadvantages and Risks

Despite its capabilities, Agent Mode should not be treated as a completely autonomous developer.

### ⚠️ 1. Usage Limits Can Become a Problem

Agent-based features consume usage resources, including premium requests depending on the GitHub Copilot plan.

A complicated task may require many interactions because the agent might need to inspect files, make changes, run tests, encounter errors, and try again.

As a result, large tasks can consume available usage relatively quickly, and additional usage may involve extra cost depending on the plan.

---

### ⚠️ 2. Vague Instructions Can Produce Poor Results

The quality of the result depends heavily on how clearly the task is described.

For example:

> “Improve my application.”

is extremely open-ended.

The agent has to guess what “improve” means.

A better instruction would specify:

> “Improve the dashboard by adding loading states, handling API errors, and making the layout responsive without changing the existing API.”

The more precise the goal and constraints are, the easier it is for the agent to work in the right direction.

---

### ⚠️ 3. Human Review Is Still Necessary

Agent Mode can edit files and execute terminal commands, which means mistakes can have real consequences.

An agent might:

* Modify the wrong file
* Remove code that was still needed
* Install an unnecessary dependency
* Change an existing behaviour
* Introduce a security issue
* Make assumptions that don't match the project's requirements

Because of this, developers should review the changes rather than blindly accepting everything.

Auto-approval settings require even more caution because they can give the agent greater freedom to perform actions without asking for confirmation.

---

### ⚠️ 4. It Doesn't Always Understand the Bigger Picture

An agent may produce code that is technically valid but still wrong for the actual product.

For example, it might successfully implement a feature but use an architecture that doesn't fit the rest of the application.

This highlights an important distinction:

> **Writing working code is not the same as understanding the software.**

The developer still needs to make decisions about architecture, requirements, security, performance, and maintainability.

---

### ⚠️ 5. Good Results Require Good Instructions

Using an AI coding agent effectively is itself a skill.

Developers need to learn how to communicate:

* What needs to be changed
* What must remain unchanged
* Which technologies should be used
* What constraints exist
* How success should be verified

In other words, simply giving an AI more freedom does not automatically produce better results.

---

### ⚠️ 6. MCP Introduces Additional Security Concerns

MCP can make agents much more powerful because it allows them to interact with external systems.

But greater access also means greater risk.

If an agent has access to a database, repository, API, or other external service, an incorrect instruction or poorly configured connection could potentially lead to unintended actions.

Therefore, MCP integrations should follow the **principle of least privilege**—the agent should receive only the access it actually needs.

---

## 5. Agent Mode vs Coding Agent

Although the two names sound similar, they serve different workflows.

| Feature         | Agent Mode in VS Code             | Coding Agent                        |
| --------------- | --------------------------------- | ----------------------------------- |
| Where it works  | Inside your VS Code environment   | Primarily in the cloud              |
| How you start   | Give it a task in your workspace  | Assign a GitHub Issue               |
| Main purpose    | Interactive development           | Background task execution           |
| File changes    | Directly works with the workspace | Works on the assigned task remotely |
| Result          | Updated project/code              | Pull request for review             |
| Best suited for | Active development and debugging  | Delegating larger tasks             |

So, Agent Mode is closer to **pair programming**, while the Coding Agent is closer to **delegating a development task to a teammate**.

---

## 6. Best Way to Use GitHub Copilot Agents

The most effective approach is not to give the agent complete freedom.

A better workflow is:

### Step 1 — Explain the Goal

Clearly describe what you want to achieve.

### Step 2 — Provide Constraints

Mention the technologies, files, architecture, or behaviours that should not be changed.

### Step 3 — Let the Agent Plan

Allow it to inspect the project and determine the required changes.

### Step 4 — Review the Changes

Check the modified files before assuming everything is correct.

### Step 5 — Run Tests

Make sure the implementation actually works.

### Step 6 — Check the Final Result

Even if all tests pass, verify that the feature behaves the way you intended.

This keeps the developer **in control of the process** while still gaining the productivity benefits of AI agents.

---

## 7. Conclusion

GitHub Copilot's Agent Mode represents a significant change from traditional AI code completion.

Instead of simply predicting the next line of code, it can participate in a larger development workflow—understanding a task, modifying multiple files, running commands, testing the application, analysing errors, and iterating on the solution.

For students and developers, this can save a considerable amount of time, especially when dealing with repetitive work, project setup, refactoring, and straightforward debugging.

At the same time, it would be a mistake to treat it as a replacement for a developer.

The agent can generate code, but the developer is still responsible for understanding **why the code should exist, whether the approach is appropriate, and whether the final result is safe and correct**.

The most useful mindset is therefore not:

> **“Let the AI build everything for me.”**

but:

> **“Let the AI handle the repetitive work while I remain responsible for the important decisions.”**

When used with clear instructions, proper project context, careful review, and sensible security practices, GitHub Copilot Agent Mode can become a powerful development assistant rather than just another code-generation tool.
