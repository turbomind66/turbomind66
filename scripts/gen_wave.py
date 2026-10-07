import random, colorsys, os, math, xml.dom.minidom as M

OUT = os.path.join(os.getcwd(), 'assets')
os.makedirs(OUT, exist_ok=True)

def random_palette(n=4):
    base = random.random()
    cols = []
    for i in range(n):
        h = (base + i / n) % 1.0
        r, g, b = colorsys.hsv_to_rgb(h, 0.78, 0.95)
        cols.append((int(r*255), int(g*255), int(b*255)))
    return cols

def hexc(c): return '#%02x%02x%02x' % c

def sine_path(kind, w=1200, h=120, amp=22, periods=3.0):
    midline = h * 0.5
    phase = random.random() * math.tau
    def wave_y(x):
        return midline + amp * math.sin(2*math.pi*periods*x/w + phase)
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
    pal = random_palette(4)
    svg = make_wave(kind, pal)
    M.parseString(svg)
    with open(os.path.join(OUT, f'wave-{kind}.svg'), 'w', encoding='utf-8') as f:
        f.write(svg)
    print('wrote', kind, 'palette', [hexc(c) for c in pal], 'len', len(svg))
