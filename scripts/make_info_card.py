"""
Build a neofetch-style info card SVG (Andrew6rant style) to sit to the RIGHT of
the ASCII portrait: colored key/value rows for work experience, tech stack, and
highlights -- NOT GitHub stats (the contribution graph covers those).

Static content, hand-authored below. Lines fade/slide in on a short stagger so
it feels like the panel is printing alongside the portrait. STATIC=1 emits the
frozen state for Quick Look previews.
"""
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "info-card.svg")
STATIC = bool(os.environ.get("STATIC"))

W, H = 480, 378
PAD = 20
TITLEBAR_H = 30
KEY_X = PAD
VAL_X = PAD + 92
LINE_H = 16

FONT_HOST = 11
FONT_KV = 9.6
FONT_SEC = 9.6
FONT_BUL = 9.2

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
MUTED = "#7d8590"
INK = "#c9d1d9"
KEY = "#ffa657"      # orange keys (matches Andrew)
SECTION = "#58a6ff"  # blue section headers
GREEN = "#3fb950"
ACCENT = "#22d3ee"

# ===========================================================================
#  EDIT THIS  -- your info panel. It re-lays-out automatically; if it gets too
#  tall for the card, bump H above (and the width= in your profile README).
#  The username in the header is HOST below.
#
#  row types:
#    ("host",)              -> "you@github" header + rule
#    ("kv", key, value)     -> orange key + light value
#    ("sec", title)         -> blue "— title —" section rule
#    ("bul", text)          -> green dot + light bullet
#    ("gap",)               -> a little vertical space
# ===========================================================================
HOST = "rishi"   # shown as  rishi@github  in the header

ROWS = [
    ("host",),
    ("kv", "Now", "CTO @ dBee (Aug 2025-Present)"),
    ("kv", "Prev", "SWE Backend @ Oriserve.ai"),
    ("kv", "Prev", "Software Engineer @ AST Consulting"),
    ("gap",),
    ("sec", "dBee -- CTO"),
    ("bul", "Real-time Voice AI (LLM/STT/TTS), multi-agent RAG pipelines, K8s/KEDA scale"),
    ("gap",),
    ("sec", "Oriserve.ai -- Backend"),
    ("bul", "450K+ daily calls · latency 3.5s→1.2s · SIP cost -98% ($0.22→$0.004/min)"),
    ("gap",),
    ("sec", "AST Consulting -- SWE"),
    ("bul", "Ranking engine, 21M MAU, sub-100ms p99 · SSO (OIDC/JWKS) · Razorpay"),
    ("gap",),
    ("sec", "Stack"),
    ("kv", "Languages", "JS/TS, Python, Java, C/C++, Go"),
    ("kv", "AI/Agents", "RAG, LLMs, STT/TTS, eval, vector DB"),
    ("kv", "Backend", "Node, FastAPI, Spring Boot, NestJS"),
    ("kv", "Data", "Mongo, Postgres, Redis, Kafka, ES"),
    ("kv", "Frontend", "React, Next.js, LiveKit, WebRTC"),
    ("kv", "Platform", "Docker, AWS, GCP, K8s, KEDA"),
]


def esc(s):
    return html.escape(s)


def rise(inner, i):
    """fade + slight upward slide, staggered by row index; freezes visible."""
    if STATIC:
        return f"<g>{inner}</g>"
    delay = 0.15 + i * 0.06
    return (f'<g opacity="0" transform="translate(0,5)">{inner}'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.4s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="0 5" to="0 0" '
            f'begin="{delay:.2f}s" dur="0.4s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/></g>')


parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    '<defs>'
    f'<linearGradient id="ibg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient></defs>',
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#ibg)"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]
for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')
parts.append(f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" '
             f'text-anchor="middle">{esc(HOST)}@github: ~$ neofetch</text>')

y = TITLEBAR_H + 26
for i, row in enumerate(ROWS):
    kind = row[0]
    if kind == "gap":
        y += LINE_H * 0.5
        continue
    if kind == "host":
        host = esc(HOST)
        rule_x = KEY_X + (len(HOST) + 7) * 6.3 + 8
        inner = (f'<text x="{KEY_X}" y="{y:.1f}" font-size="{FONT_HOST}" font-weight="700">'
                 f'<tspan fill="{GREEN}">{host}</tspan><tspan fill="{MUTED}">@</tspan>'
                 f'<tspan fill="{ACCENT}">github</tspan></text>'
                 f'<line x1="{rule_x}" y1="{y-4:.1f}" x2="{W-PAD}" y2="{y-4:.1f}" '
                 f'stroke="{FRAME}" stroke-opacity="0.8"/>')
    elif kind == "sec":
        title = esc(row[1])
        inner = (f'<text x="{KEY_X}" y="{y:.1f}" fill="{SECTION}" font-size="{FONT_SEC}" font-weight="700">'
                 f'&#8212; {title}</text>'
                 f'<line x1="{KEY_X + 10 + len(row[1])*6.1}" y1="{y-4:.1f}" x2="{W-PAD}" y2="{y-4:.1f}" '
                 f'stroke="{FRAME}" stroke-opacity="0.8"/>')
    elif kind == "kv":
        key, val = esc(row[1]), esc(row[2])
        inner = (f'<text x="{KEY_X}" y="{y:.1f}" fill="{KEY}" font-size="{FONT_KV}" font-weight="700">{key}</text>'
                 f'<text x="{VAL_X}" y="{y:.1f}" fill="{INK}" font-size="{FONT_KV}">{val}</text>')
    elif kind == "bul":
        txt = esc(row[1])
        inner = (f'<circle cx="{KEY_X+3}" cy="{y-4:.1f}" r="2.2" fill="{GREEN}"/>'
                 f'<text x="{KEY_X+11}" y="{y:.1f}" fill="{INK}" font-size="{FONT_BUL}">{txt}</text>')
    else:
        continue
    parts.append(rise(inner, i))
    y += LINE_H

parts.append("</svg>")
svg = "".join(parts)
with open(OUT, "w") as f:
    f.write(svg)
print("wrote", OUT, len(svg), "bytes;", W, "x", H, "content_bottom", round(y))
