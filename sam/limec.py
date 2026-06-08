import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import render, cq
import math
from cadquery import selectors

THICK = 20
WIDTH = 280
SAGITA = 90
HEIGHT = 60

HOLE_DIAMETER = 3  # screw holes in the bottom plate
HOLE_COUNT = 6     # number of holes along the sagittaArc
HOLE_MARGIN = 0.08  # margin from arc edges as fraction of arc length


def arc_hole_points(count: int) -> list:
    """Vypočítá body pro díry podél oblouku spodního plátu.

    Rovnoměrně rozmístí `count` děr podél oblouku s mezerou od okrajů.

    Args:
        count: Počet děr rovnoměrně rozmístěných podél oblouku.

    Returns:
        Seznam (x, y) souřadnic středů děr.
    """
    chord = WIDTH
    r = (SAGITA ** 2 + (chord / 2) ** 2) / (2 * SAGITA)
    # Place holes in the middle of the plate band with margin from both edges
    # Inner edge of plate band is ~100mm from outer arc center, outer edge at r=113.75
    # r - THICK*0.55 ≈ 102.75 gives ~2.75mm margin from inner edge and ~11mm from outer edge
    r_hole = r - THICK * 0.55
    cx = chord / 2
    cy = SAGITA - r
    a_start = math.atan2(0 - cy, 0 - cx)
    a_end = math.atan2(0 - cy, chord - cx)
    points = []
    for i in range(count):
        t = HOLE_MARGIN + i * (1 - 2 * HOLE_MARGIN) / (count - 1)
        angle = a_start + t * (a_end - a_start)
        x = cx + r_hole * math.cos(angle)
        y = cy + r_hole * math.sin(angle)
        points.append((x, -y))
    return points


def build_body():
    """Vytvoří model límce z CyberPunku s konstantní tloušťkou.
    """

    body = (cq.Workplane("XY")
            .moveTo(0, 0)
            .sagittaArc((WIDTH, 0), SAGITA)
            .offset2D(THICK / 2, kind='intersection')
            .extrude(HEIGHT).fillet(9)
            .workplane(offset=-HEIGHT / 2)
            .moveTo(0, 0)
            .sagittaArc((WIDTH, 0), SAGITA)
            .line(-15, 0)
            .sagittaArc((15, 0), -SAGITA+15).close()
            .extrude(2)
            .edges("|Z").fillet(10))
    body = body.edges(selectors.BoxSelector((-1000, -1000, 1.9), (1000, 1000, 2.1))).edges("#Z").fillet(1)

    # screw holes along the sagittaArc in the bottom plate
    holes = arc_hole_points(HOLE_COUNT)
    body = (body.faces("<Z")
            .workplane()
            .pushPoints(holes)
            .circle(HOLE_DIAMETER / 2)
            .cutBlind(-2))

    return body


def main():
    """Hlavní workflow."""
    render(build_body(), "limec.stl")


if __name__ == "__main__":
    main()
