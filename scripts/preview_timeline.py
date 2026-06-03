"""Render 1600x900 PNG previews of the 2-slide timeline PPTX."""
import os, math
from PIL import Image, ImageDraw, ImageFont

SLIDE_W_IN = 13.333
SLIDE_H_IN = 7.5
SCALE = 120

W = int(SLIDE_W_IN * SCALE)
H = int(SLIDE_H_IN * SCALE)
def i(v): return int(v * SCALE)

NAVY      = (0x05, 0x08, 0x10)
NAVY_2    = (0x0A, 0x10, 0x20)
NAVY_3    = (0x14, 0x1A, 0x2C)
CYAN      = (0x7A, 0xE5, 0xFF)
CYAN_SOFT = (0xC8, 0xF4, 0xFF)
WHITE     = (0xEC, 0xF0, 0xF4)
STEEL     = (0x98, 0xA0, 0xAA)
MUTED     = (0x6A, 0x72, 0x80)

def F(size, bold=False, mono=False):
    name = ('consola.ttf' if not bold else 'consolab.ttf') if mono else \
           ('calibrib.ttf' if bold else 'calibri.ttf')
    try:
        return ImageFont.truetype(name, size)
    except OSError:
        return ImageFont.load_default()

title_font = F(int(34 * 1.33), bold=True)
sub_font   = F(int(11 * 1.33), mono=True)
date_font  = F(int(11 * 1.33), bold=True, mono=True)
body_font  = F(int(12 * 1.33))
num_font   = F(int(10 * 1.33), bold=True, mono=True)
foot_font  = F(int(8 * 1.33), mono=True)

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

def wrap(draw, text, font, max_w_px):
    words = text.split()
    lines, cur = [], ''
    for w in words:
        test = (cur + ' ' + w).strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] > max_w_px and cur:
            lines.append(cur); cur = w
        else:
            cur = test
    if cur: lines.append(cur)
    return lines

def render_slide(milestones, half_label, total_label, blob_side, idx_start, out_path):
    img = Image.new('RGB', (W, H), NAVY)
    draw = ImageDraw.Draw(img, 'RGBA')

    if blob_side == 'left':
        draw.ellipse((i(-2), i(-2.5), i(6), i(5.5)), fill=NAVY_3)
    else:
        draw.ellipse((i(13.333 - 6), i(-2.5), i(13.333 + 2), i(5.5)), fill=NAVY_3)

    draw.text((i(0.6), i(0.30)), "OUR ROAD TO ORBIT", font=title_font, fill=WHITE)
    draw.text((i(0.6), i(0.86)),
              f"{half_label}   ·   {total_label}   ·   AMORPHIS",
              font=sub_font, fill=CYAN)
    draw.line((i(0.6), i(1.27), i(2.4), i(1.27)), fill=CYAN, width=2)
    draw.ellipse((i(13.333 - 0.55), i(0.40), i(13.333 - 0.37), i(0.58)), fill=CYAN)

    TIMELINE_TOP    = 1.70
    TIMELINE_BOTTOM = 7.05
    N = len(milestones)
    ROW_GAP = (TIMELINE_BOTTOM - TIMELINE_TOP) / (N - 1)
    CENTER_X = SLIDE_W_IN / 2
    WAVE_AMP = 1.05
    NODE_R = 0.20
    DOT_R  = 0.07

    nodes = []
    for k in range(N):
        y = TIMELINE_TOP + k * ROW_GAP
        phase = (k / (N - 1)) * math.pi * 1.6
        x = CENTER_X + math.sin(phase) * WAVE_AMP
        nodes.append((x, y))

    def draw_road(width_px, alpha):
        samples = 18
        for k in range(N - 1):
            x1, y1 = nodes[k]; x2, y2 = nodes[k+1]
            for s in range(samples):
                t1 = s / samples; t2 = (s + 1) / samples
                ax = x1 + (x2-x1)*t1; ay = y1 + (y2-y1)*t1
                bx = x1 + (x2-x1)*t2; by = y1 + (y2-y1)*t2
                draw.line((i(ax), i(ay), i(bx), i(by)),
                          fill=CYAN + (alpha,), width=width_px)

    draw_road(int(12 * 1.33), 30)
    draw_road(int(6  * 1.33), 65)
    draw_road(int(2  * 1.33), 255)

    for k, (x, y) in enumerate(nodes):
        draw.ellipse((i(x-NODE_R), i(y-NODE_R), i(x+NODE_R), i(y+NODE_R)),
                     fill=NAVY, outline=CYAN, width=2)
        num = f"{idx_start + k:02d}"
        bbox = draw.textbbox((0, 0), num, font=num_font)
        nw, nh = bbox[2]-bbox[0], bbox[3]-bbox[1]
        draw.text((i(x) - nw // 2, i(y) - nh // 2 - 2),
                  num, font=num_font, fill=CYAN_SOFT)

    TEXT_W = 4.7
    GAP    = 0.45
    for k, (x, y) in enumerate(nodes):
        date, body = milestones[k]
        on_left = x >= CENTER_X
        if on_left:
            tx = x - NODE_R - GAP - TEXT_W
            align_right = True
        else:
            tx = x + NODE_R + GAP
            align_right = False
        ty = y - 0.42

        pill_w, pill_h = 2.10, 0.32
        pill_x = (tx + TEXT_W - pill_w) if on_left else tx
        draw.rounded_rectangle((i(pill_x), i(ty), i(pill_x+pill_w), i(ty+pill_h)),
                               radius=int(0.06 * SCALE),
                               fill=NAVY_2, outline=CYAN, width=1)
        bbox = draw.textbbox((0, 0), date, font=date_font)
        tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
        draw.text((i(pill_x) + (i(pill_w) - tw) // 2,
                   i(ty) + (i(pill_h) - th) // 2 - 2),
                  date, font=date_font, fill=CYAN_SOFT)

        max_w_px = i(TEXT_W) - 4
        lines = wrap(draw, body, body_font, max_w_px)
        line_h = body_font.size + 4
        for li, line in enumerate(lines):
            if align_right:
                bbox = draw.textbbox((0, 0), line, font=body_font)
                lw = bbox[2]-bbox[0]
                draw.text((i(tx + TEXT_W) - lw - 2, i(ty + 0.40) + li * line_h),
                          line, font=body_font, fill=WHITE)
            else:
                draw.text((i(tx) + 2, i(ty + 0.40) + li * line_h),
                          line, font=body_font, fill=WHITE)

    draw.text((i(0.6), i(7.20)),
              "AMORPHIS · INDIA'S FIRST SPACE-GRADE SMA ACTUATOR COMPANY",
              font=foot_font, fill=MUTED)
    draw.text((i(11.0), i(7.20)),
              half_label, font=foot_font, fill=STEEL)

    img.save(out_path, 'PNG')
    print(f'Saved: {out_path}')

OUT_DIR = os.path.join(os.path.dirname(__file__), '..')
render_slide(MILESTONES[:6], "PART 1 / 2", "AUG 2021 → SEPT 2023",
             'left',  1, os.path.join(OUT_DIR, 'timeline-preview-1.png'))
render_slide(MILESTONES[6:], "PART 2 / 2", "JAN 2024 → MAY 2027",
             'right', 7, os.path.join(OUT_DIR, 'timeline-preview-2.png'))
