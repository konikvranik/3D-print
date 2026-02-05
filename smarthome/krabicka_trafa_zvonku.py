import sys
import os

import cadquery as cq
from cadquery import Edge, Wire, Vector, Solid
from ocp_vscode import set_port

set_port(3939)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import render

top_width = 100
bottom_width = 30
top_height = 60
bottom_height = 30
depth = 150
WALL_THICKNESS = 3


def build_tapered_prism():
    """Create a prism that starts as 10x10 and tapers to 10x2 over a height.

    Uses a loft between two centered rectangles.
    """
    wp = cq.Workplane("XY")
    bottom_wire = wp.rect(top_width, depth).wire().val()
    top_points = [
        (-top_width / 2, depth / 2, top_height),  # Left top
        (top_width / 2, depth / 2, top_height),  # Right top
        (bottom_width / 2, -depth / 2 * 0.7, bottom_height),  # Right bottom
        (-bottom_width / 2, -depth / 2 * 0.7, bottom_height),  # Left bottom
    ]
    # Create edges and wire for top polygon
    edges = []
    for i in range(len(top_points)):
        p1 = top_points[i]
        p2 = top_points[(i + 1) % len(top_points)]
        edges.append(Edge.makeLine(p1, p2))
    top_wire = Wire.assembleEdges(edges)

    # Use Solid.makeLoft() for non-planar loft
    outer_solid = Solid.makeLoft([bottom_wire, top_wire])
    solid = cq.Workplane(obj=outer_solid)

    solid = (
        solid.edges()
        .filter(lambda e: e.Center().z > 0 and e.Center().y != 75)
        .fillet(24)
    )
    solid = (
        solid.edges()
        .filter(lambda e: e.Center().z > 0 and e.Center().y == 75)
        .fillet(5)
    )

    solid = solid.faces("<Z").shell(WALL_THICKNESS)

    solid = cylinder_hole(solid, -1)
    solid = cylinder_hole(solid, 1)

    return solid


def cylinder_hole(solid, direction):
    return (
        solid.union(
            cq.Workplane("XY")
            .cylinder(bottom_height, 5, centered=(True, True, False))
            .translate((direction * (top_width / 2 - 5), 0, 0))
            .cut(solid)
            .translate((direction * WALL_THICKNESS, 0, 0))
        )
        .faces("<Z")
        .workplane()
        .moveTo(direction * (top_width / 2 - 5 + WALL_THICKNESS), 0)
        .circle(1.6)
        .cutThruAll()
        .faces("<Z")
        .workplane(offset=-WALL_THICKNESS * 2)
        .moveTo(direction * (top_width / 2 - 5 + WALL_THICKNESS), 0)
        .circle(3)
        .cutBlind(-top_height)
    )


if __name__ == "__main__":
    render(build_tapered_prism())
