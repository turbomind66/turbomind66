import os, re, random, math, colorsys, datetime

AMP = 26
PERIODS = 1.0
BASELINE = 38
VIEW_W, VIEW_H = 1200, 140

def hsl_hex(h, s=0.72, l=0.56):
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return '#%02x%02x%02x' % (int(r*255), int(g*255), int(b*255))

def gen_wave(stops):
    c1, c2 = stops
    pts = []
    n = 240
    for i in range(n+1):
        x = i / n * VIEW_W
        y = BASELINE + AMP * math.sin((i/n)*PERIODS*2*math.pi)
        pts.append(f'{x:.1f},{y:.1f}')
    d = f'M0,{VIEW_H} L0,{BASELINE+AMP*math.sin(0):.1f} L' + ' L'.join(pts)
    d += f' L{VIEW_W},{VIEW_H} Z'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VIEW_W} {VIEW_H}" '
            f'preserveAspectRatio="none" width="100%" height="{VIEW_H}>\n'
            f'  <defs>\n    <linearGradient id="g" x1="0" y1="0" x2="1" y2="0">\n'
            f'      <stop offset="0%" stop-color="{c1}"/>\n      <stop offset="100%" stop-color="{c2}"/>\n'
            f'    </linearGradient>\n  </defs>\n  <path d="{d}" fill="url(#g)"/>\n</svg>\n')

base = random.random()
stops = (hsl_hex(base), hsl_hex((base + 0.5) % 1.0))
today = datetime.date.today().strftime('%Y%m%d')
here = os.path.dirname(os.path.abspath(__file__))
assets = os.path.abspath(os.path.join(here, '..', 'assets'))
os.makedirs(assets, exist_ok=True)
top = os.path.join(assets, f'wave-top-{today}.svg')
bot = os.path.join(assets, f'wave-bottom-{today}.svg')
open(top, 'w').write(gen_wave(stops))
open(bot, 'w').write(gen_wave(stops))
rm = os.path.abspath(os.path.join(here, '..', 'README.md'))
if os.path.exists(rm):
    t = open(rm).read()
    t = re.sub(r'\./assets/wave-top-[0-9]+\.svg', f'./assets/wave-top-{today}.svg', t)
    t = re.sub(r'\./assets/wave-bottom-[0-9]+\.svg', f'./assets/wave-bottom-{today}.svg', t)
    t = t.replace('./assets/wave-top.svg', f'./assets/wave-top-{today}.svg')
    t = t.replace('./assets/wave-bottom.svg', f'./assets/wave-bottom-{today}.svg')
    open(rm, 'w').write(t)
print('wave generated:', top, bot, 'pair', stops)
