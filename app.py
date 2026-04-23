import base64
from pathlib import Path
import gradio as gr
from util import css, js, Color
import pandas as pd
from trading_floor import names, lastnames, short_model_names
import plotly.express as px
from accounts import Account
from database import read_log

mapper = {
    "trace": Color.WHITE,
    "agent": Color.CYAN,
    "function": Color.GREEN,
    "generation": Color.YELLOW,
    "response": Color.MAGENTA,
    "account": Color.RED,
}

_ACCENT = ["#22d3ee", "#a78bfa", "#34d399", "#fb923c"]


class Trader:
    def __init__(self, name: str, lastname: str, model_name: str, accent_index: int = 0):
        self.name = name
        self.lastname = lastname
        self.model_name = model_name
        self.accent = _ACCENT[accent_index % len(_ACCENT)]
        self.account = Account.get(name)

    def reload(self):
        self.account = Account.get(self.name)

    def get_title(self) -> str:
        initial = self.name[:1].upper()
        return f"""
<div class="trader-head">
  <div style="display:flex;align-items:center;gap:12px;margin-bottom:4px;">
    <div style="width:44px;height:44px;border-radius:12px;background:{self.accent}22;border:1px solid {self.accent}55;
                display:flex;align-items:center;justify-content:center;font-weight:800;font-size:1.1rem;color:{self.accent};">{initial}</div>
    <div style="flex:1;min-width:0;">
      <div style="font-size:1.35rem;font-weight:700;color:#f1f5f9;letter-spacing:-0.02em;line-height:1.15;">{self.name}</div>
      <div style="font-size:0.8rem;color:#94a3b8;margin-top:2px;">{self.lastname}</div>
    </div>
    <div style="font-size:0.68rem;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;padding:6px 10px;border-radius:999px;
                background:rgba(15,23,42,0.85);border:1px solid {self.accent}44;color:{self.accent};white-space:nowrap;">{self.model_name}</div>
  </div>
</div>
""".strip()

    def get_portfolio_value_df(self) -> pd.DataFrame:
        df = pd.DataFrame(self.account.portfolio_value_time_series, columns=["datetime", "value"])
        df["datetime"] = pd.to_datetime(df["datetime"])
        return df

    def get_portfolio_value_chart(self):
        df = self.get_portfolio_value_df()
        if df.empty:
            v = self.account.calculate_portfolio_value() or 0.0
            df = pd.DataFrame({"datetime": [pd.Timestamp.now()], "value": [v]})
        fig = px.line(df, x="datetime", y="value")
        fig.update_traces(
            line=dict(color=self.accent, width=2.8),
            fill="tozeroy",
            fillcolor=self._hex_to_rgba(self.accent, 0.16),
        )
        fig.update_layout(
            template="plotly_dark",
            height=260,
            margin=dict(l=8, r=8, t=28, b=8),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15,23,42,0.45)",
            font=dict(family="ui-sans-serif, system-ui, sans-serif", size=11, color="#94a3b8"),
            showlegend=False,
            title=dict(text="Portfolio value", font=dict(size=12, color="#64748b"), x=0, xanchor="left"),
        )
        fig.update_xaxes(
            gridcolor="rgba(71,85,105,0.35)",
            zeroline=False,
            tickformat="%m/%d",
            tickangle=0,
            tickfont=dict(size=10),
        )
        fig.update_yaxes(
            gridcolor="rgba(71,85,105,0.25)",
            zeroline=False,
            tickfont=dict(size=10),
            tickformat=",.0f",
        )
        return fig

    @staticmethod
    def _hex_to_rgba(hex_color: str, alpha: float) -> str:
        h = hex_color.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return f"rgba({r},{g},{b},{alpha})"

    def get_holdings_df(self) -> pd.DataFrame:
        holdings = self.account.get_holdings()
        if not holdings:
            return pd.DataFrame(columns=["Symbol", "Quantity"])

        return pd.DataFrame(
            [{"Symbol": symbol, "Quantity": quantity} for symbol, quantity in holdings.items()]
        )

    def get_transactions_df(self) -> pd.DataFrame:
        transactions = self.account.list_transactions()
        if not transactions:
            return pd.DataFrame(columns=["Timestamp", "Symbol", "Quantity", "Price", "Rationale"])

        return pd.DataFrame(transactions)

    def get_portfolio_value(self) -> str:
        portfolio_value = self.account.calculate_portfolio_value() or 0.0
        pnl = self.account.calculate_profit_loss(portfolio_value) or 0.0
        pos = pnl >= 0
        tone = "#34d399" if pos else "#fb7185"
        tone_bg = "rgba(52, 211, 153, 0.12)" if pos else "rgba(251, 113, 133, 0.12)"
        arrow = "↑" if pos else "↓"
        return f"""
<div class="pnl-strip" style="background:{tone_bg};border:1px solid {self._hex_to_rgba(tone, 0.35)};padding:14px 16px;">
  <div style="display:flex;align-items:baseline;justify-content:space-between;gap:12px;flex-wrap:wrap;">
    <div>
      <div style="font-size:0.7rem;font-weight:600;text-transform:uppercase;letter-spacing:0.1em;color:#64748b;margin-bottom:4px;">Net worth</div>
      <div style="font-size:1.85rem;font-weight:800;color:#f8fafc;letter-spacing:-0.03em;">${portfolio_value:,.0f}</div>
    </div>
    <div style="text-align:right;">
      <div style="font-size:0.7rem;font-weight:600;text-transform:uppercase;letter-spacing:0.1em;color:#64748b;margin-bottom:4px;">Unrealized P&amp;L</div>
      <div style="font-size:1.25rem;font-weight:700;color:{tone};">{arrow} ${abs(pnl):,.0f}</div>
    </div>
  </div>
</div>
""".strip()

    def get_logs(self, previous=None) -> str:
        logs = read_log(self.name, last_n=16)
        lines = []
        for log in logs:
            timestamp, typ, message = log
            color = mapper.get(typ, Color.WHITE).value
            safe_msg = (
                message.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
            )
            lines.append(
                f'<div style="margin:3px 0;padding:4px 0;border-bottom:1px solid rgba(51,65,85,0.35);">'
                f'<span style="color:#475569;font-size:0.68rem;">{timestamp}</span> '
                f'<span style="color:#64748b;font-size:0.68rem;font-weight:600;">[{typ}]</span><br/>'
                f'<span style="color:{color};font-size:0.74rem;">{safe_msg}</span></div>'
            )
        inner = "".join(lines) if lines else '<div style="color:#64748b;padding:8px;">No activity yet.</div>'
        response = f'<div class="log-panel" style="max-height:240px;overflow-y:auto;">{inner}</div>'
        if response != previous:
            return response
        return gr.update()


class TraderView:
    def __init__(self, trader: Trader):
        self.trader = trader
        self.portfolio_value = None
        self.chart = None
        self.holdings_table = None
        self.transactions_table = None

    def make_ui(self):
        with gr.Column(elem_classes=["trader-card"], scale=1, min_width=280):
            gr.HTML(self.trader.get_title())
            with gr.Row():
                self.portfolio_value = gr.HTML(self.trader.get_portfolio_value)
            with gr.Row(elem_classes=["plot-wrap"]):
                self.chart = gr.Plot(
                    self.trader.get_portfolio_value_chart,
                    container=True,
                    show_label=False,
                )
            gr.HTML('<div class="section-label">Activity log</div>')
            with gr.Row(variant="panel"):
                self.log = gr.HTML(self.trader.get_logs)
            gr.HTML('<div class="section-label">Holdings</div>')
            with gr.Row():
                self.holdings_table = gr.Dataframe(
                    value=self.trader.get_holdings_df,
                    label="Holdings",
                    headers=["Symbol", "Quantity"],
                    row_count=(5, "dynamic"),
                    col_count=2,
                    max_height=220,
                    elem_classes=["dataframe-fix-small"],
                    interactive=False,
                )
            gr.HTML('<div class="section-label">Recent transactions</div>')
            with gr.Row():
                self.transactions_table = gr.Dataframe(
                    value=self.trader.get_transactions_df,
                    label="Recent Transactions",
                    headers=["Timestamp", "Symbol", "Quantity", "Price", "Rationale"],
                    row_count=(5, "dynamic"),
                    col_count=5,
                    max_height=240,
                    elem_classes=["dataframe-fix"],
                    interactive=False,
                )

        timer = gr.Timer(value=120)
        timer.tick(
            fn=self.refresh,
            inputs=[],
            outputs=[
                self.portfolio_value,
                self.chart,
                self.holdings_table,
                self.transactions_table,
            ],
            show_progress="hidden",
            queue=False,
        )
        log_timer = gr.Timer(value=0.5)
        log_timer.tick(
            fn=self.trader.get_logs,
            inputs=[self.log],
            outputs=[self.log],
            show_progress="hidden",
            queue=False,
        )

    def refresh(self):
        self.trader.reload()
        return (
            self.trader.get_portfolio_value(),
            self.trader.get_portfolio_value_chart(),
            self.trader.get_holdings_df(),
            self.trader.get_transactions_df(),
        )


def _build_background_css() -> str:
    image_path = Path(__file__).with_name("landing-img.webp")
    if not image_path.exists():
        return css

    encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
    return css + f"""
.gradio-container {{
  background-image:
    linear-gradient(135deg, rgba(2, 6, 23, 0.86) 0%, rgba(15, 23, 42, 0.82) 45%, rgba(2, 6, 23, 0.9) 100%),
    url('data:image/webp;base64,{encoded}') !important;
  background-size: cover !important;
  background-position: center center !important;
  background-repeat: no-repeat !important;
  background-attachment: fixed !important;
}}
"""


def create_ui():
    traders = [
        Trader(trader_name, lastname, model_name, accent_index=i)
        for i, (trader_name, lastname, model_name) in enumerate(zip(names, lastnames, short_model_names))
    ]
    trader_views = [TraderView(trader) for trader in traders]

    theme = gr.themes.Soft(primary_hue="cyan", secondary_hue="indigo", neutral_hue="slate")

    with gr.Blocks(
        title="Trading floor",
        css=_build_background_css(),
        js=js,
        theme=theme,
        fill_width=True,
    ) as ui:
        gr.HTML(
            """
<div class="floor-hero">
  <h1>Autonomous trading floor</h1>
  <p>Live portfolio, MCP traces, and execution log — fed from your local <code style="background:rgba(0,0,0,0.25);padding:2px 8px;border-radius:6px;">accounts.db</code>.</p>
</div>
            """.strip()
        )
        with gr.Accordion("How to run agents", open=False):
            gr.Markdown(
                """
- **This tab** only **displays** data. It does not call OpenAI by itself.
- **Trading loop** (OpenAI + MCP): in another terminal run `uv run trading_floor.py` from this folder (`OPENAI_API_KEY` in `.env`).
- First cycle runs **immediately**, then every **`RUN_EVERY_N_MINUTES`** (see `.env`).
- Dashboard URL: **http://127.0.0.1:7860/**
                """.strip()
            )
        with gr.Row(equal_height=True):
            for trader_view in trader_views:
                trader_view.make_ui()

    return ui


if __name__ == "__main__":
    ui = create_ui()
    print("\n  Dashboard: http://127.0.0.1:7860/\n  Traders:   run in another terminal: uv run trading_floor.py\n")
    ui.launch(inbrowser=True, server_name="127.0.0.1", server_port=7860)
