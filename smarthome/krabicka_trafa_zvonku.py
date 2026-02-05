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
    # Create bottom rectangle wire at Z=0
    bottom_wire = wp.rect(width, depth).wire().val()

    # Define top polygon with varying heights:
    # - Sides parallel to Y-axis (X=-50 and X=50): Z=50 (shorter side, width=100)
    # - Sides parallel to X-axis (Y=75 and Y=-50): Z=100 (longer side, depth=150)
    # Interpolate corner heights: Z is average of heights at X and Y positions
    top_points = [
        Vector(-50, 75, 60),  # Left top: X=-50 (Z=50) and Y=75 (Z=100) -> avg=75
        Vector(50, 75, 60),  # Right top: X=50 (Z=50) and Y=75 (Z=100) -> avg=75
        Vector(
            25, -50, 30
        ),  # Right bottom: Y=-50 (Z=100), X=25 (25% from Z=50) -> avg=87.5
        Vector(
            -25, -50, 30
        ),  # Left bottom: Y=-50 (Z=100), X=-25 (25% from Z=50) -> avg=87.5
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

    # Apply fillet BEFORE hollowing (on solid outer surface)
    # Use r=5 for all edges as it's the maximum reliable radius
    #solid = solid.edges().filter(lambda e: e.Center().z > 0).fillet(5)
    
   # Apply fillet (r=24): exclude base edges (z=0) and far Y edges (y=75)
    solid = (
        solid.edges()
        .filter(lambda e: e.Center().z > 0 and e.Center().y != 75)
        .fillet(43)
    )
    # Apply smaller fillet (r=5) to far Y edges (y=75, excluding base)
    solid = (
        solid.edges()
        .filter(lambda e: e.Center().z > 0 and e.Center().y == 75)
        .fillet(5)
    )

        
    # When faces are selected before shell(), they are removed during shelling
    solid = solid.faces("<Z").shell(WALL_THICKNESS)

    return solid


def main():
    """Main workflow."""
    # render tapered prism (10x10 -> 10x2)
    tapered = build_tapered_prism()
    render(tapered, "tapered_prism.stl")


if __name__ == "__main__":
    main()
