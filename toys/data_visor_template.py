# -*- coding: utf-8 -*-
"""Lieutenant Commander Data VISOR glasses template for 3D pen.

Generates a 1:1 scale PDF template with flat parts that a child can trace
with a 3D pen, then assemble into sci-fi glasses.

Sized for a ~9 year old (face width ~115mm).

Parts:
  1. Main VISOR band (the iconic eye piece)
  2. Left temple arm
  3. Right temple arm
  4. Nose bridge connector

Usage:
    python3 toys/data_visor_template.py
"""

import os

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black, gray, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register fonts with Czech diacritics support
pdfmetrics.registerFont(
    TTFont("Sans", "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf")
)
pdfmetrics.registerFont(
    TTFont("SansBold", "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf")
)

# ---------------------------------------------------------------------------
# Dimensions – all values in mm, converted to points (reportlab unit) below
# ---------------------------------------------------------------------------
PAGE_W, PAGE_H = A4  # already in points (595 x 842)

# Main VISOR band – 115mm fits a 9-year-old
VISOR_OUTER_W = 115 * mm
VISOR_OUTER_H = 35 * mm
VISOR_INNER_W = 95 * mm  # eye opening
VISOR_INNER_H = 20 * mm  # eye opening
VISOR_CORNER_R = 6 * mm

# Nose bridge
BRIDGE_W = 15 * mm
BRIDGE_H = 8 * mm
BRIDGE_TAB = 5 * mm

# Temple arms
ARM_LENGTH = 115 * mm
ARM_WIDTH = 6 * mm
ARM_HOOK_R = 10 * mm

# Hinge tabs on visor (where arms attach)
HINGE_TAB_W = 8 * mm
HINGE_TAB_H = 6 * mm


def draw_rounded_rect(
    c: canvas.Canvas, x: float, y: float, w: float, h: float, r: float
):
    """Draw a rounded rectangle outline at (x, y)."""
    c.roundRect(x, y, w, h, r, fill=0, stroke=1)


def draw_visor(c: canvas.Canvas, cx: float, cy: float):
    """Draw the main VISOR band centered at (cx, cy)."""
    # Outer band
    ox = cx - VISOR_OUTER_W / 2
    oy = cy - VISOR_OUTER_H / 2
    draw_rounded_rect(c, ox, oy, VISOR_OUTER_W, VISOR_OUTER_H, VISOR_CORNER_R)

    # Inner eye slot – solid thin line (shows where NOT to fill)
    ix = cx - VISOR_INNER_W / 2
    iy = cy - VISOR_INNER_H / 2
    c.setLineWidth(0.5)
    c.setStrokeColor(gray)
    draw_rounded_rect(c, ix, iy, VISOR_INNER_W, VISOR_INNER_H, VISOR_CORNER_R - 1 * mm)
    c.setStrokeColor(black)
    c.setLineWidth(0.7)

    # Decorative horizontal stripes (Data's VISOR detail)
    stripe_count = 5
    stripe_spacing = VISOR_INNER_H / (stripe_count + 1)
    c.setStrokeColor(gray)
    c.setLineWidth(0.3)
    for i in range(1, stripe_count + 1):
        sy = iy + i * stripe_spacing
        c.line(ix + 3 * mm, sy, ix + VISOR_INNER_W / 2 - 4 * mm, sy)
        c.line(ix + VISOR_INNER_W / 2 + 4 * mm, sy, ix + VISOR_INNER_W - 3 * mm, sy)
    c.setStrokeColor(black)
    c.setLineWidth(0.7)

    # Left hinge tab
    lx = ox - HINGE_TAB_W
    ly = cy - HINGE_TAB_H / 2
    c.rect(lx, ly, HINGE_TAB_W, HINGE_TAB_H, fill=0, stroke=1)
    c.setDash(3, 2)
    c.line(lx + HINGE_TAB_W, ly, lx + HINGE_TAB_W, ly + HINGE_TAB_H)
    c.setDash()

    # Right hinge tab
    rx = ox + VISOR_OUTER_W
    ry = cy - HINGE_TAB_H / 2
    c.rect(rx, ry, HINGE_TAB_W, HINGE_TAB_H, fill=0, stroke=1)
    c.setDash(3, 2)
    c.line(rx, ry, rx, ry + HINGE_TAB_H)
    c.setDash()

    # Label
    c.setFont("Sans", 7)
    c.drawCentredString(
        cx, oy - 7 * mm, "1x HLAVNI VISOR (obkresli plny obrys, sede vynechej)"
    )


def draw_temple_arm(c: canvas.Canvas, x: float, y: float, mirror: bool = False):
    """Draw a temple arm starting at (x, y). Ear hook curves at the end."""
    d = -1 if mirror else 1

    p = c.beginPath()
    # Outer edge (top) – straight section
    p.moveTo(x, y + ARM_WIDTH)
    p.lineTo(x + d * ARM_LENGTH, y + ARM_WIDTH)

    # Ear hook curve (outer edge)
    hook_steps = 10
    for i in range(1, hook_steps + 1):
        t = i / hook_steps
        hx = x + d * ARM_LENGTH + d * ARM_HOOK_R * (1 - (1 - t**2) ** 0.5)
        hy = y + ARM_WIDTH - ARM_HOOK_R * t
        p.lineTo(hx, hy)

    # Inner edge of hook (going back, thinner)
    inner_w = ARM_WIDTH * 0.5
    for i in range(hook_steps, -1, -1):
        t = i / hook_steps
        hx = x + d * ARM_LENGTH + d * ARM_HOOK_R * (1 - (1 - t**2) ** 0.5)
        hy = y + ARM_WIDTH - ARM_HOOK_R * t - inner_w
        p.lineTo(hx, hy)

    # Back along straight section (inner edge)
    p.lineTo(x, y)
    p.close()

    c.drawPath(p, fill=0, stroke=1)

    # Hinge fold line
    c.setDash(3, 2)
    c.line(x + d * 4 * mm, y, x + d * 4 * mm, y + ARM_WIDTH)
    c.setDash()

    # Alignment dot
    c.circle(x + d * 6 * mm, y + ARM_WIDTH / 2, 1.5 * mm, fill=1, stroke=0)

    label = "1x PRAVE RAMINKO" if not mirror else "1x LEVE RAMINKO"
    c.setFont("Sans", 7)
    c.drawCentredString(x + d * ARM_LENGTH / 2, y - 7 * mm, label)


def draw_nose_bridge(c: canvas.Canvas, cx: float, cy: float):
    """Draw nose bridge connector – curved piece with side tabs."""
    p = c.beginPath()

    p.moveTo(cx - BRIDGE_W / 2 - BRIDGE_TAB, cy - 2 * mm)
    p.lineTo(cx - BRIDGE_W / 2 - BRIDGE_TAB, cy + 2 * mm)
    p.lineTo(cx - BRIDGE_W / 2, cy + 2 * mm)
    # Curve over the nose
    p.curveTo(
        cx - BRIDGE_W / 4,
        cy + BRIDGE_H,
        cx + BRIDGE_W / 4,
        cy + BRIDGE_H,
        cx + BRIDGE_W / 2,
        cy + 2 * mm,
    )
    # Right tab
    p.lineTo(cx + BRIDGE_W / 2 + BRIDGE_TAB, cy + 2 * mm)
    p.lineTo(cx + BRIDGE_W / 2 + BRIDGE_TAB, cy - 2 * mm)
    p.lineTo(cx + BRIDGE_W / 2, cy - 2 * mm)
    # Curve back
    p.curveTo(
        cx + BRIDGE_W / 4,
        cy + BRIDGE_H - 5 * mm,
        cx - BRIDGE_W / 4,
        cy + BRIDGE_H - 5 * mm,
        cx - BRIDGE_W / 2,
        cy - 2 * mm,
    )
    p.close()

    c.drawPath(p, fill=0, stroke=1)

    # Fold lines for tabs
    c.setDash(3, 2)
    c.line(cx - BRIDGE_W / 2, cy - 2 * mm, cx - BRIDGE_W / 2, cy + 2 * mm)
    c.line(cx + BRIDGE_W / 2, cy - 2 * mm, cx + BRIDGE_W / 2, cy + 2 * mm)
    c.setDash()

    c.setFont("Sans", 7)
    c.drawCentredString(cx, cy - 8 * mm, "1x NOSNI MUSTEK")


def draw_assembly_diagram(c: canvas.Canvas, x: float, y: float):
    """Draw assembly instructions."""
    c.setFont("SansBold", 9)
    c.drawString(x, y, "SKLADBA:")
    c.setFont("Sans", 7)

    instructions = [
        "1. Obkresli vsechny dily 3D perem podél plnych obrysovych car",
        "2. Carkovane carecky = mista pro ohyb / pripojeni dilo (priloze a pritav)",
        "3. Sedivy obrys uvnitr visoru = vyrez pro oci (vynech vypln)",
        "4. Raminka pripoj k boecnim zalozkam visoru",
        "5. Nosni mustek pripoj zespodu do stredu visoru",
    ]
    for i, line in enumerate(instructions):
        c.drawString(x, y - 12 * mm - i * 6 * mm, line)


def main():
    """Generate the PDF template."""
    output_path = os.path.splitext(os.path.abspath(__file__))[0] + ".pdf"

    c = canvas.Canvas(output_path, pagesize=A4)
    c.setTitle("Data VISOR - Sablona pro 3D pero (9 let)")
    c.setAuthor("3D-print repo")

    # Header
    c.setFont("SansBold", 16)
    c.drawCentredString(
        PAGE_W / 2, PAGE_H - 20 * mm, "DATA VISOR - Sablona pro 3D pero"
    )
    c.setFont("Sans", 9)
    c.drawCentredString(
        PAGE_W / 2,
        PAGE_H - 27 * mm,
        "Meritko 1:1  |  Pro cca 9lete ditetko  |  Vytiskni BEZ zmeny meritka",
    )

    # Scale reference bar (50mm)
    bar_y = PAGE_H - 34 * mm
    bar_x = PAGE_W / 2 - 25 * mm
    c.setLineWidth(1.5)
    c.line(bar_x, bar_y, bar_x + 50 * mm, bar_y)
    c.line(bar_x, bar_y - 2 * mm, bar_x, bar_y + 2 * mm)
    c.line(bar_x + 50 * mm, bar_y - 2 * mm, bar_x + 50 * mm, bar_y + 2 * mm)
    c.setFont("Sans", 7)
    c.drawCentredString(
        PAGE_W / 2, bar_y - 5 * mm, "50 mm - zkontroluj meritko po vytisteni!"
    )
    c.setLineWidth(0.7)

    # VISOR
    c.setLineWidth(0.7)
    draw_visor(c, PAGE_W / 2, PAGE_H - 85 * mm)

    # Nose bridge
    draw_nose_bridge(c, PAGE_W / 2, PAGE_H - 130 * mm)

    # Temple arms
    draw_temple_arm(c, 25 * mm, PAGE_H - 175 * mm, mirror=False)
    draw_temple_arm(c, PAGE_W - 25 * mm, PAGE_H - 220 * mm, mirror=True)

    # Assembly instructions
    draw_assembly_diagram(c, 25 * mm, 55 * mm)

    # Footer
    c.setFont("Sans", 6)
    c.drawCentredString(
        PAGE_W / 2,
        12 * mm,
        "Pokud je meritko spravne, rozměr mezi svislými carami vyse = presne 50 mm.",
    )

    c.save()
    print(f"PDF saved: {output_path}")


if __name__ == "__main__":
    main()
