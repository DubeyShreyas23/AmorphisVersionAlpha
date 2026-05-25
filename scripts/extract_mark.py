"""Extract just the metallic A-mark from amorphis-logo.png and discard
   the 'AMORPHIS' text underneath.

   Strategy: scan the rows of the (already-transparent-backgrounded) image
   top-to-bottom. The mark is the first contiguous block of non-empty rows.
   The first horizontal gap (>= MIN_GAP empty rows) after that block is the
   boundary between the mark and the text — crop just above it.
"""
from PIL import Image
import os, sys

ROOT = os.path.join(os.path.dirname(__file__), '..')
SRC  = os.path.join(ROOT, 'amorphis-logo.png')
DST  = os.path.join(ROOT, 'amorphis-mark.png')

ALPHA_T   = 28        # any pixel with alpha > this counts as "content"
MIN_GAP   = 10        # rows of pure transparency that mark the gap between A and AMORPHIS

img = Image.open(SRC).convert('RGBA')
w, h = img.size
print(f'Source: {w}x{h}')

# Build a per-row "has_content" flag
alpha = img.split()[-1]
row_has = []
for y in range(h):
    has = False
    for x in range(w):
        if alpha.getpixel((x, y)) > ALPHA_T:
            has = True
            break
    row_has.append(has)

# Find the bottom of the mark: walk down through the first block of content,
# then through the first gap >= MIN_GAP empty rows.
in_block = False
gap_run  = 0
mark_bottom = h
for y, has in enumerate(row_has):
    if has:
        if not in_block:
            in_block = True
        gap_run = 0
    else:
        if in_block:
            gap_run += 1
            if gap_run >= MIN_GAP:
                # We've cleared the mark and have a confirmed gap
                mark_bottom = y - gap_run + 2     # crop just inside the gap
                break

# A few pixels of breathing room, but don't undershoot
mark_bottom = min(h, mark_bottom + 6)

# Find the actual visible horizontal bbox so we don't keep blank columns
col_has = [False]*w
for x in range(w):
    for y in range(mark_bottom):
        if alpha.getpixel((x, y)) > ALPHA_T:
            col_has[x] = True
            break
left  = next((x for x, c in enumerate(col_has) if c), 0)
right = w - next((x for x, c in enumerate(reversed(col_has)) if c), 0)

# A bit of padding so the drop-shadow filter doesn't clip
PAD = 18
crop = (max(0, left - PAD), 0, min(w, right + PAD), mark_bottom)
mark = img.crop(crop)
print(f'Crop  : {crop} → {mark.size}')

# Cap width at 700 px so the file stays small
MAX_W = 700
if mark.width > MAX_W:
    new_h = int(mark.height * MAX_W / mark.width)
    mark = mark.resize((MAX_W, new_h), Image.LANCZOS)

mark.save(DST, 'PNG', optimize=True)
print(f'Output: {mark.size}, {os.path.getsize(DST)/1024:.1f} KB → {DST}')
