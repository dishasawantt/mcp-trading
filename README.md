## MCP trading simulation

OpenAI Agents SDK + MCP (stdio) servers for a multi-agent trading floor UI and scheduler.

### Setup

1. Install [Python 3.12](https://www.python.org/) and [uv](https://docs.astral.sh/uv/).
2. From this directory:

```bash
uv sync
```

3. Copy `.env.example` to `.env`, then set **`OPENAI_API_KEY`** (a starter `.env` may already exist with an empty key—paste your key after the `=`).

### Environment variables

| Variable | Purpose |
|----------|---------|
| `OPENAI_API_KEY` | Trader / researcher agents (required) |
| `POLYGON_API_KEY` | Real stock prices via Polygon (optional; falls back to random prices if unset) |
| `POLYGON_PLAN` | `paid` or `realtime` for richer Polygon MCP; omit for free EOD + local `market_server.py` |
| `BRAVE_API_KEY` | Optional. Brave Search MCP is **omitted** if unset (required before: a missing key crashed MCP startup so **no OpenAI calls** ran). |
| `PUSHOVER_USER`, `PUSHOVER_TOKEN` | Push notifications from `push_server.py` |
| `DEEPSEEK_API_KEY`, `GROK_API_KEY`, `GOOGLE_API_KEY`, `OPENROUTER_API_KEY` | Only if you point traders at those models in `trading_floor.py` / env |

Optional scheduler / behavior:

| Variable | Default |
|----------|---------|
| `RUN_EVERY_N_MINUTES` | `60` (lower for testing, e.g. `3`) |
| `RUN_EVEN_WHEN_MARKET_IS_CLOSED` | `true` (set `false` to skip runs when Polygon says the US market is closed) |
| `USE_MANY_MODELS` | `false` |

Researcher MCP also uses **Node** (`npx`) for Brave Search and LibSQL memory (`./memory/{trader}.db`) per `mcp_params.py`.

### Run

You normally need **two terminals** in this folder:

1. **Dashboard** (read-only UI — charts, logs, holdings from `accounts.db`):

```bash
uv run app.py
```

Then open **http://127.0.0.1:7860/** (port matters).

2. **Trading loop** (runs the LLM + MCP agents that buy/sell and append history):

```bash
uv run trading_floor.py
```

Until (2) is running (or has run), accounts stay at the starting balance and charts look flat.

Reset trader strategies / balances (see `reset.py`):

```bash
uv run reset.py
```

### License

MIT — see `LICENSE`.
