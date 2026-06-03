"""Amorphis — Our Road to Orbit
Two-slide PPTX. Each slide is a downward winding-road timeline with 6 milestones.
Slide 1: Aug 2021 → Sept 2023 (foundations + first SMA actuator)
Slide 2: Jan 2024 → May 2027  (deep eval + Amorphis launch)
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
NAVY      = RGBColor(0x05, 0x08, 0x10)
NAVY_2    = RGBColor(0x0A, 0x10, 0x20)
NAVY_3    = RGBColor(0x14, 0x1A, 0x2C)
CYAN      = RGBColor(0x7A, 0xE5, 0xFF)
CYAN_SOFT = RGBColor(0xC8, 0xF4, 0xFF)
WHITE     = RGBColor(0xEC, 0xF0, 0xF4)
STEEL     = RGBColor(0x98, 0xA0, 0xAA)
MUTED     = RGBColor(0x6A, 0x72, 0x80)

# ── DATA — split into two halves ────────────────────
MILESTONES = [
    ("Aug 2021",            "Global evaluation of SMA HDRM for Dhruva Space's satellite deployer system."),
    ("Aug 2021 – Mar 2022", "Conversations with vendors. Quotes ranged $5,000 – $10,000 per system."),
    ("Apr 2022",            "Decided to build our own Dhruva Space burn-wire mechanism for satellite separation. Successfully passed the ISRO review board."),
    ("Jan 2023",            "Co-wrote proposal for ISRO Human Spaceflight Programme (HSFC). EoI on using SMA actuators for module locking."),
    ("Feb 2023",            "Procured an engineering model of an SMA actuator from a European startup."),
    ("Sept 2023",           "Actuator delivery — vibration-qualified, thermo-vac tested European SMA actuator."),
    ("Jan 2024",            "Extensively evaluated the actuator. Damaged it — no actuation, over-current event."),
    ("Apr 2024",            "Ordered additional actuators and continued evaluation."),
    ("Aug 2024",            'Sankalp joined PhD on "SMA actuator design and development for space applications".'),
    ("Sept 2025",           "Kushagra worked with a space-robotics startup using super-elastic Nitinol wire for satellite capture."),
    ("May 2026",            "Amorphis established for development of sector-agnostic SMA actuators."),
    ("May 2027",            "First indigenous SMA actuator — market release."),
]

# ── HELPER: set line transparency via XML ───────────
def set_line_alpha(connector, alpha_percent):
    spPr = connector.line._get_or_add_ln()
    for child in spPr.findall(qn('a:solidFill')):
        spPr.remove(child)
    solidFill = etree.SubElement(spPr, qn('a:solidFill'))
    srgb = etree.SubElement(solidFill, qn('a:srgbClr'))
    srgb.set('val', '7AE5FF')
    alpha = etree.SubElement(srgb, qn('a:alpha'))
    alpha.set('val', str(int(alpha_percent * 1000)))

# ── PRESENTATION ────────────────────────────────────
prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)

def build_slide(slide_milestones, half_label, total_label, blob_side='left'):
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Background
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid(); bg.fill.fore_color.rgb = NAVY
    bg.line.fill.background()

    # Depth blob — varies per slide for visual variety
    if blob_side == 'left':
        blob = slide.shapes.add_shape(MSO_SHAPE.OVAL,
            Inches(-2), Inches(-2.5), Inches(8), Inches(8))
    else:
        blob = slide.shapes.add_shape(MSO_SHAPE.OVAL,
            Inches(13.333 - 6), Inches(-2.5), Inches(8), Inches(8))
    blob.fill.solid(); blob.fill.fore_color.rgb = NAVY_3
    blob.line.fill.background()

    # Top-right accent dot
    dot = slide.shapes.add_shape(MSO_SHAPE.OVAL,
        Inches(13.333 - 0.55), Inches(0.40), Inches(0.18), Inches(0.18))
    dot.fill.solid(); dot.fill.fore_color.rgb = CYAN
    dot.line.fill.background()

    # Title
    title = slide.shapes.add_textbox(Inches(0.6), Inches(0.30), Inches(12.1), Inches(0.55))
    tf = title.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.LEFT
    r = p.add_run()
    r.text = "OUR ROAD TO ORBIT"
    r.font.name = "Calibri"; r.font.size = Pt(34); r.font.bold = True
    r.font.color.rgb = WHITE
    r._r.get_or_add_rPr().set('spc', '300')

    # Subtitle
    sub = slide.shapes.add_textbox(Inches(0.6), Inches(0.86), Inches(12.1), Inches(0.32))
    tf = sub.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.LEFT
    r = p.add_run()
    r.text = f"{half_label}   ·   {total_label}   ·   AMORPHIS"
    r.font.name = "Consolas"; r.font.size = Pt(11)
    r.font.color.rgb = CYAN
    r._r.get_or_add_rPr().set('spc', '400')

    # Cyan rule
    rule = slide.shapes.add_connector(1, Inches(0.6), Inches(1.27), Inches(2.4), Inches(1.27))
    rule.line.color.rgb = CYAN; rule.line.width = Pt(1.5)

    # Timeline geometry — only 6 milestones per slide, plenty of room
    TIMELINE_TOP    = 1.70
    TIMELINE_BOTTOM = 7.05
    N = len(slide_milestones)
    ROW_GAP = (TIMELINE_BOTTOM - TIMELINE_TOP) / (N - 1)
    CENTER_X = 13.333 / 2
    WAVE_AMP = 1.05
    NODE_R = 0.20
    DOT_R  = 0.07

    nodes = []
    for k in range(N):
        y = TIMELINE_TOP + k * ROW_GAP
        phase = (k / (N - 1)) * math.pi * 1.6
        x = CENTER_X + math.sin(phase) * WAVE_AMP
        nodes.append((x, y))

    # Road — three-layer halo
    def draw_road(width_pt, alpha):
        samples = 18
        for k in range(N - 1):
            x1, y1 = nodes[k]; x2, y2 = nodes[k+1]
            for s in range(samples):
                t1 = s / samples; t2 = (s + 1) / samples
                ax = x1 + (x2-x1)*t1; ay = y1 + (y2-y1)*t1
                bx = x1 + (x2-x1)*t2; by = y1 + (y2-y1)*t2
                ln = slide.shapes.add_connector(1,
                    Inches(ax), Inches(ay), Inches(bx), Inches(by))
                ln.line.color.rgb = CYAN; ln.line.width = Pt(width_pt)
                if alpha < 100: set_line_alpha(ln, alpha)

    draw_road(12.0, 12)
    draw_road(6.0,  26)
    draw_road(2.0,  100)

    # Nodes — bigger, with index number inside
    for idx, (x, y) in enumerate(nodes, start=1 if half_label.startswith("PART 1") else 7):
        ring = slide.shapes.add_shape(MSO_SHAPE.OVAL,
            Inches(x - NODE_R), Inches(y - NODE_R),
            Inches(NODE_R*2), Inches(NODE_R*2))
        ring.fill.solid(); ring.fill.fore_color.rgb = NAVY
        ring.line.color.rgb = CYAN; ring.line.width = Pt(1.75)
        # Index number inside the node
        ntf = ring.text_frame
        ntf.margin_left = ntf.margin_right = ntf.margin_top = ntf.margin_bottom = 0
        np = ntf.paragraphs[0]; np.alignment = PP_ALIGN.CENTER
        nr = np.add_run(); nr.text = f"{idx:02d}"
        nr.font.name = "Consolas"; nr.font.size = Pt(10); nr.font.bold = True
        nr.font.color.rgb = CYAN_SOFT

    # Callouts
    TEXT_W = 4.7
    GAP    = 0.45
    for k, (x, y) in enumerate(nodes):
        date, body = slide_milestones[k]
        on_left = x >= CENTER_X
        if on_left:
            tx = x - NODE_R - GAP - TEXT_W
            align = PP_ALIGN.RIGHT
        else:
            tx = x + NODE_R + GAP
            align = PP_ALIGN.LEFT
        ty = y - 0.42

        # Pill
        pill_w = 2.10
        pill_h = 0.32
        pill_x = (tx + TEXT_W - pill_w) if on_left else tx
        pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(pill_x), Inches(ty), Inches(pill_w), Inches(pill_h))
        pill.fill.solid(); pill.fill.fore_color.rgb = NAVY_2
        pill.line.color.rgb = CYAN; pill.line.width = Pt(0.8)
        ptf = pill.text_frame
        ptf.margin_left = Inches(0.08); ptf.margin_right = Inches(0.08)
        ptf.margin_top = ptf.margin_bottom = Inches(0.02)
        ptf.word_wrap = False
        pp = ptf.paragraphs[0]; pp.alignment = PP_ALIGN.CENTER
        pr = pp.add_run(); pr.text = date
        pr.font.name = "Consolas"; pr.font.size = Pt(11); pr.font.bold = True
        pr.font.color.rgb = CYAN_SOFT
        pr._r.get_or_add_rPr().set('spc', '120')

        # Description — generous height now that we have 6 per slide
        desc = slide.shapes.add_textbox(
            Inches(tx), Inches(ty + 0.40),
            Inches(TEXT_W), Inches(0.50))
        dtf = desc.text_frame
        dtf.margin_left = dtf.margin_right = Inches(0.02)
        dtf.margin_top = dtf.margin_bottom = Inches(0)
        dtf.word_wrap = True
        dp = dtf.paragraphs[0]; dp.alignment = align
        dr = dp.add_run(); dr.text = body
        dr.font.name = "Calibri"; dr.font.size = Pt(12)
        dr.font.color.rgb = WHITE

    # Footer
    footer = slide.shapes.add_textbox(Inches(0.6), Inches(7.20), Inches(9), Inches(0.25))
    ftf = footer.text_frame
    ftf.margin_left = ftf.margin_right = ftf.margin_top = ftf.margin_bottom = 0
    fp = ftf.paragraphs[0]; fp.alignment = PP_ALIGN.LEFT
    fr = fp.add_run(); fr.text = "AMORPHIS · INDIA'S FIRST SPACE-GRADE SMA ACTUATOR COMPANY"
    fr.font.name = "Consolas"; fr.font.size = Pt(8); fr.font.color.rgb = MUTED
    fr._r.get_or_add_rPr().set('spc', '500')

    credit = slide.shapes.add_textbox(Inches(9.5), Inches(7.20), Inches(3.5), Inches(0.25))
    ctf = credit.text_frame
    ctf.margin_left = ctf.margin_right = ctf.margin_top = ctf.margin_bottom = 0
    cp = ctf.paragraphs[0]; cp.alignment = PP_ALIGN.RIGHT
    cr = cp.add_run(); cr.text = half_label
    cr.font.name = "Consolas"; cr.font.size = Pt(8); cr.font.color.rgb = STEEL
    cr._r.get_or_add_rPr().set('spc', '500')

build_slide(MILESTONES[:6], "PART 1 / 2", "AUG 2021 → SEPT 2023", blob_side='left')
build_slide(MILESTONES[6:], "PART 2 / 2", "JAN 2024 → MAY 2027", blob_side='right')

OUT = os.path.join(os.path.dirname(__file__), '..', 'Amorphis-Timeline.pptx')
prs.save(OUT)
print(f'Saved: {OUT}')
print(f'Slides: {len(prs.slides)}')
