# -*- coding: utf-8 -*-
"""Generate full-width random two-color waves and update README refs.
Single wave, AMP=13, sharp peak (pow 0.6) / round trough (pow 1.2).
Top wave fills from top edge (peak down); bottom fills to bottom (peak up).
Writes wave-top-YYYYMMDD-HHMM.svg / wave-bottom-YYYYMMDD-HHMM.svg and rewrites README img refs (width=100%).
"""
import re, time, random, math, colorsys, io, os

W, VIEW_H = 1440, 140
AMP = 13
PERIODS = 1.0
PEAK_POW, TROUGH_POW = 0.6, 1.2
STEP = 8
MID = VIEW_H / 2.0
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def shape(sv):
    return sv ** PEAK_POW if sv >= 0 else -((-sv) ** TROUGH_POW)

def wave_points(phase):
    pts = []
    x = 0
    while x <= W:
        sv = math.sin(2 * math.pi * (x / (W / PERIODS)) + phase)
        pts.append((x, MID - AMP * shape(sv)))
        x += STEP
    return pts

def gen_svg(top, phase, c1, c2):
    line = ' '.join('%.1f,%.1f' % p for p in wave_points(phase))
    if top:
        d = 'M0,0 L%s L%d,0 Z' % (line, W)
    else:
        d = 'M0,%d L%s L%d,%d Z' % (VIEW_H, line, W, VIEW_H)
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
            'preserveAspectRatio="none" width="%d" height="%d">\n' % (W, VIEW_H, W, VIEW_H)
            + '  <defs>\n'
            + '    <linearGradient id="g" x1="0" y1="0" x2="1" y2="0">\n'
            + '      <stop offset="0%%" stop-color="%s"/>\n' % c1
            + '      <stop offset="100%%" stop-color="%s"/>\n' % c2
            + '    </linearGradient>\n  </defs>\n'
            + '  <path d="%s" fill="url(#g)"/>\n</svg>\n' % d)

def main():
    ts = time.strftime('%Y%m%d-%H%M')
    top_name = 'wave-top-%s.svg' % ts
    bot_name = 'wave-bottom-%s.svg' % ts
    base_hue = random.random()
    c1 = '#%02x%02x%02x' % tuple(int(v * 255) for v in colorsys.hls_to_rgb(base_hue, 0.6, 0.65))
    c2 = '#%02x%02x%02x' % tuple(int(v * 255) for v in colorsys.hls_to_rgb((base_hue + 0.45) % 1.0, 0.6, 0.65))
    phase = random.random() * 2 * math.pi
    svg_top = gen_svg(True, phase, c1, c2)
    svg_bot = gen_svg(False, phase, c1, c2)
    assets = os.path.join(ROOT, 'assets')
    os.makedirs(assets, exist_ok=True)
    with io.open(os.path.join(assets, top_name), 'w', encoding='utf-8') as f:
        f.write(svg_top)
    with io.open(os.path.join(assets, bot_name), 'w', encoding='utf-8') as f:
        f.write(svg_bot)
    readme_path = os.path.join(ROOT, 'README.md')
    with io.open(readme_path, 'r', encoding='utf-8') as f:
        readme = f.read()
    readme = re.sub(r'<img src="assets/wave-top-[\w\-]+\.svg"[^>]*/>',
                    '<img src="assets/%s" width="100%%" />' % top_name, readme)
    readme = re.sub(r'<img src="assets/wave-bottom-[\w\-]+\.svg"[^>]*/>',
                    '<img src="assets/%s" width="100%%" />' % bot_name, readme)
    with io.open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme)
    print('generated', top_name, bot_name, 'colors', c1, c2)

if __name__ == '__main__':
    main()
