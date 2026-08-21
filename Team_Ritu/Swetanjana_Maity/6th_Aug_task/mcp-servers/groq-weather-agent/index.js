#!/usr/bin/env node
import "dotenv/config";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
import Groq from "groq-sdk";
import readline from "node:readline/promises";
import { stdin, stdout } from "node:process";
import { fileURLToPath } from "node:url";
import path from "node:path";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const WEATHER_SERVER_PATH = path.resolve(__dirname, "../bhubaneswar-weather/index.js");
const GROQ_MODEL = process.env.GROQ_MODEL || "llama-3.3-70b-versatile";

if (!process.env.GROQ_API_KEY) {
  console.error("Missing GROQ_API_KEY. Set it in your environment or in a .env file.");
  process.exit(1);
}

const groq = new Groq({ apiKey: process.env.GROQ_API_KEY });

const transport = new StdioClientTransport({
  command: "node",
  args: [WEATHER_SERVER_PATH],
});

const mcpClient = new Client({ name: "groq-weather-agent", version: "1.0.0" });
await mcpClient.connect(transport);

const { tools: mcpTools } = await mcpClient.listTools();

const groqTools = mcpTools.map((tool) => ({
  type: "function",
  function: {
    name: tool.name,
    description: tool.description,
    parameters: tool.inputSchema,
  },
}));

async function callMcpTool(name, args) {
  const result = await mcpClient.callTool({ name, arguments: args });
  return result.content
    .filter((c) => c.type === "text")
    .map((c) => c.text)
    .join("\n");
}

async function chat(messages) {
  let response = await groq.chat.completions.create({
    model: GROQ_MODEL,
    messages,
    tools: groqTools,
    tool_choice: "auto",
  });
  let choice = response.choices[0];

  while (choice.finish_reason === "tool_calls") {
    messages.push(choice.message);

    for (const toolCall of choice.message.tool_calls) {
      const args = JSON.parse(toolCall.function.arguments || "{}");
      const toolResult = await callMcpTool(toolCall.function.name, args);
      messages.push({ role: "tool", tool_call_id: toolCall.id, content: toolResult });
    }

    response = await groq.chat.completions.create({
      model: GROQ_MODEL,
      messages,
      tools: groqTools,
      tool_choice: "auto",
    });
    choice = response.choices[0];
  }

  messages.push(choice.message);
  return choice.message.content;
}

const messages = [
  {
    role: "system",
    content:
      "You are a helpful weather assistant for Bhubaneswar, Odisha, India. " +
      "Use the get_bhubaneswar_weather tool whenever the user asks about current conditions or a forecast. " +
      "Answer concisely, mentioning temperature, condition, and wind when relevant.",
  },
];

const cliArgs = process.argv.slice(2);

if (cliArgs.length > 0) {
  messages.push({ role: "user", content: cliArgs.join(" ") });
  console.log(await chat(messages));
  await mcpClient.close();
  process.exit(0);
}

console.log("Groq + MCP weather agent for Bhubaneswar. Ask a question (Ctrl+C to exit).\n");
const rl = readline.createInterface({ input: stdin, output: stdout });

while (true) {
  const question = await rl.question("> ");
  if (!question.trim()) continue;
  messages.push({ role: "user", content: question });
  console.log((await chat(messages)) + "\n");
}
