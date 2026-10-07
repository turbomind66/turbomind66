
import random, colorsys, os, math, xml.dom.minidom as M

OUT = os.path.join(os.getcwd(), 'assets')
os.makedirs(OUT, exist_ok=True)

AMP = 12        # 更扁：振幅从 22 降到 12
PERIODS = 2.5   # 更宽：波长从 400 拉长到 480（每个波更宽）

def two_color_palette():
    # 双色渐变：同一对撞色相（base 与 base+0.5），去掉中间杂色
    base = random.random()
    cols = []
    for h in (base, (base + 0.5) % 1.0):
        r, g, b = colorsys.hsv_to_rgb(h, 0.80, 0.95)
        cols.append((int(r*255), int(g*255), int(b*255)))
    return cols

def hexc(c): return '#%02x%02x%02x' % c

def sine_path(kind, w=1200, h=120):
    midline = h * 0.5
    phase = random.random() * math.tau
    def wave_y(x):
        return midline + AMP * math.sin(2*math.pi*PERIODS*x/w + phase)
    pts = []
    step = 8
    if kind == 'top':
        pts.append((0, 0)); pts.append((w, 0))
        x = w
        while x >= 0:
            pts.append((x, wave_y(x))); x -= step
        pts.append((0, wave_y(0)))
    else:
        pts.append((0, h)); pts.append((w, h))
        x = w
        while x >= 0:
            pts.append((x, wave_y(x))); x -= step
        pts.append((0, wave_y(0)))
    return 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts) + ' Z'

def make_wave(kind, palette):
    w, h = 1200, 120
    stops = ''.join(
        f'<stop offset="{i/(len(palette)-1):.3f}" stop-color="{hexc(palette[i])}"/>'
        for i in range(len(palette)))
    path = sine_path(kind)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" preserveAspectRatio="none">\n'
            f'  <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="0">{stops}</linearGradient></defs>\n'
            f'  <path d="{path}" fill="url(#g)"/>\n'
            f'</svg>\n')

for kind in ('top', 'bottom'):
    pal = two_color_palette()
    svg = make_wave(kind, pal)
    M.parseString(svg)
    with open(os.path.join(OUT, f'wave-{kind}.svg'), 'w', encoding='utf-8') as f:
        f.write(svg)
    print('wrote', kind, 'palette', [hexc(c) for c in pal], 'len', len(svg))
