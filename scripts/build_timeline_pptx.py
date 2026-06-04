"""Amorphis — Road to Orbit (Infographic style)

Two-slide PPTX inspired by the user's reference image: a real winding road
with dashed centre stripe + colour-coded map-pin markers.

Improvements over v1:
  * Catmull-Rom spline through 6 hand-placed pin anchor points → smooth
    curves, no sharp kinks
  * Pins sit AT the anchor points (well-separated by design)
  * Proper dashed centre stripe via arc-length parameterisation
  * Pin direction (above/below road) chosen per slide for tidy layout
"""
import os, math
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from lxml import etree

# ── PALETTE ─────────────────────────────────────────
BG       = RGBColor(0xF7, 0xF8, 0xFB)
BG_GRID  = RGBColor(0xE6, 0xEA, 0xF1)
ROAD     = RGBColor(0x37, 0x3C, 0x44)
ROAD_DK  = RGBColor(0x26, 0x2A, 0x32)
ROAD_DASH = RGBColor(0xFF, 0xFF, 0xFF)
INK      = RGBColor(0x1F, 0x23, 0x2B)
INK_2    = RGBColor(0x52, 0x59, 0x66)
MUTED    = RGBColor(0x8B, 0x93, 0xA1)

PINS = [
    RGBColor(0xF5, 0x8E, 0x5B),
    RGBColor(0xE8, 0x5B, 0x4E),
    RGBColor(0x6C, 0xB8, 0x7E),
    RGBColor(0x44, 0xA8, 0xB3),
    RGBColor(0x5C, 0x96, 0xCA),
    RGBColor(0x3C, 0x4E, 0x7A),
]
TITLE_SQUARES = [
    RGBColor(0xE8, 0x5B, 0x4E),
    RGBColor(0xF5, 0xB7, 0x4E),
    RGBColor(0x6C, 0xB8, 0x7E),
    RGBColor(0x44, 0xA8, 0xB3),
    RGBColor(0x5C, 0x96, 0xCA),
]

# ── DATA ────────────────────────────────────────────
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

# ── PIN ANCHOR POINTS (per slide) ───────────────────
# Strict 3-up / 3-below pattern for clean text-card spacing.
# Each tuple: (x, y_on_road, stem_above_road)
PINS_LAYOUT = [
    (1.50,  3.25, True),    # 01 above
    (3.70,  5.20, False),   # 02 below
    (5.90,  3.25, True),    # 03 above
    (8.10,  5.20, False),   # 04 below
    (10.30, 3.25, True),    # 05 above
    (12.50, 5.20, False),   # 06 below — text-card swings left
]
ROAD_PRE  = [(0.30, 4.20)]                            # come in from the left
ROAD_POST = [(13.10, 4.20)]                           # carry on past pin 6

# ── HELPERS ─────────────────────────────────────────
def set_line_solid_alpha(line, hex6, alpha_percent):
    lnE = line._get_or_add_ln()
    for child in lnE.findall(qn('a:solidFill')):
        lnE.remove(child)
    sf = etree.SubElement(lnE, qn('a:solidFill'))
    srgb = etree.SubElement(sf, qn('a:srgbClr'))
    srgb.set('val', hex6)
    a = etree.SubElement(srgb, qn('a:alpha'))
    a.set('val', str(int(alpha_percent * 1000)))

def add_text(slide, x, y, w, h, text, *, font='Calibri', size=12, bold=False,
             color=INK, align=PP_ALIGN.LEFT, spc=None):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.margin_left = tf.margin_right = Inches(0)
    tf.margin_top = tf.margin_bottom = Inches(0)
    tf.word_wrap = True
    p = tf.paragraphs[0]; p.alignment = align
    r = p.add_run()
    r.text = text
    r.font.name = font; r.font.size = Pt(size); r.font.bold = bold
    r.font.color.rgb = color
    if spc is not None: r._r.get_or_add_rPr().set('spc', str(spc))
    return tb

def catmull_rom_segment(p0, p1, p2, p3, n=20):
    """Centripetal Catmull–Rom between p1 and p2 with control p0,p3."""
    pts = []
    for i in range(n):
        t  = i / n
        t2 = t * t; t3 = t2 * t
        x = 0.5 * (
            2 * p1[0]
            + (-p0[0] + p2[0]) * t
            + (2*p0[0] - 5*p1[0] + 4*p2[0] - p3[0]) * t2
            + (-p0[0] + 3*p1[0] - 3*p2[0] + p3[0]) * t3
        )
        y = 0.5 * (
            2 * p1[1]
            + (-p0[1] + p2[1]) * t
            + (2*p0[1] - 5*p1[1] + 4*p2[1] - p3[1]) * t2
            + (-p0[1] + 3*p1[1] - 3*p2[1] + p3[1]) * t3
        )
        pts.append((x, y))
    return pts

def catmull_rom_path(waypoints, samples_per_seg=22):
    """Smooth path through all waypoints using Catmull-Rom."""
    if len(waypoints) < 2:
        return list(waypoints)
    # Extend with reflected endpoints so we can interpolate the first/last segment
    extended = [waypoints[0]] + list(waypoints) + [waypoints[-1]]
    pts = []
    for i in range(len(extended) - 3):
        seg = catmull_rom_segment(extended[i], extended[i+1], extended[i+2], extended[i+3], n=samples_per_seg)
        pts.extend(seg)
    pts.append(waypoints[-1])
    return pts

def dash_along_path(slide, pts, dash_len=0.30, gap_len=0.32, color=ROAD_DASH, width_pt=1.6):
    """Walk along the smooth path and draw alternating dash / gap segments
    so the dashes have a consistent visual length regardless of curve speed."""
    total_state = 'dash'
    remaining = dash_len
    for i in range(len(pts) - 1):
        x1, y1 = pts[i]
        x2, y2 = pts[i+1]
        seg_len = math.hypot(x2 - x1, y2 - y1)
        if seg_len < 1e-6:
            continue
        consumed = 0.0
        while consumed < seg_len:
            take = min(remaining, seg_len - consumed)
            t0 = consumed / seg_len
            t1 = (consumed + take) / seg_len
            ax = x1 + (x2 - x1) * t0; ay = y1 + (y2 - y1) * t0
            bx = x1 + (x2 - x1) * t1; by = y1 + (y2 - y1) * t1
            if total_state == 'dash':
                ln = slide.shapes.add_connector(1,
                    Inches(ax), Inches(ay), Inches(bx), Inches(by))
                ln.line.color.rgb = color
                ln.line.width = Pt(width_pt)
            consumed += take
            remaining -= take
            if remaining <= 1e-6:
                total_state = 'gap' if total_state == 'dash' else 'dash'
                remaining = gap_len if total_state == 'gap' else dash_len

def add_shadowed_oval(slide, cx, cy, r, fill, ring_color=ROAD_DASH, ring_w_pt=2.5):
    # Shadow circle just behind
    sh = slide.shapes.add_shape(MSO_SHAPE.OVAL,
        Inches(cx - r), Inches(cy - r + 0.05),
        Inches(r*2), Inches(r*2))
    sh.fill.solid(); sh.fill.fore_color.rgb = RGBColor(0, 0, 0)
    sh.line.fill.background()
    # Translucency via XML
    spPr = sh.fill.fore_color._xFill.getparent()
    srgb = spPr.find(qn('a:srgbClr'))
    if srgb is not None:
        a = etree.SubElement(srgb, qn('a:alpha'))
        a.set('val', '20000')
    # Main coloured circle
    main = slide.shapes.add_shape(MSO_SHAPE.OVAL,
        Inches(cx - r), Inches(cy - r),
        Inches(r*2), Inches(r*2))
    main.fill.solid(); main.fill.fore_color.rgb = fill
    main.line.color.rgb = ring_color; main.line.width = Pt(ring_w_pt)
    return main

# ── PRESENTATION ────────────────────────────────────
prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)

def build_slide(slide_milestones, pin_anchors, part_label, date_range, idx_start):
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Background
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid(); bg.fill.fore_color.rgb = BG; bg.line.fill.background()

    # Faint grid
    for gx in range(1, 14):
        ln = slide.shapes.add_connector(1, Inches(gx), Inches(0), Inches(gx), Inches(7.5))
        ln.line.color.rgb = BG_GRID; ln.line.width = Pt(0.4)
    for gy in range(1, 8):
        ln = slide.shapes.add_connector(1, Inches(0), Inches(gy), Inches(13.333), Inches(gy))
        ln.line.color.rgb = BG_GRID; ln.line.width = Pt(0.4)

    # Title squares row
    sq_size = 0.18
    sq_y = 0.42
    sq_total_w = len(TITLE_SQUARES) * sq_size + (len(TITLE_SQUARES) - 1) * 0.04
    sq_x0 = (13.333 - sq_total_w) / 2
    for i, col in enumerate(TITLE_SQUARES):
        sq = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
            Inches(sq_x0 + i * (sq_size + 0.04)), Inches(sq_y),
            Inches(sq_size), Inches(sq_size))
        sq.fill.solid(); sq.fill.fore_color.rgb = col; sq.line.fill.background()

    add_text(slide, 0, 0.66, 13.333, 0.55,
             "OUR ROAD TO ORBIT",
             font='Calibri', size=30, bold=True, color=INK,
             align=PP_ALIGN.CENTER, spc=250)

    add_text(slide, 0, 1.18, 13.333, 0.32,
             f"〔  {part_label}   ·   {date_range}   ·   AMORPHIS  〕",
             font='Consolas', size=10, bold=True, color=INK_2,
             align=PP_ALIGN.CENTER, spc=400)

    # ── Road waypoints — extend pin anchors with road tails ────
    waypoints = list(ROAD_PRE)
    for (px, py, _above) in pin_anchors:
        waypoints.append((px, py))
    waypoints.extend(ROAD_POST)

    pts = catmull_rom_path(waypoints, samples_per_seg=24)

    # Shadow (offset down)
    for k in range(len(pts) - 1):
        x1, y1 = pts[k]; x2, y2 = pts[k+1]
        ln = slide.shapes.add_connector(1,
            Inches(x1), Inches(y1 + 0.06),
            Inches(x2), Inches(y2 + 0.06))
        ln.line.color.rgb = ROAD_DK; ln.line.width = Pt(32)
        set_line_solid_alpha(ln.line, '262A32', 22)

    # Road body
    for k in range(len(pts) - 1):
        x1, y1 = pts[k]; x2, y2 = pts[k+1]
        ln = slide.shapes.add_connector(1,
            Inches(x1), Inches(y1), Inches(x2), Inches(y2))
        ln.line.color.rgb = ROAD; ln.line.width = Pt(28)

    # Proper dashed centre stripe
    dash_along_path(slide, pts, dash_len=0.32, gap_len=0.32, width_pt=1.6)

    # ── Pins ───────────────────────────────────────
    PIN_R = 0.30
    # Stem lengths: above pins need more room for text growing upward
    STEM_ABOVE = 1.15
    STEM_BELOW = 0.90
    PILL_W = 1.30; PILL_H = 0.26
    TEXT_W = 1.75   # slightly wider for more comfortable wrapping

    for i, (px, py, above) in enumerate(pin_anchors):
        col = PINS[i]
        # Stem
        stem_len = STEM_ABOVE if above else STEM_BELOW
        stem_y0 = py + (-0.22 if above else 0.22)
        stem_y1 = py + (-stem_len if above else stem_len)
        stem = slide.shapes.add_connector(1,
            Inches(px), Inches(stem_y0),
            Inches(px), Inches(stem_y1))
        stem.line.color.rgb = col; stem.line.width = Pt(2.6)

        # Pin head
        head_cy = stem_y1
        add_shadowed_oval(slide, px, head_cy, PIN_R, fill=col)

        # Number centred inside pin head
        num_tb = slide.shapes.add_textbox(
            Inches(px - PIN_R), Inches(head_cy - 0.18),
            Inches(PIN_R * 2), Inches(0.36))
        ntf = num_tb.text_frame
        ntf.margin_left = ntf.margin_right = Inches(0)
        ntf.margin_top = ntf.margin_bottom = Inches(0)
        np = ntf.paragraphs[0]; np.alignment = PP_ALIGN.CENTER
        nr = np.add_run(); nr.text = f"{idx_start + i:02d}"
        nr.font.name = "Calibri"; nr.font.size = Pt(15); nr.font.bold = True
        nr.font.color.rgb = ROAD_DASH

        # ── Text card Y+X placement ────────────────
        # Text sits BESIDE the pin (horizontal).  The ENTIRE block is
        # vertically centred on head_cy so it never crosses the road or
        # runs off the slide edges.
        # Block order top→bottom: pill → title → description  (total ≈1.35 in)
        BLOCK_H = PILL_H + 0.06 + 0.32 + 0.06 + 0.65
        ty_pill  = head_cy - BLOCK_H / 2
        ty_title = ty_pill + PILL_H + 0.06
        ty_desc  = ty_title + 0.32 + 0.06

        # Clamp so block never clips slide top (below header) or bottom
        TOP_GUARD = 1.45
        BOT_GUARD = 7.35
        if ty_pill < TOP_GUARD:
            d = TOP_GUARD - ty_pill
            ty_pill += d; ty_title += d; ty_desc += d
        if ty_desc + 0.65 > BOT_GUARD:
            d = (ty_desc + 0.65) - BOT_GUARD
            ty_pill -= d; ty_title -= d; ty_desc -= d

        # X: prefer right of pin, flip left only if overflows slide
        text_right = (px + PIN_R + 0.14 + TEXT_W) <= 13.15
        if text_right:
            tx = px + PIN_R + 0.14; align = PP_ALIGN.LEFT
        else:
            tx = px - PIN_R - 0.14 - TEXT_W; align = PP_ALIGN.RIGHT

        pill_x = tx if align == PP_ALIGN.LEFT else (tx + TEXT_W - PILL_W)

        # Date pill
        pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(pill_x), Inches(ty_pill),
            Inches(PILL_W), Inches(PILL_H))
        pill.fill.solid(); pill.fill.fore_color.rgb = col
        pill.line.fill.background()
        ptf = pill.text_frame
        ptf.margin_left = Inches(0.06); ptf.margin_right = Inches(0.06)
        ptf.margin_top = ptf.margin_bottom = Inches(0.02)
        ptf.word_wrap = False
        pp = ptf.paragraphs[0]; pp.alignment = PP_ALIGN.CENTER
        pr = pp.add_run(); pr.text = slide_milestones[i][0]
        pr.font.name = 'Consolas'; pr.font.size = Pt(9); pr.font.bold = True
        pr.font.color.rgb = ROAD_DASH
        pr._r.get_or_add_rPr().set('spc', '60')

        # Title (bold)
        add_text(slide, tx, ty_title, TEXT_W, 0.34,
                 slide_milestones[i][1],
                 font='Calibri', size=13, bold=True, color=INK, align=align)

        # Description — height 0.65 (~3 short lines at 9pt)
        add_text(slide, tx, ty_desc, TEXT_W, 0.65,
                 slide_milestones[i][2],
                 font='Calibri', size=9.5, color=INK_2, align=align)

    # Footer
    add_text(slide, 0.6, 7.20, 9, 0.25,
             "AMORPHIS · INDIA'S FIRST SPACE-GRADE SMA ACTUATOR COMPANY",
             font='Consolas', size=8, color=MUTED, spc=500)
    add_text(slide, 9.5, 7.20, 3.5, 0.25,
             part_label,
             font='Consolas', size=8, color=MUTED, align=PP_ALIGN.RIGHT, spc=500)


build_slide(MILESTONES[:6],  PINS_LAYOUT, "PART 1 / 2", "AUG 2021 → SEPT 2023", 1)
build_slide(MILESTONES[6:], PINS_LAYOUT, "PART 2 / 2", "JAN 2024 → MAY 2027",  7)

OUT = os.path.join(os.path.dirname(__file__), '..', 'Amorphis-Timeline.pptx')
try:
    prs.save(OUT)
    print(f'Saved: {OUT}')
except PermissionError:
    ALT = os.path.join(os.path.dirname(__file__), '..', 'Amorphis-Timeline-v2.pptx')
    prs.save(ALT)
    print(f'!! Original file locked, saved to: {ALT}')
print(f'Slides: {len(prs.slides)}')
