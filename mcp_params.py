import os
from dotenv import load_dotenv
from market import is_paid_polygon, is_realtime_polygon

load_dotenv(override=True)

polygon_api_key = os.getenv("POLYGON_API_KEY")
brave_api_key = os.getenv("BRAVE_API_KEY")

# The MCP server for the Trader to read Market Data

if is_paid_polygon or is_realtime_polygon:
    market_mcp = {
        "command": "uvx",
        "args": ["--from", "git+https://github.com/polygon-io/mcp_polygon@v0.1.0", "mcp_polygon"],
        "env": {"POLYGON_API_KEY": polygon_api_key},
    }
else:
    market_mcp = {"command": "uv", "args": ["run", "market_server.py"]}


# The full set of MCP servers for the trader: Accounts, Push Notification and the Market

trader_mcp_server_params = [
    {"command": "uv", "args": ["run", "accounts_server.py"]},
    {"command": "uv", "args": ["run", "push_server.py"]},
    market_mcp,
]

# The full set of MCP servers for the researcher: Fetch, Brave Search and Memory


def researcher_mcp_server_params(name: str):
    servers: list[dict] = [
        {"command": "uvx", "args": ["mcp-server-fetch"]},
    ]
    _npm_quiet = {"NPM_CONFIG_LOGLEVEL": "silent", "NPM_CONFIG_UPDATE_NOTIFIER": "false"}

    if brave_api_key:
        servers.append(
            {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-brave-search"],
                "env": {**_npm_quiet, "BRAVE_API_KEY": brave_api_key},
            }
        )
    servers.append(
        {
            "command": "npx",
            "args": ["-y", "mcp-memory-libsql"],
            "env": {**_npm_quiet, "LIBSQL_URL": f"file:./memory/{name}.db"},
        }
    )
    return servers
