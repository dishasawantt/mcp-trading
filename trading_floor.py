from traders import Trader
from typing import List
import asyncio
from tracers import LogTracer
from agents import add_trace_processor
from market import is_market_open
from dotenv import load_dotenv
import os

load_dotenv(override=True)

RUN_EVERY_N_MINUTES = int(os.getenv("RUN_EVERY_N_MINUTES", "60"))
RUN_EVEN_WHEN_MARKET_IS_CLOSED = (
    os.getenv("RUN_EVEN_WHEN_MARKET_IS_CLOSED", "true").strip().lower() == "true"
)
USE_MANY_MODELS = os.getenv("USE_MANY_MODELS", "false").strip().lower() == "true"

names = ["Arjun", "Vikram", "Rohan", "Kavya"]
lastnames = ["Patience", "Bold", "Systematic", "Crypto"]

if USE_MANY_MODELS:
    model_names = [
        "gpt-4.1-mini",
        "deepseek-chat",
        "gemini-2.5-flash-preview-04-17",
        "grok-3-mini-beta",
    ]
    short_model_names = ["GPT 4.1 Mini", "DeepSeek V3", "Gemini 2.5 Flash", "Grok 3 Mini"]
else:
    model_names = ["gpt-4o-mini"] * 4
    short_model_names = ["GPT 4o mini"] * 4


def create_traders() -> List[Trader]:
    traders = []
    for name, lastname, model_name in zip(names, lastnames, model_names):
        traders.append(Trader(name, lastname, model_name))
    return traders


async def run_every_n_minutes():
    add_trace_processor(LogTracer())
    traders = create_traders()
    print(
        f"RUN_EVEN_WHEN_MARKET_IS_CLOSED={RUN_EVEN_WHEN_MARKET_IS_CLOSED} "
        f"(set false in .env to skip runs when US market is closed and Polygon reports closed)"
    )
    while True:
        if RUN_EVEN_WHEN_MARKET_IS_CLOSED or is_market_open():
            print(f"Running {len(traders)} traders sequentially (avoids MCP / uvx stampede)…")
            for trader in traders:
                await trader.run()
            print(f"Cycle done. Sleeping {RUN_EVERY_N_MINUTES} min.")
        else:
            print("Market is closed, skipping run (set RUN_EVEN_WHEN_MARKET_IS_CLOSED=true to run anyway)")
        await asyncio.sleep(RUN_EVERY_N_MINUTES * 60)


if __name__ == "__main__":
    print(
        f"Trading floor: every {RUN_EVERY_N_MINUTES} min, "
        f"first cycle starts immediately. Dashboard: http://127.0.0.1:7860/"
    )
    asyncio.run(run_every_n_minutes())
