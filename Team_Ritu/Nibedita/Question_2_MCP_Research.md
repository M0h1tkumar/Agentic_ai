TASK
13 / 08 / 2026

Question 2: Comprehensive Research Report on the Model

Context Protocol (MCP)

1. Introduction and Core Motivation

Historically,  empowering  Large  Language  Models  (LLMs)  with  external  data  and  execution  capabilities

required brittle, proprietary, and highly fragmented integrations. Every AI application vendor built custom

plugins   and   bespoke   database   connectors,   creating   an   intractable   integration   matrix.   Introduced   by

Anthropic, the Model Context Protocol (MCP) establishes an open, universal standard designed to solve this

fragmentation by acting as a "USB-C port for artificial intelligence applications," enabling seamless plug-

and-play interoperability.

2. Structural Architecture of MCP

The MCP ecosystem is built on a clean decoupling of concerns, organized into three primary architectural

tiers:

•

MCP Host: The overarching application that the user interacts with (e.g., an AI-powered IDE or desktop

assistant). The host manages security boundaries, user approval prompts, and UI rendering.

•

MCP Client: A component embedded within the host that establishes and maintains a direct session with

an MCP server, handling the serialization and routing of messages.

•

MCP Server:  A lightweight, specialized program whose sole responsibility is to expose specific data

contexts and execution primitives according to the MCP specification.

3. Core Capabilities Exposed by MCP Servers

MCP servers expose three fundamental primitives that allow LLMs to transcend static pre-training data:

•

Resources   (Data   Ingestion):  Readable   data   contexts   addressed   via   standard   URIs   (e.g.,   database

schemas or file contents) with explicit MIME types.

•

Tools (Action Execution): Executable functions that expose rigid JSON schemas, allowing the AI to take

action, write data, or run commands.

•

Prompts (Workflow Templates):  Pre-defined templates and interactive workflows supplied by servers

to guide user interactions.

4. Security and Ecosystem Impact

As AI agents gain autonomous capabilities, security is maintained through strict user consent controls, local

sandboxing via STDIO transport, and open-source standardization that enables a rich, modular library of

community-built servers.

