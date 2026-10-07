#!/usr/bin/env python3
"""Generate a self-hosted typewriter (typing) SVG for the GitHub profile README.

No third-party service required: the output SVG uses SMIL animations that run
when the file is embedded via <img> in a README. Committed to the repo so the
profile never depends on an external host.
"""
import os
import xml.etree.ElementTree as ET
from html import escape

# ---- layout ----
W, H = 600, 50
FONT_SIZE = 24
START_X = 12
BASELINE = 33
COLOR = "#36BCF7"
CHAR_W = 0.6 * FONT_SIZE          # approx monospace advance width
CURSOR_W = CHAR_W * 0.55

# ---- animation timings (seconds) ----
TYPE_PER_CHAR = 0.075
HOLD = 1.6
ERASE_PER_CHAR = 0.035

PHRASES = [
    "Building AI assistants for audit workflows",
    "Python / Go / Node full-stack",
    "Automating the boring stuff",
    "Audit Office @ YTG",
]


def metrics(text):
    n = len(text)
    w = max(1.0, round(n * CHAR_W, 1))
    td = max(0.4, round(n * TYPE_PER_CHAR, 2))   # type duration
    ed = max(0.3, round(n * ERASE_PER_CHAR, 2))  # erase duration
    return w, td, ed


# build per-phrase slot timeline
slots = []
t = 0.0
for text in PHRASES:
    w, td, ed = metrics(text)
    slots.append({"text": text, "w": w, "td": td, "ed": ed, "t0": round(t, 2)})
    t += td + HOLD + ed
CYCLE = round(t, 2)


def frac(x):
    return f"{x / CYCLE:.4f}"


def clip_anim(slot):
    """Return (width_values, width_keytimes, x_values, op_values, op_keytimes)."""
    w, td, ed = slot["w"], slot["td"], slot["ed"]
    t0 = slot["t0"]
    t_type_end = t0 + td
    t_hold_end = t_type_end + HOLD
    t_erase_end = t_hold_end + ed

    if t0 == 0:
        wk = [0, frac(td), frac(t_hold_end), frac(t_erase_end), 1.0]
        wv = [0, w, w, 0, 0]
        xv = [START_X, START_X + w, START_X + w, START_X, START_X]
        ok = [0, frac(t_erase_end), 1.0]
        ov = [1, 0, 0]
    else:
        wk = [0, frac(t0), frac(t_type_end), frac(t_hold_end), frac(t_erase_end), 1.0]
        wv = [0, 0, w, w, 0, 0]
        xv = [START_X, START_X, START_X + w, START_X + w, START_X, START_X]
        ok = [0, frac(t0), frac(t_erase_end), 1.0]
        ov = [0, 1, 0, 0]
    return wv, wk, xv, ov, ok


def build_svg():
    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" role="img" aria-label="Typing animation">'
    )
    parts.append(
        f'<style>'
        f'.t {{ font-family: Consolas, "Courier New", monospace; '
        f'font-size: {FONT_SIZE}px; font-weight: 600; fill: {COLOR}; }}'
        f'.c {{ fill: {COLOR}; }}'
        f'</style>'
    )
    parts.append("<defs>")
    for i, slot in enumerate(slots):
        wv, wk, xv, ov, ok = clip_anim(slot)
        parts.append(f'<clipPath id="clip{i}">')
        parts.append(
            f'<rect x="{START_X}" y="0" height="{H}" width="0">'
            f'<animate attributeName="width" dur="{CYCLE}s" repeatCount="indefinite" '
            f'calcMode="linear" keyTimes="{";".join(str(v) for v in wk)}" values="{";".join(str(v) for v in wv)}"/>'
            f'</rect>'
        )
        parts.append("</clipPath>")
    parts.append("</defs>")

    # text layers (one per phrase, clipped)
    for i, slot in enumerate(slots):
        parts.append(
            f'<text class="t" x="{START_X}" y="{BASELINE}" '
            f'clip-path="url(#clip{i})" lengthAdjust="spacingAndGlyphs" '
            f'textLength="{slot["w"]}">{escape(slot["text"])}</text>'
        )

    # cursor blocks (one per phrase, synced position + blink visibility)
    for i, slot in enumerate(slots):
        wv, wk, xv, ov, ok = clip_anim(slot)
        parts.append(
            f'<rect class="c" x="{START_X}" y="{BASELINE - FONT_SIZE + 4}" '
            f'width="{CURSOR_W:.1f}" height="{FONT_SIZE - 2}" opacity="0">'
            f'<animate attributeName="x" dur="{CYCLE}s" repeatCount="indefinite" '
            f'calcMode="linear" keyTimes="{";".join(str(v) for v in wk)}" values="{";".join(str(v) for v in xv)}"/>'
            f'<animate attributeName="opacity" dur="{CYCLE}s" repeatCount="indefinite" '
            f'calcMode="discrete" keyTimes="{";".join(str(v) for v in ok)}" values="{";".join(str(v) for v in ov)}"/>'
            f'</rect>'
        )

    parts.append("</svg>")
    return "\n".join(parts)


def main():
    svg = build_svg()
    # validate well-formed XML
    ET.fromstring(svg)
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
    out_dir = "assets"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "typing.svg")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg + "\n")
    print(f"OK wrote {out_path} ({len(svg)} bytes), CYCLE={CYCLE}s")


if __name__ == "__main__":
    main()
