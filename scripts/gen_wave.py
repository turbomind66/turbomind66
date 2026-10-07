import random, colorsys, os, xml.dom.minidom as M

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

def make_wave(kind, palette):
    w, h = 1200, 120
    stops = ''.join(
        f'<stop offset="{i/(len(palette)-1):.3f}" stop-color="{hexc(palette[i])}"/>'
        for i in range(len(palette)))
    if kind == 'top':
        path = ('M0,0 L1200,0 L1200,55 '
                'C1050,105 950,15 800,55 '
                'C650,95 550,15 400,55 '
                'C250,95 150,15 0,55 Z')
    else:
        path = ('M0,55 '
                'C150,15 250,95 400,55 '
                'C550,15 650,95 800,55 '
                'C950,15 1050,95 1200,55 '
                'L1200,120 L0,120 Z')
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
    print('wrote', kind, [hexc(c) for c in pal])
