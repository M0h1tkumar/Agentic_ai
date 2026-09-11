# Currency Converter Agent

This document details the specification, MCP server integration, test issue, and output verification for the **Currency Converter Agent**.

---

## 🎯 1. Objective

To provide an autonomous agent capable of retrieving real-time foreign exchange rates, performing multi-currency conversions, and calculating cross-currency historical conversion trends.

---

## ⚡ 2. MCP Server

- **MCP Server Package**: `@mcp-tools/currency-converter-server`
- **Transport**: STDIO (`npx -y @mcp-tools/currency-converter-server`)
- **Exposed Tools**: `convert_currency`, `get_exchange_rates`, `get_historical_rate`

---

## 🤖 3. Agent Responsibility

- **Agent ID**: `currency-converter-agent-01`
- **Primary Function**: Parses financial queries containing amounts and currency codes (e.g., USD, EUR, JPY, INR), invokes conversion tools, applies real-time spreads, and formats structured conversion tables.

---

## 🧪 4. Test Issue / Prompt

> **Test Issue**: *"Convert 2,500 USD into EUR, GBP, JPY, and INR. Provide the current exchange rate applied for each currency."*

---

## 📤 5. Expected Output

```markdown
### 💱 Foreign Exchange Conversion Report

**Base Amount**: $2,500.00 USD  
**Timestamp**: 2026-08-11 14:30:00 UTC

| Target Currency | Code | Exchange Rate (1 USD) | Converted Amount |
| :--- | :--- | :--- | :--- |
| **Euro** | `EUR` | 0.9152 | €2,288.00 |
| **British Pound** | `GBP` | 0.7845 | £1,961.25 |
| **Japanese Yen** | `JPY` | 147.20 | ¥368,000.00 |
| **Indian Rupee** | `INR` | 83.45 | ₹208,625.00 |

*Data sourced via Currency Converter MCP Server.*
```
