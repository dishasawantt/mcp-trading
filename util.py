from enum import Enum

css = """
:root {
  --floor-bg: #0c1222;
  --card-bg: linear-gradient(165deg, rgba(30, 41, 59, 0.92) 0%, rgba(15, 23, 42, 0.97) 55%, rgba(12, 18, 34, 1) 100%);
  --card-border: rgba(100, 116, 139, 0.22);
  --card-shadow: 0 18px 48px rgba(0, 0, 0, 0.35);
  --text: #e2e8f0;
  --muted: #94a3b8;
  --accent: #22d3ee;
  --accent-dim: rgba(34, 211, 238, 0.12);
}

.gradio-container {
  background-image:
    linear-gradient(135deg, rgba(2, 6, 23, 0.9) 0%, rgba(15, 23, 42, 0.84) 45%, rgba(2, 6, 23, 0.92) 100%),
    radial-gradient(1200px 600px at 10% -10%, rgba(34, 211, 238, 0.08), transparent 55%),
    radial-gradient(900px 500px at 100% 0%, rgba(99, 102, 241, 0.07), transparent 50%),
    var(--floor-bg) !important;
  background-size: cover !important;
  background-position: center center !important;
  background-repeat: no-repeat !important;
  background-attachment: fixed !important;
  min-height: 100vh;
}

main.contain {
  max-width: 1880px !important;
  margin: 0 auto !important;
  padding: 0.75rem 1rem 2rem !important;
}

footer { display: none !important; }

.floor-hero {
  border-radius: 20px;
  padding: 1.35rem 1.75rem;
  margin-bottom: 1.25rem;
  background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 27, 75, 0.55) 45%, rgba(15, 23, 42, 0.92) 100%);
  border: 1px solid rgba(148, 163, 184, 0.18);
  box-shadow: var(--card-shadow);
}

.floor-hero h1 {
  margin: 0 0 0.35rem 0;
  font-size: 1.65rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  background: linear-gradient(90deg, #f1f5f9 0%, #22d3ee 55%, #a5b4fc 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.floor-hero p {
  margin: 0;
  color: var(--muted);
  font-size: 0.95rem;
  line-height: 1.5;
}

.trader-card {
  background: var(--card-bg) !important;
  border: 1px solid var(--card-border) !important;
  border-radius: 18px !important;
  padding: 1rem 1rem 1.1rem !important;
  box-shadow: var(--card-shadow) !important;
  min-width: 0 !important;
}

.trader-card .trader-head {
  margin-bottom: 0.85rem;
}

.trader-card .pnl-strip {
  border-radius: 14px !important;
  overflow: hidden;
  margin-bottom: 0.65rem !important;
}

.trader-card .plot-wrap {
  border-radius: 14px;
  overflow: hidden;
  border: 1px solid rgba(71, 85, 105, 0.35);
  background: rgba(15, 23, 42, 0.5);
  margin-bottom: 0.65rem !important;
}

.trader-card .plot-wrap > div {
  border-radius: 14px !important;
}

.trader-card .log-panel {
  border-radius: 12px !important;
  border: 1px solid rgba(51, 65, 85, 0.5) !important;
  background: rgba(2, 6, 23, 0.55) !important;
  font-family: ui-monospace, "Cascadia Code", "SF Mono", Menlo, monospace !important;
  font-size: 0.72rem !important;
  line-height: 1.5 !important;
  padding: 0.65rem 0.75rem !important;
  margin-bottom: 0.65rem !important;
}

.trader-card .section-label {
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: #64748b;
  margin: 0.5rem 0 0.35rem 0;
}

.trader-card .dataframe-fix-small .table-wrap,
.trader-card .dataframe-fix .table-wrap {
  min-height: 120px;
  max-height: 200px;
  border-radius: 10px;
  border: 1px solid rgba(51, 65, 85, 0.4);
  overflow: auto;
}

.trader-card table th {
  font-size: 0.7rem !important;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: #94a3b8 !important;
}

.trader-card .label-wrap span {
  color: #cbd5e1 !important;
  font-weight: 600 !important;
  font-size: 0.78rem !important;
}

.trader-card .accordion {
  border-radius: 14px !important;
  border: 1px solid rgba(71, 85, 105, 0.35) !important;
  background: rgba(15, 23, 42, 0.4) !important;
  margin-bottom: 1rem !important;
}

.trader-card .accordion summary {
  font-weight: 600 !important;
  color: #cbd5e1 !important;
}
"""


js = """
function refresh() {
    const url = new URL(window.location);
    if (url.searchParams.get('__theme') !== 'dark') {
        url.searchParams.set('__theme', 'dark');
        window.location.href = url.href;
    }
}
"""


class Color(Enum):
    RED = "#fb7185"
    GREEN = "#4ade80"
    YELLOW = "#fbbf24"
    BLUE = "#60a5fa"
    MAGENTA = "#c084fc"
    CYAN = "#22d3ee"
    WHITE = "#cbd5e1"
