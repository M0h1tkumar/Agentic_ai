# 1. 6 August --- API vs MCP

## What is an API?

An **API (Application Programming Interface)** is a contract that lets
one software system communicate with another.

Example:

``` text
Application
    |
    | GET /weather?city=Bhubaneswar
    v
Weather API
    |
    v
JSON response
```

A conventional API requires the developer to know the endpoint,
authentication, HTTP method, parameters, request/response format,
errors, and rate limits.

## What is MCP?

**MCP (Model Context Protocol)** is a standardized protocol for
connecting AI applications to external tools, resources, and prompts.

MCP defines three core primitives:

  -----------------------------------------------------------------------
  Primitive               Purpose                 Example
  ----------------------- ----------------------- -----------------------
  Tools                   Actions an AI           Search, database query,
                          application can invoke  file operation

  Resources               Context/data exposed to Documents, files,
                          the AI application      database records

  Prompts                 Reusable interaction    Code review or research
                          templates               prompt
  -----------------------------------------------------------------------

MCP architecture:
https://modelcontextprotocol.io/docs/learn/architecture

## API vs MCP

  ----------------------------------------------------------------------------------
  Feature                 Traditional API              MCP
  ----------------------- ---------------------------- -----------------------------
  Main purpose            Application-to-application   AI
                          communication                application-to-tool/context
                                                       communication

  Interface               Usually custom               Standardized MCP protocol
                          REST/GraphQL/RPC             

  Tool discovery          Usually custom/manual        Standardized discovery

  Context handling        Application-specific         Resources are first-class

  Prompt templates        Usually separate             Prompts are first-class

  AI-agent orientation    Not necessarily              Designed for AI applications

  Reuse across AI clients Requires adapters            Same MCP server can serve MCP
                                                       clients

  Best use                Direct service integration   Agent interoperability
  ----------------------------------------------------------------------------------

## Is MCP a replacement for APIs?

**No.**

MCP can sit on top of existing APIs:

``` text
AI Agent
   |
   | MCP tool call
   v
MCP Server
   |
   | HTTP request
   v
Existing API
```

So:

> **API = service interface.**\
> **MCP = standardized AI interoperability layer.**

## Drawbacks of API over MCP for agentic AI

### 1. Custom integration

With many APIs, an agent framework may need custom adapters:

``` text
Agent
 |-- GitHub adapter
 |-- Slack adapter
 |-- Jira adapter
 |-- Weather adapter
 |-- Database adapter
```

MCP provides a common protocol for compatible clients and servers.

### 2. No universal tool discovery

An API may document endpoints, but the AI client still needs integration
logic to understand which endpoint is useful and how to call it.

MCP provides standardized discovery for its primitives.

### 3. Context is not normally a first-class API concept

Traditional APIs return data. Agent systems often need:

``` text
Data + Tools + Context + Instructions
```

MCP explicitly models resources and prompts in addition to tools.

### 4. Integration duplication

Without a common protocol:

``` text
API A -> Client-specific integration
API B -> Client-specific integration
API C -> Client-specific integration
```

With MCP:

``` text
MCP Server
 |--> Client A
 |--> Client B
 |--> Client C
```

### 5. APIs can be too low-level for agents

An API might expose dozens of low-level endpoints. An MCP server can
expose higher-level agent-oriented tools such as:

``` text
search_customer()
get_customer_orders()
create_support_ticket()
```

## When an API is better

APIs are often better when:

-   a normal application directly consumes a service
-   strict deterministic contracts are needed
-   very high throughput/low overhead matters
-   the consumer is not an AI agent
-   an existing service architecture is already stable

**Conclusion:** MCP complements APIs rather than replacing them.

------------------------------------------------------------------------

# 2. MCP Server Submission

Assigned links:

-   https://mcpservers.org/
-   https://mcpmarket.com/submit

## MCP Servers submission

The submission form asks for server name, short description,
repository/documentation link, category, and contact email.

Source: https://mcpservers.org/submit

Suggested submission:

``` text
Server Name:
Bhubaneswar Weather MCP

Short Description:
An MCP server that provides weather information and forecasts for Bhubaneswar and other cities to AI agents.

Category:
Weather / Data / Utilities

Repository:
<YOUR-GITHUB-REPOSITORY>
```

## MCP Market submission

MCP Market accepts a GitHub repository or remote MCP server URL.

Source: https://mcpmarket.com/submit

Suggested information:

``` text
Name:
Bhubaneswar Weather MCP

Description:
MCP server exposing weather lookup and forecast tools for AI agents.

GitHub:
<YOUR-GITHUB-REPOSITORY>

Remote MCP:
<OPTIONAL-REMOTE-MCP-URL>
```

Do not claim a submission is complete until it has actually been
submitted and accepted.

------------------------------------------------------------------------

# 3. Bhubaneswar Weather Predictor

## Objective

Build a small ML weather predictor for Bhubaneswar.

Pipeline:

``` text
Historical Weather Data
        |
        v
     Pandas
        |
        v
Feature Engineering
        |
        v
Random Forest
        |
        v
Next-day Temperature
        |
        v
Optional MCP Tool
```

## Project structure

``` text
bhubaneswar-weather/
├── weather_predictor.py
├── requirements.txt
└── README.md
```

## requirements.txt

``` txt
pandas
numpy
requests
scikit-learn
joblib
```

## Complete predictor

``` python
import requests
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

LATITUDE = 20.2961
LONGITUDE = 85.8245


def download_weather():
    url = "https://archive-api.open-meteo.com/v1/archive"

    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "start_date": "2021-01-01",
        "end_date": "2026-08-01",
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "wind_speed_10m_max"
        ],
        "timezone": "Asia/Kolkata"
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def prepare_data(data):
    daily = data["daily"]
    df = pd.DataFrame(daily)

    df["time"] = pd.to_datetime(df["time"])

    df = df.rename(columns={
        "time": "date",
        "temperature_2m_max": "max_temp",
        "temperature_2m_min": "min_temp",
        "precipitation_sum": "rain",
        "wind_speed_10m_max": "wind"
    })

    df = df.dropna()

    df["prev_max_temp"] = df["max_temp"].shift(1)
    df["prev_min_temp"] = df["min_temp"].shift(1)
    df["prev_rain"] = df["rain"].shift(1)
    df["prev_wind"] = df["wind"].shift(1)

    df["temp_3day_avg"] = df["max_temp"].rolling(3).mean()
    df["temp_7day_avg"] = df["max_temp"].rolling(7).mean()

    df["month"] = df["date"].dt.month
    df["day_of_year"] = df["date"].dt.dayofyear

    return df.dropna()


def train_model(df):
    features = [
        "prev_max_temp",
        "prev_min_temp",
        "prev_rain",
        "prev_wind",
        "temp_3day_avg",
        "temp_7day_avg",
        "month",
        "day_of_year"
    ]

    X = df[features]
    y = df["max_temp"]

    split = int(len(df) * 0.8)

    X_train = X.iloc[:split]
    X_test = X.iloc[split:]
    y_train = y.iloc[:split]
    y_test = y.iloc[split:]

    model = RandomForestRegressor(
        n_estimators=300,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)

    print(f"Test MAE: {mae:.2f} °C")

    return model, features


def predict_next_day(df, model, features):
    latest = df.iloc[-1]

    X = pd.DataFrame([{
        "prev_max_temp": latest["max_temp"],
        "prev_min_temp": latest["min_temp"],
        "prev_rain": latest["rain"],
        "prev_wind": latest["wind"],
        "temp_3day_avg": df["max_temp"].tail(3).mean(),
        "temp_7day_avg": df["max_temp"].tail(7).mean(),
        "month": latest["month"],
        "day_of_year": latest["day_of_year"] + 1
    }])

    return model.predict(X[features])[0]


def main():
    data = download_weather()
    df = prepare_data(data)
    model, features = train_model(df)

    prediction = predict_next_day(df, model, features)

    print(
        f"Predicted next-day maximum temperature "
        f"for Bhubaneswar: {prediction:.2f} °C"
    )


if __name__ == "__main__":
    main()
```

Install and run:

``` bash
python -m venv .venv
```

Windows:

``` powershell
.venv\Scripts\activate
```

``` bash
pip install -r requirements.txt
python weather_predictor.py
```

The exact prediction changes with the historical data available from the
provider.

------------------------------------------------------------------------

# 4. Weather Predictor as an MCP Server

The official MCP Python SDK provides `FastMCP` and decorator-based
tools.

Source: https://github.com/modelcontextprotocol/python-sdk

Example:

``` python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Bhubaneswar Weather")


@mcp.tool()
def get_weather(city: str) -> str:
    """Return weather information for a city."""
    return f"Weather lookup requested for {city}"


if __name__ == "__main__":
    mcp.run()
```

A production version should validate city names, call a real weather
provider, return structured data, handle failures, rate-limit requests,
and keep secrets out of source code.
