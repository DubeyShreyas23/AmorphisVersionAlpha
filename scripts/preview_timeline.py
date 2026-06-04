"""PNG previews of the infographic-style timeline (matches build_timeline_pptx.py)."""
import os, math
from PIL import Image, ImageDraw, ImageFont

SLIDE_W_IN = 13.333
SLIDE_H_IN = 7.5
SCALE = 130
W = int(SLIDE_W_IN * SCALE)
H = int(SLIDE_H_IN * SCALE)
def i(v): return int(v * SCALE)

BG       = (0xF7, 0xF8, 0xFB)
BG_GRID  = (0xE6, 0xEA, 0xF1)
ROAD     = (0x37, 0x3C, 0x44)
ROAD_DK  = (0x26, 0x2A, 0x32)
ROAD_DASH = (0xFF, 0xFF, 0xFF)
INK      = (0x1F, 0x23, 0x2B)
INK_2    = (0x52, 0x59, 0x66)
MUTED    = (0x8B, 0x93, 0xA1)

PINS = [
    (0xF5, 0x8E, 0x5B),
    (0xE8, 0x5B, 0x4E),
    (0x6C, 0xB8, 0x7E),
    (0x44, 0xA8, 0xB3),
    (0x5C, 0x96, 0xCA),
    (0x3C, 0x4E, 0x7A),
]
TITLE_SQUARES = [
    (0xE8, 0x5B, 0x4E),
    (0xF5, 0xB7, 0x4E),
    (0x6C, 0xB8, 0x7E),
    (0x44, 0xA8, 0xB3),
    (0x5C, 0x96, 0xCA),
]

def F(size, bold=False, mono=False):
    name = ('consola.ttf' if not bold else 'consolab.ttf') if mono else \
           ('calibrib.ttf' if bold else 'calibri.ttf')
    try: return ImageFont.truetype(name, size)
    except OSError: return ImageFont.load_default()

title_font  = F(int(30 * 1.4), bold=True)
sub_font    = F(int(10 * 1.4), bold=True, mono=True)
pin_num     = F(int(15 * 1.4), bold=True)
pill_font   = F(int(9 * 1.4), bold=True, mono=True)
title_card  = F(int(14 * 1.4), bold=True)
body_card   = F(int(9.5 * 1.4))
foot_font   = F(int(8 * 1.4), mono=True)

MILESTONES = [
    ("Aug 2021",            "Dhruva Evaluation",   "Global evaluation of SMA HDRM for Dhruva Space's satellite deployer system."),
    ("Aug 2021 – Mar 2022", "Vendor Quotes",       "Vendor quotes ranged $5,000 – $10,000 per system."),
    ("Apr 2022",            "Burn-Wire Build",     "Built own Dhruva Space burn-wire mechanism. Passed ISRO review board."),
    ("Jan 2023",            "ISRO HSFC Proposal",  "Co-wrote ISRO HSFC proposal. EoI on SMA actuators for module locking."),
    ("Feb 2023",            "EM Procurement",      "Procured an SMA engineering model from a European startup."),
    ("Sept 2023",           "Actuator Delivery",   "Vibration-qualified, thermo-vac tested European SMA actuator."),
    ("Jan 2024",            "Deep Evaluation",     "Damaged the actuator during deep eval — no actuation, over-current."),
    ("Apr 2024",            "Iteration",           "Ordered additional actuators and continued evaluation."),
    ("Aug 2024",            "Sankalp · PhD",       'Sankalp joined PhD: "SMA actuator design and development for space".'),
    ("Sept 2025",           "Kushagra · Robotics", "Kushagra worked with a space-robotics startup using super-elastic Nitinol."),
    ("May 2026",            "Amorphis Founded",    "Amorphis established for sector-agnostic SMA actuators."),
    ("May 2027",            "Market Release",      "First indigenous SMA actuator — market release."),
]

PINS_S1 = [
    (1.50,  3.25, True),
    (3.70,  5.20, False),
    (5.90,  3.25, True),
    (8.10,  5.20, False),
    (10.30, 3.25, True),
    (12.50, 5.20, False),
]
ROAD_PRE  = [(0.30, 4.20)]
ROAD_POST = [(13.10, 4.20)]

def wrap(draw, text, font, max_w_px):
    words = text.split(); lines = []; cur = ''
    for w in words:
        test = (cur + ' ' + w).strip()
        bb = draw.textbbox((0, 0), test, font=font)
        if bb[2] - bb[0] > max_w_px and cur:
            lines.append(cur); cur = w
        else:
            cur = test
    if cur: lines.append(cur)
    return lines

def catmull_rom_seg(p0, p1, p2, p3, n=22):
    pts = []
    for k in range(n):
        t = k / n; t2 = t*t; t3 = t2*t
        x = 0.5*(2*p1[0] + (-p0[0]+p2[0])*t + (2*p0[0]-5*p1[0]+4*p2[0]-p3[0])*t2 + (-p0[0]+3*p1[0]-3*p2[0]+p3[0])*t3)
        y = 0.5*(2*p1[1] + (-p0[1]+p2[1])*t + (2*p0[1]-5*p1[1]+4*p2[1]-p3[1])*t2 + (-p0[1]+3*p1[1]-3*p2[1]+p3[1])*t3)
        pts.append((x, y))
    return pts

def catmull_path(wps, samples_per_seg=24):
    ext = [wps[0]] + list(wps) + [wps[-1]]
    pts = []
    for k in range(len(ext) - 3):
        pts.extend(catmull_rom_seg(ext[k], ext[k+1], ext[k+2], ext[k+3], samples_per_seg))
    pts.append(wps[-1])
    return pts

def dash_along(draw, pts, dash_len=0.32, gap_len=0.32, width=2, color=ROAD_DASH):
    state = 'dash'; remaining = dash_len
    for k in range(len(pts) - 1):
        x1, y1 = pts[k]; x2, y2 = pts[k+1]
        seg = math.hypot(x2 - x1, y2 - y1)
        if seg < 1e-6: continue
        consumed = 0.0
        while consumed < seg:
            take = min(remaining, seg - consumed)
            t0 = consumed / seg; t1 = (consumed + take) / seg
            ax = x1 + (x2-x1)*t0; ay = y1 + (y2-y1)*t0
            bx = x1 + (x2-x1)*t1; by = y1 + (y2-y1)*t1
            if state == 'dash':
                draw.line((i(ax), i(ay), i(bx), i(by)), fill=color, width=width)
            consumed += take; remaining -= take
            if remaining <= 1e-6:
                state = 'gap' if state == 'dash' else 'dash'
                remaining = gap_len if state == 'gap' else dash_len

def render_slide(milestones, pin_anchors, part_label, date_range, idx_start, out_path):
    img = Image.new('RGB', (W, H), BG)
    draw = ImageDraw.Draw(img, 'RGBA')

    # Grid
    for gx in range(1, 14):
        draw.line((i(gx), 0, i(gx), H), fill=BG_GRID, width=1)
    for gy in range(1, 8):
        draw.line((0, i(gy), W, i(gy)), fill=BG_GRID, width=1)

    # Title squares
    sq_size = 0.18; sq_y = 0.42
    sq_total_w = len(TITLE_SQUARES) * sq_size + (len(TITLE_SQUARES) - 1) * 0.04
    sq_x0 = (13.333 - sq_total_w) / 2
    for j, col in enumerate(TITLE_SQUARES):
        x = sq_x0 + j * (sq_size + 0.04)
        draw.rectangle((i(x), i(sq_y), i(x + sq_size), i(sq_y + sq_size)), fill=col)

    # Title
    text = "OUR ROAD TO ORBIT"
    bb = draw.textbbox((0, 0), text, font=title_font)
    tw = bb[2] - bb[0]
    draw.text(((W - tw) // 2, i(0.66)), text, font=title_font, fill=INK)

    # Subtitle
    sub = f"〔  {part_label}   ·   {date_range}   ·   AMORPHIS  〕"
    bb = draw.textbbox((0, 0), sub, font=sub_font)
    sw = bb[2] - bb[0]
    draw.text(((W - sw) // 2, i(1.18)), sub, font=sub_font, fill=INK_2)

    # Road waypoints
    waypoints = list(ROAD_PRE)
    for (px, py, _a) in pin_anchors:
        waypoints.append((px, py))
    waypoints.extend(ROAD_POST)
    pts = catmull_path(waypoints, samples_per_seg=24)

    # Road shadow
    for k in range(len(pts) - 1):
        x1, y1 = pts[k]; x2, y2 = pts[k+1]
        draw.line((i(x1), i(y1 + 0.06), i(x2), i(y2 + 0.06)),
                  fill=ROAD_DK + (60,), width=int(32 * 1.4))
    # Road body
    for k in range(len(pts) - 1):
        x1, y1 = pts[k]; x2, y2 = pts[k+1]
        draw.line((i(x1), i(y1), i(x2), i(y2)), fill=ROAD, width=int(28 * 1.4))

    # Dashed centre
    dash_along(draw, pts, dash_len=0.32, gap_len=0.32, width=2)

    # Pins
    PIN_R = 0.30
    STEM_ABOVE = 1.15
    STEM_BELOW = 0.90
    PILL_W = 1.30; PILL_H = 0.26
    TEXT_W = 1.75

    for j, (px, py, above) in enumerate(pin_anchors):
        col = PINS[j]
        stem_len = STEM_ABOVE if above else STEM_BELOW
        stem_y0 = py + (-0.22 if above else 0.22)
        stem_y1 = py + (-stem_len if above else stem_len)
        # Stem
        draw.line((i(px), i(stem_y0), i(px), i(stem_y1)), fill=col, width=5)
        # Pin shadow
        draw.ellipse((i(px - PIN_R), i(stem_y1 - PIN_R + 0.05),
                      i(px + PIN_R), i(stem_y1 + PIN_R + 0.05)),
                     fill=(0, 0, 0, 50))
        # Pin head
        draw.ellipse((i(px - PIN_R), i(stem_y1 - PIN_R),
                      i(px + PIN_R), i(stem_y1 + PIN_R)),
                     fill=col, outline=ROAD_DASH, width=3)
        # Number
        num = f"{idx_start + j:02d}"
        bb = draw.textbbox((0, 0), num, font=pin_num)
        nw, nh = bb[2]-bb[0], bb[3]-bb[1]
        draw.text((i(px) - nw // 2, i(stem_y1) - nh // 2 - 3),
                  num, font=pin_num, fill=ROAD_DASH)

        # Text card
        head_cy = stem_y1

        # Y: entire block centred on head_cy, clamped to slide bounds
        BLOCK_H = PILL_H + 0.06 + 0.32 + 0.06 + 0.65
        ty_pill  = head_cy - BLOCK_H / 2
        ty_title = ty_pill + PILL_H + 0.06
        ty_desc  = ty_title + 0.32 + 0.06

        TOP_GUARD = 1.45; BOT_GUARD = 7.35
        if ty_pill < TOP_GUARD:
            d = TOP_GUARD - ty_pill
            ty_pill += d; ty_title += d; ty_desc += d
        if ty_desc + 0.65 > BOT_GUARD:
            d = (ty_desc + 0.65) - BOT_GUARD
            ty_pill -= d; ty_title -= d; ty_desc -= d

        # X: prefer right, flip left near edge
        text_right = (px + PIN_R + 0.14 + TEXT_W) <= 13.15
        if text_right:
            tx = px + PIN_R + 0.14; align_right = False
        else:
            tx = px - PIN_R - 0.14 - TEXT_W; align_right = True

        pill_x = tx if not align_right else (tx + TEXT_W - PILL_W)

        # Date pill
        draw.rounded_rectangle((i(pill_x), i(ty_pill),
                                i(pill_x + PILL_W), i(ty_pill + PILL_H)),
                               radius=int(0.05 * SCALE), fill=col)
        bb = draw.textbbox((0, 0), milestones[j][0], font=pill_font)
        pw, ph = bb[2]-bb[0], bb[3]-bb[1]
        draw.text((i(pill_x) + (i(PILL_W) - pw) // 2,
                   i(ty_pill) + (i(PILL_H) - ph) // 2 - 2),
                  milestones[j][0], font=pill_font, fill=ROAD_DASH)

        # Title
        title = milestones[j][1]
        bb = draw.textbbox((0, 0), title, font=title_card)
        ttw = bb[2] - bb[0]
        if align_right:
            draw.text((i(tx + TEXT_W) - ttw, i(ty_title)),
                      title, font=title_card, fill=INK)
        else:
            draw.text((i(tx), i(ty_title)),
                      title, font=title_card, fill=INK)

        # Description (wrapped, max 3 lines)
        body = milestones[j][2]
        max_w_px = i(TEXT_W) - 4
        lines = wrap(draw, body, body_card, max_w_px)[:3]
        line_h = body_card.size + 3
        for li, line in enumerate(lines):
            if align_right:
                bb = draw.textbbox((0, 0), line, font=body_card)
                lw = bb[2] - bb[0]
                draw.text((i(tx + TEXT_W) - lw - 2, i(ty_desc) + li * line_h),
                          line, font=body_card, fill=INK_2)
            else:
                draw.text((i(tx) + 2, i(ty_desc) + li * line_h),
                          line, font=body_card, fill=INK_2)

    # Footer
    draw.text((i(0.6), i(7.20)),
              "AMORPHIS · INDIA'S FIRST SPACE-GRADE SMA ACTUATOR COMPANY",
              font=foot_font, fill=MUTED)
    draw.text((i(11.0), i(7.20)), part_label, font=foot_font, fill=MUTED)

    img.save(out_path, 'PNG')
    print(f'Saved: {out_path}')

OUT_DIR = os.path.join(os.path.dirname(__file__), '..')
render_slide(MILESTONES[:6],  PINS_S1, "PART 1 / 2", "AUG 2021 → SEPT 2023", 1,
             os.path.join(OUT_DIR, 'timeline-preview-1.png'))
render_slide(MILESTONES[6:], PINS_S1, "PART 2 / 2", "JAN 2024 → MAY 2027", 7,
             os.path.join(OUT_DIR, 'timeline-preview-2.png'))
