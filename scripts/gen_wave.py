#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate self-hosted random two-color wave SVGs for profile README.
Top wave: peaks point DOWN (eave style). Bottom wave: peaks point UP.
Amplitude is intentionally small/flat; one full sine wave across width.
"""
import math, random, re, os, datetime

W, H = 1200, 140
AMP = 13
PERIODS = 1.0


def hsl(h, s, l):
    def hue(p, q, t):
        if t < 0:
            t += 1
        if t > 1:
            t -= 1
        if t < 1 / 6:
            return p + (q - p) * 6 * t
        if t < 1 / 2:
            return q
        if t < 2 / 3:
            return p + (q - p) * (2 / 3 - t) * 6
        return p
    if s == 0:
        r = g = b = l
    else:
        q = l * (1 + s) if l < 0.5 else l + s - l * s
        p = 2 * l - q
        r = hue(p, q, h + 1 / 3)
        g = hue(p, q, h)
        b = hue(p, q, h - 1 / 3)
    return "#%02x%02x%02x" % (round(r * 255), round(g * 255), round(b * 255))


def wave_path(kind, c1, c2):
    pts = []
    for i in range(0, W + 1, 8):
        y = H / 2 + AMP * math.sin(2 * math.pi * PERIODS * i / W)
        pts.append((i, y))
    if kind == "top":
        d = "M0,0 L0,%.1f " % pts[0][1]
        d += " ".join("L%.1f,%.1f" % (x, y) for x, y in pts)
        d += " L%d,0 Z" % W
    else:
        d = "M0,%d L0,%.1f " % (H, pts[0][1])
        d += " ".join("L%.1f,%.1f" % (x, y) for x, y in pts)
        d += " L%d,%d Z" % (W, H)
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
            'preserveAspectRatio="none" width="100%%" height="%d">'
            '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="0">'
            '<stop offset="0" stop-color="%s"/>'
            '<stop offset="1" stop-color="%s"/>'
            '</linearGradient></defs>'
            '<path d="%s" fill="url(#g)"/></svg>') % (W, H, H, c1, c2, d)


def main():
    base = random.random()
    c1 = hsl(base, 0.7, 0.6)
    c2 = hsl((base + 0.5) % 1, 0.7, 0.6)
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M")
    top = "wave-top-%s.svg" % ts
    bot = "wave-bottom-%s.svg" % ts
    os.makedirs("assets", exist_ok=True)
    with open(os.path.join("assets", top), "w") as f:
        f.write(wave_path("top", c1, c2))
    with open(os.path.join("assets", bot), "w") as f:
        f.write(wave_path("bottom", c1, c2))
    if os.path.exists("README.md"):
        with open("README.md") as f:
            t = f.read()
        t = re.sub(r"(?:\./)?assets/wave-top-[\w-]+\.svg", "assets/" + top, t)
        t = re.sub(r"(?:\./)?assets/wave-bottom-[\w-]+\.svg", "assets/" + bot, t)
        with open("README.md", "w") as f:
            f.write(t)
    print("generated", top, bot)


if __name__ == "__main__":
    main()
