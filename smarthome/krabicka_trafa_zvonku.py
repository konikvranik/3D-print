import sys
import os

import cadquery as cq
from cadquery import Edge, Wire, Vector, Solid
from ocp_vscode import (
    show,
    show_object,
    reset_show,
    set_port,
    set_defaults,
    get_defaults,
)

set_port(3939)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import render

width = 100
height = 60
depth = 150
WALL_THICKNESS = 3


def build_tapered_prism():
    """Create a prism that starts as 10x10 and tapers to 10x2 over a height.

    Uses a loft between two centered rectangles.
    """
    wp = cq.Workplane("XY")
    bottom_wire = wp.rect(width, depth).wire().val()
    top_points = [
        Vector(-width / 2, depth / 2, height),  # Left top
        Vector(width / 2, depth / 2, height),  # Right top
        Vector(25, -50, 30),  # Right bottom
        Vector(-25, -50, 30),  # Left bottom
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
        .fillet(15)
    )
    solid = (
        solid.edges()
        .filter(lambda e: e.Center().z > 0 and e.Center().y == 75)
        .fillet(5)
    )

    solid = solid.faces("<Z").shell(WALL_THICKNESS)

    return solid


def main():
    """Main workflow."""
    # render tapered prism (10x10 -> 10x2)
    tapered = build_tapered_prism()
    render(tapered, "tapered_prism.stl")


if __name__ == "__main__":
    main()
