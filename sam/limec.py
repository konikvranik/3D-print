import os
import selectors
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import render, cq
import math
from cadquery import Workplane, selectors

THICK = 20
WIDTH = 280
SAGITA = 90
HEIGHT = 60

HOLE_DIAMETER = 3  # screw holes in the bottom plate
HOLE_COUNT = 6  # number of holes along the sagittaArc
HOLE_MARGIN = 0.08  # margin from arc edges as fraction of arc length


def build_bottom_body():
    """Vytvoří model límce z CyberPunku s konstantní tloušťkou.
    """
    body = cq.Workplane("XY")
    bottom_height = HEIGHT * 3 / 5
    body = bottom_body(body, bottom_height)
    body = body.workplane(offset=-bottom_height / 2)
    body = bottom_plate(body)
    return body


def bottom_body(workplane: Workplane, bottom_height: float) -> Workplane:
    workplane = workplane.moveTo(0, 0)
    workplane = workplane.sagittaArc((WIDTH, 0), SAGITA)
    workplane = workplane.offset2D(THICK / 2, kind='intersection')
    workplane = workplane.extrude(bottom_height)
    workplane = workplane.edges("<Z")
    workplane = workplane.fillet(9)
    return workplane


def bottom_plate(body: Workplane) -> Workplane:
    plate_height = 2
    body = (body
            .workplane(offset=-plate_height / 2 + .2)
            .moveTo(0, 0)
            .sagittaArc((WIDTH, 0), SAGITA)
            .line(-15, 0)
            .sagittaArc((15, 0), -SAGITA + 15).close()
            .extrude(plate_height))
    body = screw_holes(body)
    body = body.edges("|Z").fillet(10)
    body = (body
            .edges(selectors.BoxSelector((-1000, -1000, 1.9), (1000, 1000, 2.1)))
            .edges("#Z")
            .fillet(1))
    return body


def screw_holes(body: Workplane) -> Workplane:
    # screw holes along the sagittaArc in the bottom plate
    holes = arc_hole_points(HOLE_COUNT)
    body = (body.faces("<Z")
            .workplane()
            .pushPoints(holes)
            .circle(HOLE_DIAMETER / 2)
            .cutBlind(-2))
    return body


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


def build_top_body():
    """Vytvoří model límce z CyberPunku s konstantní tloušťkou.
    """
    body = cq.Workplane("XY")
    top_height = HEIGHT * 2 / 5
    body = inset(body, HEIGHT * 1 / 5)
    body = top_body(body, top_height)
    body = body.clean()
    body = body.faces(">Z[-2]").fillet(.5)
    return body


def inset(body, top_height):
    body = (body
            .moveTo(0, 0)
            .sagittaArc((WIDTH, 0), SAGITA)
            .offset2D(THICK / 2 - .6 * 1.2, kind='intersection')
            .extrude(top_height)
            .faces(">Z")
            .workplane()
            )
    return body


def top_body(workplane: Workplane, top_height) -> Workplane:
    return (workplane
            .moveTo(0, 0)
            .sagittaArc((WIDTH, 0), SAGITA)
            .offset2D(THICK / 2, kind='intersection')
            .extrude(top_height)
            .edges(">Z")
            .fillet(9)
            )


def main():
    """Hlavní workflow."""
    render(build_bottom_body(), "limec_bottom.stl")
    render(build_top_body(), "limec_top.stl")


if __name__ == "__main__":
    main()
