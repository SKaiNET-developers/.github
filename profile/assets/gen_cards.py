#!/usr/bin/env python3
"""Generate the repo-card SVGs used in profile/README.md.

Each entry in CARDS produces cards/<slug>-light.svg and cards/<slug>-dark.svg;
the README links each card image to its repository. To add a repo: append an
entry to CARDS, run `python3 gen_cards.py`, and add a linked <picture> block
for the new slug to profile/README.md.
"""
import html
import os
import textwrap

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cards")
os.makedirs(OUT, exist_ok=True)

FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
EMOJI_FONT = "'Apple Color Emoji', 'Segoe UI Emoji', 'Noto Color Emoji', sans-serif"

THEMES = {
    "light": {"bg": "#ffffff", "border": "#d0d7de", "title": "#1f2328",
              "tag": "#656d76", "desc": "#424a53", "arrow": "#656d76"},
    "dark":  {"bg": "#0d1117", "border": "#30363d", "title": "#e6edf3",
              "tag": "#8b949e", "desc": "#c9d1d9", "arrow": "#8b949e"},
}

W, H = 400, 190

CARDS = [
    # slug, emoji, name, tagline, description
    ("skainet", "🧠", "SKaiNET", "Core AI engine",
     "Tensors, neural networks, compilation and native execution."),
    ("transformers", "💬", "SKaiNET-transformers", "Language models",
     "Multi-model LLM inference and agentic tool calling for JVM, Android and Kotlin/Native."),
    ("audio", "🎙️", "SKaiNET-audio", "Audio models",
     "Audio support for the SKaiNET engine."),
    ("rag", "🔎", "SKaiNET-rag", "Retrieval-augmented generation",
     "RAG building blocks on top of SKaiNET."),
    ("notebook", "📓", "skainet-notebook", "Experimentation",
     "Interactive learning with Kotlin and Jupyter."),
    ("examples", "📱", "SKaiNET-examples", "Practical applications",
     "Examples of integrating AI into software."),
    ("mikrograd", "🎓", "miKrograd", "Education",
     "A tiny autograd engine and neural net library with a PyTorch-like API, in Kotlin."),
    ("coding-skills", "🤖", "SKaiNET-coding-skills", "AI agent skills",
     "Skills that teach AI coding agents how to work with SKaiNET."),
    ("cartridge", "📦", "SKaiNET-cartridge", "Model distribution",
     "Packaging specifications for AI model cartridges."),
    ("embedded", "⚙️", "SKaiNET-embedded", "Embedded AI",
     "Running SKaiNET models on embedded targets via MLIR and IREE."),
    ("research", "🔬", "SKaiNET-research", "Research",
     "Experimental implementations of papers with SKaiNET."),
    ("labs", "🌱", "SKaiNET-labs", "Incubator",
     "Early-stage SKaiNET projects and ideas."),
    ("federated-learning", "🤝", "federated-learning", "Distributed training",
     "A SKaiNET module adding federated learning capability."),
    ("gradienttracer", "🧪", "gradienttracer", "Numerical validation",
     "PyTorch-generated reference data that keeps SKaiNET's math honest."),
]

TPL = """<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect x="1" y="1" width="{iw}" height="{ih}" rx="14" fill="{bg}" stroke="{border}" stroke-width="1.5"/>
  <text x="28" y="52" font-size="28" font-family="{emoji_font}">{emoji}</text>
  <text x="28" y="92" font-family="{font}" font-size="19" font-weight="700" fill="{title_c}">{name} <tspan fill="{arrow}" font-weight="400">↗</tspan></text>
  <text x="28" y="116" font-family="{font}" font-size="14" fill="{tag_c}">{tagline}</text>
  <text x="28" y="142" font-family="{font}" font-size="15" fill="{desc_c}">{desc_tspans}</text>
</svg>
"""


def esc(s: str) -> str:
    return html.escape(s, quote=False)


for slug, emoji, name, tagline, desc in CARDS:
    lines = textwrap.wrap(desc, width=46, max_lines=3)
    tspans = esc(lines[0])
    for line in lines[1:]:
        tspans += f'<tspan x="28" dy="21">{esc(line)}</tspan>'
    for theme, c in THEMES.items():
        svg = TPL.format(
            W=W, H=H, iw=W - 2, ih=H - 2,
            bg=c["bg"], border=c["border"], title_c=c["title"],
            tag_c=c["tag"], desc_c=c["desc"], arrow=c["arrow"],
            font=FONT, emoji_font=EMOJI_FONT,
            emoji=emoji, name=esc(name), tagline=esc(tagline),
            desc_tspans=tspans,
        )
        path = os.path.join(OUT, f"{slug}-{theme}.svg")
        with open(path, "w") as f:
            f.write(svg)
        print(path)
