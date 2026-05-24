"""Prepare amorphis-logo.png for the web:
   - flood-fill white background to alpha=0 (with anti-alias-friendly threshold)
   - crop to visible content
   - downscale to a sensible max width
   - save as optimised PNG
"""
from PIL import Image
import sys, os

SRC = os.path.join(os.path.dirname(__file__), '..', 'amorphis-logo.png')
DST = os.path.join(os.path.dirname(__file__), '..', 'amorphis-logo.png')

img = Image.open(SRC).convert('RGBA')
w, h = img.size
print(f'Input  : {w}x{h}, {os.path.getsize(SRC)/1024:.1f} KB')

# Per-pixel: if the pixel is close to pure white, drop alpha.
# Anti-alias the edge so it doesn't look jagged.
px = img.load()
THRESH = 235          # min luminance to consider "white" — anything brighter -> alpha 0
EDGE   = 245          # above this -> fully transparent; between THRESH..EDGE soft fade
for y in range(h):
    for x in range(w):
        r, g, b, a = px[x, y]
        lum = max(r, g, b)
        if r > THRESH and g > THRESH and b > THRESH and abs(r-g) < 12 and abs(g-b) < 12:
            if lum >= EDGE:
                px[x, y] = (r, g, b, 0)
            else:
                # soft alpha between thresholds
                frac = (lum - THRESH) / (EDGE - THRESH)   # 0..1
                new_a = int(a * (1.0 - frac))
                px[x, y] = (r, g, b, new_a)

# Crop to the bounding box of non-transparent pixels (plus 16-px padding)
bbox = img.getbbox()
if bbox:
    pad = 24
    bbox = (max(0, bbox[0]-pad), max(0, bbox[1]-pad), min(w, bbox[2]+pad), min(h, bbox[3]+pad))
    img = img.crop(bbox)

# Downscale: max width 900 px keeps logo crisp at any hero size
MAX_W = 900
if img.width > MAX_W:
    new_h = int(img.height * MAX_W / img.width)
    img = img.resize((MAX_W, new_h), Image.LANCZOS)

img.save(DST, 'PNG', optimize=True)
print(f'Output : {img.width}x{img.height}, {os.path.getsize(DST)/1024:.1f} KB')
