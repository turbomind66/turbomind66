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
    n = 240
    pts = []
    for i in range(n+1):
        x = i / n * VIEW_W
        y = BASELINE + AMP * math.sin((i/n)*PERIODS*2*math.pi)
        pts.append('%.1f,%.1f' % (x, y))
    d = 'M0,%d L0,%.1f L%s L%d,%d Z' % (VIEW_H, BASELINE+AMP*math.sin(0), ' L'.join(pts), VIEW_W, VIEW_H)
    svg = []
    svg.append('<svg xmlns="http://www.w3.org/2000/svg"')
    svg.append(' viewBox="0 0 %d %d"' % (VIEW_W, VIEW_H))
    svg.append(' preserveAspectRatio="none" width="100%%" height="%d">' % VIEW_H)
    svg.append('\n  <defs>\n    <linearGradient id="g" x1="0" y1="0" x2="1" y2="0">\n')
    svg.append('      <stop offset="0%%" stop-color="%s"/>\n' % c1)
    svg.append('      <stop offset="100%%" stop-color="%s"/>\n' % c2)
    svg.append('    </linearGradient>\n  </defs>\n')
    svg.append('  <path d="%s" fill="url(#g)"/>\n' % d)
    svg.append('</svg>\n')
    return ''.join(svg)

# 时间戳文件名（含时分），每次运行换新 URL，避开 GitHub camo 图片缓存
stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M')
stops = (hsl_hex(random.random()), hsl_hex((random.random() + 0.5) % 1.0))
here = os.path.dirname(os.path.abspath(__file__))
assets = os.path.abspath(os.path.join(here, '..', 'assets'))
os.makedirs(assets, exist_ok=True)
top = os.path.join(assets, 'wave-top-%s.svg' % stamp)
bot = os.path.join(assets, 'wave-bottom-%s.svg' % stamp)
open(top, 'w').write(gen_wave(stops))
open(bot, 'w').write(gen_wave(stops))
rm = os.path.abspath(os.path.join(here, '..', 'README.md'))
if os.path.exists(rm):
    t = open(rm).read()
    t = re.sub(r'\./assets/wave-top-[\d\-]+\.svg', './assets/wave-top-%s.svg' % stamp, t)
    t = re.sub(r'\./assets/wave-bottom-[\d\-]+\.svg', './assets/wave-bottom-%s.svg' % stamp, t)
    t = t.replace('./assets/wave-top.svg', './assets/wave-top-%s.svg' % stamp)
    t = t.replace('./assets/wave-bottom.svg', './assets/wave-bottom-%s.svg' % stamp)
    open(rm, 'w').write(t)
print('wave generated:', top, bot, 'pair', stops)
