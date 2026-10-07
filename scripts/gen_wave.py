
import random, colorsys, os, math, xml.dom.minidom as M, re, datetime

OUT = os.path.join(os.getcwd(), 'assets')
os.makedirs(OUT, exist_ok=True)
TODAY = datetime.date.today().strftime('%Y%m%d')
AMP = 14
PERIODS = 1.0

def hsv2(h):
    r, g, b = colorsys.hsv_to_rgb(h, 0.80, 0.95)
    return (int(r*255), int(g*255), int(b*255))
def two_color_palette():
    base = random.random()
    return [hsv2(base), hsv2((base + 0.5) % 1.0)]
def hexc(c): return '#%02x%02x%02x' % c
def sine_path(kind, w=1200, h=120):
    mid = h * 0.5
    phase = random.random() * math.tau
    wy = lambda x: mid + AMP * math.sin(2*math.pi*PERIODS*x/w + phase)
    pts = [(0, 0), (w, 0)] if kind == 'top' else [(0, h), (w, h)]
    x = w
    while x >= 0:
        pts.append((x, wy(x))); x -= 8
    pts.append((0, wy(0)))
    return 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts) + ' Z'
def make_wave(kind, pal):
    stops = ''.join(f'<stop offset="{i/(len(pal)-1):.3f}" stop-color="{hexc(pal[i])}"/>' for i in range(len(pal)))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="120" viewBox="0 0 1200 120" preserveAspectRatio="none">\n'
            f'  <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="0">{stops}</linearGradient></defs>\n'
            f'  <path d="{sine_path(kind)}" fill="url(#g)"/>\n</svg>\n')

for kind in ('top', 'bottom'):
    pal = two_color_palette()
    svg = make_wave(kind, pal)
    M.parseString(svg)
    fn = os.path.join(OUT, f'wave-{kind}-{TODAY}.svg')
    with open(fn, 'w', encoding='utf-8') as f: f.write(svg)
    print('wrote', fn, [hexc(c) for c in pal])

readme = os.path.join(os.getcwd(), 'README.md')
if os.path.exists(readme):
    with open(readme, encoding='utf-8') as f: txt = f.read()
    txt = re.sub(r'\./assets/wave-top[^"]*\.svg', f'./assets/wave-top-{TODAY}.svg', txt)
    txt = re.sub(r'\./assets/wave-bottom[^"]*\.svg', f'./assets/wave-bottom-{TODAY}.svg', txt)
    with open(readme, 'w', encoding='utf-8') as f: f.write(txt)
    print('readme updated')
