#!/usr/bin/env node
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

// Bhubaneswar, Odisha, India
const LATITUDE = 20.2961;
const LONGITUDE = 85.8245;

const WMO_CODES = {
  0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
  45: "Fog", 48: "Depositing rime fog",
  51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
  61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
  71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
  80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
  95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail",
};

const server = new McpServer({ name: "bhubaneswar-weather", version: "1.0.0" });

server.registerTool(
  "get_bhubaneswar_weather",
  {
    title: "Get Bhubaneswar weather",
    description:
      "Fetch current weather conditions for Bhubaneswar, Odisha, India, and optionally a short daily forecast, via Open-Meteo (no API key required).",
    inputSchema: {
      forecastDays: z
        .number()
        .int()
        .min(0)
        .max(7)
        .default(0)
        .describe("Number of additional forecast days to include (0-7). 0 returns only current conditions."),
    },
  },
  async ({ forecastDays = 0 }) => {
    const url = new URL("https://api.open-meteo.com/v1/forecast");
    url.searchParams.set("latitude", LATITUDE);
    url.searchParams.set("longitude", LONGITUDE);
    url.searchParams.set("current_weather", "true");
    url.searchParams.set("timezone", "Asia/Kolkata");
    if (forecastDays > 0) {
      url.searchParams.set("daily", "temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode");
      url.searchParams.set("forecast_days", String(forecastDays));
    }

    const res = await fetch(url);
    if (!res.ok) {
      throw new Error(`Open-Meteo request failed: ${res.status} ${await res.text()}`);
    }
    const data = await res.json();

    const cw = data.current_weather;
    const lines = [
      `Bhubaneswar current weather (as of ${cw.time}):`,
      `  Temperature: ${cw.temperature}°C`,
      `  Wind: ${cw.windspeed} km/h, direction ${cw.winddirection}°`,
      `  Condition: ${WMO_CODES[cw.weathercode] || `code ${cw.weathercode}`}`,
    ];

    if (data.daily) {
      lines.push("", "Forecast:");
      data.daily.time.forEach((date, i) => {
        lines.push(
          `  ${date}: ${WMO_CODES[data.daily.weathercode[i]] || "?"}, ` +
            `${data.daily.temperature_2m_min[i]}–${data.daily.temperature_2m_max[i]}°C, ` +
            `precip ${data.daily.precipitation_sum[i]}mm`
        );
      });
    }

    return { content: [{ type: "text", text: lines.join("\n") }] };
  }
);

const transport = new StdioServerTransport();
await server.connect(transport);
