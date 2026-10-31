#!/usr/bin/env python3
"""Build the Zambia CDF Tracker favicon set from the official badge mark.

Design: deep-green disc (#0E4D30, sampled from the approved v4 badge), gold
ring, gold Zambia silhouette (the site's own geoBoundaries province polygons
from site/map.js, filled as one country), three deep-green rising bars cut
into the map's south-west — bar placement measured from the v4 badge so the
icon is the same mark, minus the text (illegible at tab size).

Outputs (into site/): favicon.svg, favicon.ico, favicon-16x16.png,
favicon-32x32.png, apple-touch-icon.png (full-bleed), icon-512.png.
Also writes a QA strip (16/32/64/128 on white and dark) to /tmp.
"""
import json, re, sys
from PIL import Image, ImageDraw

SITE = "/home/hatch/workspace/goals/zambia-cdf-dashboard-website/site-repo/site"
BADGE = "/home/hatch/workspace/zcdf-logo-v4-badge.png"
GREEN = (14, 77, 48)        # #0E4D30 sampled from badge disc
GOLD = (242, 176, 30)       # #F2B01E sampled from badge ring/map

# ---------- 1. Bar placement measured from the v4 badge (fractions of the
# badge's map bbox 292,105-731,454; bases flush at 0.928, tops ascending)
bars = [(0.091, 0.162, 0.751, 0.928),
        (0.205, 0.278, 0.662, 0.928),
        (0.321, 0.394, 0.573, 0.928)]
print("bars (x0,x1,y0,y1 map fractions):", bars)

# ---------- 2. Province polygons from the site's own map.js
raw = open(f"{SITE}/map.js").read()
data = json.loads(raw[raw.index("{"):raw.rindex("}") + 1])
polys = []   # list of subpaths, each [(x, y), ...]
for path in data.values():
    for sub in path.split("M")[1:]:
        nums = [float(v) for v in re.findall(r"-?\d+\.?\d*", sub)]
        pts = list(zip(nums[0::2], nums[1::2]))
        if len(pts) > 2:
            polys.append(pts)
allx = [x for p in polys for x, _ in p]; ally = [y for p in polys for _, y in p]
src_box = (min(allx), min(ally), max(allx), max(ally))
print("province polys:", len(polys), "src bbox:", [round(v, 1) for v in src_box])

# ---------- 3. Compose the master (1024) + SVG geometry
S = 1024
disc_d = S                      # disc fills the canvas
map_w_frac = 0.68               # map width as fraction of disc (clears the ring)
sw = src_box[2] - src_box[0]; sh = src_box[3] - src_box[1]
scale = (disc_d * map_w_frac) / sw
map_w, map_h = sw * scale, sh * scale
ox = (S - map_w) / 2            # centre horizontally
oy = (S - map_h) / 2 - S * 0.01  # optical centre, a touch high

def tx(x, y):
    return (ox + (x - src_box[0]) * scale, oy + (y - src_box[1]) * scale)

img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
d.ellipse([0, 0, S - 1, S - 1], fill=GREEN + (255,))
ring_in = S * 0.045
d.ellipse([ring_in, ring_in, S - 1 - ring_in, S - 1 - ring_in],
          outline=GOLD + (255,), width=max(6, int(S * 0.016)))
for p in polys:
    d.polygon([tx(x, y) for x, y in p], fill=GOLD + (255,))
for fx0, fx1, fy0, fy1 in bars:
    d.rectangle([ox + fx0 * map_w, oy + fy0 * map_h,
                 ox + fx1 * map_w, oy + fy1 * map_h], fill=GREEN + (255,))

img.save("/tmp/favicon-master.png")

# apple-touch-icon: full-bleed green square (iOS masks corners; no transparency)
apple = Image.new("RGBA", (S, S), GREEN + (255,))
apple.alpha_composite(img)
apple.convert("RGB").resize((180, 180), Image.LANCZOS).save(f"{SITE}/apple-touch-icon.png")
img.resize((512, 512), Image.LANCZOS).save(f"{SITE}/icon-512.png")
img.resize((32, 32), Image.LANCZOS).save(f"{SITE}/favicon-32x32.png")
img.resize((16, 16), Image.LANCZOS).save(f"{SITE}/favicon-16x16.png")
img.save(f"{SITE}/favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])

# SVG favicon from the same geometry
def pt(x, y):
    X, Y = tx(x, y)
    return f"{X:.0f},{Y:.0f}"
paths = "".join(
    "M" + "L".join(pt(x, y) for x, y in p) + "Z" for p in polys)
rects = "".join(
    f'<rect x="{ox + a * map_w:.0f}" y="{oy + c * map_h:.0f}" '
    f'width="{(bb - a) * map_w:.0f}" height="{(dd - c) * map_h:.0f}" fill="#0E4D30"/>'
    for a, bb, c, dd in bars)
cx = S / 2
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}">'
       f'<circle cx="{cx:.0f}" cy="{cx:.0f}" r="{S/2:.0f}" fill="#0E4D30"/>'
       f'<circle cx="{cx:.0f}" cy="{cx:.0f}" r="{S/2 - ring_in:.0f}" fill="none" '
       f'stroke="#F2B01E" stroke-width="{max(6, int(S * 0.016))}"/>'
       f'<path d="{paths}" fill="#F2B01E"/>{rects}</svg>')
open(f"{SITE}/favicon.svg", "w").write(svg)

# ---------- 4. QA strip: sizes on white + dark, saved for visual check
qa = Image.new("RGB", (640, 200), (255, 255, 255))
for i, sz in enumerate((128, 64, 32, 16)):
    qa.paste(img.resize((sz, sz), Image.LANCZOS), (20 + i * 150, 30), img.resize((sz, sz), Image.LANCZOS))
qa2 = Image.new("RGB", (640, 200), (32, 32, 32))
for i, sz in enumerate((128, 64, 32, 16)):
    r = img.resize((sz, sz), Image.LANCZOS)
    qa2.paste(r, (20 + i * 150, 30), r)
qa.save("/tmp/favicon-qa-white.png"); qa2.save("/tmp/favicon-qa-dark.png")
print("wrote favicon set to site/ + QA strips to /tmp")
