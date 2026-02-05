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
bottom_height = 40
depth = 150
WALL_THICKNESS = 3

small_case_width = 40
small_case_holes_distance = 80
small_case_height = 10

screw_hole_diameter = 3.2  # For M3 screws
screw_hole_head_diameter = 5.5  # For M3 screws


def build_small_case():
    """Create a small box with holes for mounting.

    The box is a rectangular prism with specified width and depth,
    and has mounting holes on the sides.
    """
    wp = cq.Workplane("XY")
    solid = wp.box(
        small_case_width,
        small_case_holes_distance + 40,
        small_case_height,
        centered=(True, True, False),
    )

    wp = cq.Workplane("XY")
    wp = wp.polyline(
        [
            (small_case_width / 2, -small_case_holes_distance / 2 - 20),
            (
                small_case_width / 2,
                small_case_holes_distance / 2
                + screw_hole_head_diameter / 2
                + WALL_THICKNESS,
            ),
            (-small_case_width / 2, -small_case_holes_distance / 2 - 20),
            (
                small_case_width / 2 - 5,
                small_case_holes_distance / 2
                + screw_hole_head_diameter / 2
                + WALL_THICKNESS,
            ),
        ]
    ).close()
    wp = (
        wp.workplane(offset=small_case_height)
        .polyline(
            [
                (small_case_width / 2, -small_case_holes_distance / 2 - 20),
                (
                    small_case_width / 2,
                    small_case_holes_distance / 2
                    + screw_hole_head_diameter / 2
                    + WALL_THICKNESS,
                ),
                (-small_case_width / 2, -small_case_holes_distance / 2 - 20),
                (
                    small_case_width / 2 - 5,
                    small_case_holes_distance / 2
                    + screw_hole_head_diameter / 2
                    + WALL_THICKNESS,
                ),
            ]
        )
        .close()
    )

    # Use Solid.makeLoft() for non-planar loft
    solid = wp.loft()

    # solid = (
    #     solid.edges().filter(lambda e: e.Center().z > 0).fillet(small_case_height - 0.1)
    # )
    solid = solid.faces("<Z").shell(WALL_THICKNESS)

    # Create mounting holes
    hole_radius = screw_hole_diameter / 2  # For M3 screws
    hole_offset_y = small_case_holes_distance / 2

    for y in [-hole_offset_y, hole_offset_y]:
        x_offset = small_case_width / 2 - screw_hole_head_diameter / 2

        screw_slot = (
            cq.Workplane("XY")
            .cylinder(
                small_case_height,
                screw_hole_head_diameter / 2 + WALL_THICKNESS,
                centered=(True, True, False),
            )
            .translate((x_offset, y, 0))
        )

        repeat_to_cut = 5
        for i in range(repeat_to_cut):
            screw_slot = (
                screw_slot.cut(solid).translate((-WALL_THICKNESS, 0, 0)).cut(solid)
            )
        screw_slot = screw_slot.translate(((repeat_to_cut) * WALL_THICKNESS, 0, 0))

        solid = solid.union(screw_slot)
        solid = (
            solid.moveTo(x_offset, y)
            .circle(hole_radius)
            .cutThruAll()
            .workplane(offset=-WALL_THICKNESS * 2)
            .moveTo(x_offset, y)
            .circle(screw_hole_head_diameter / 2)
            .cutBlind(small_case_height)
        )

    return solid


def build_main_case():
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
        .fillet(20)
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
    cylinder_radius = screw_hole_head_diameter / 2 + WALL_THICKNESS
    screw_slot = (
        cq.Workplane("XY")
        .cylinder(bottom_height / 2, cylinder_radius, centered=(True, True, False))
        .translate((direction * (top_width / 2 - cylinder_radius), 0, 0))
    )

    repeat_to_cut = 5
    for i in range(repeat_to_cut):
        screw_slot = (
            screw_slot.cut(solid)
            .translate((-direction * WALL_THICKNESS, 0, 0))
            .cut(solid)
        )
    screw_slot = screw_slot.translate(
        (direction * (repeat_to_cut + 1) * WALL_THICKNESS, 0, 0)
    )

    return (
        solid.union(screw_slot)
        .faces("<Z")
        .workplane()
        .moveTo(direction * (top_width / 2 - cylinder_radius + WALL_THICKNESS), 0)
        .circle(screw_hole_diameter / 2)
        .cutThruAll()
        .faces("<Z")
        .workplane(offset=-WALL_THICKNESS * 2)
        .moveTo(direction * (top_width / 2 - cylinder_radius + WALL_THICKNESS), 0)
        .circle(screw_hole_head_diameter / 2)
        .cutBlind(-top_height)
    )


if __name__ == "__main__":
    # render(build_main_case())
    render(build_small_case())
