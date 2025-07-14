import os

import cadquery as cq
from cadquery import Workplane

from common import render

# --- Environment setup ---
os.environ["FONTCONFIG_FILE"] = "/etc/fonts/fonts.conf"
os.environ["FONTCONFIG_PATH"] = "/etc/fonts/"

# --- Dimensions ---
WIDTH = 90
HEIGHT = 165
BOARD_THICKNESS = 1.45
DEPTH = 16.7 - BOARD_THICKNESS
BOTTOM_HEIGHT = 4 - BOARD_THICKNESS
WALL_THICKNESS = 1.5

# --- Mounting holes ---
HOLE_DISTANCE = 81.5
HOLE_BORDER_OFFSET = 3.7
HOLE_DIAMETER = 2.75

# --- Slot and cutout parameters ---
SLOT_WIDTH = 0.5
SLOT_SPACING = 15 + 1.5
SLOT_START_OFFSET = 2 - 1.5 / 2
SLOT_HEIGHT = 131.5

# --- Text and cutout offsets ---
TEXT_OFFSET = 2

LABELS = {1: "Čerpadlo", 2: "Nádrž"}


def create_mounting_post(face, x, y, depth=DEPTH, diameter=HOLE_DIAMETER) -> Workplane:
    """Create a mounting post with a hole."""
    return (face.tag("mounting_face")
            .moveTo(x, y)
            .rect(diameter * 2, HOLE_BORDER_OFFSET * 2).extrude(depth)
            .workplaneFromTagged("mounting_face")
            .workplane(offset=depth)
            .moveTo(x, y)
            .circle(diameter / 2)
            .cutBlind(-depth)
            )


def add_partitions(wp):
    """Add vertical and horizontal ventilation slots."""
    # Vertical slot
    wp = wp.faces("<Z").workplane(offset=WALL_THICKNESS, invert=True)
    wp = wp.moveTo(0, (-HEIGHT + SLOT_HEIGHT) / 2 + SLOT_START_OFFSET)
    wp = wp.box(SLOT_WIDTH, SLOT_HEIGHT, DEPTH - 1, centered=[True, True, False])
    # Horizontal slots
    for i in range(9):
        wp = wp.faces("<Z").workplane(offset=WALL_THICKNESS, invert=True)
        y_pos = -HEIGHT / 2 + SLOT_START_OFFSET + i * SLOT_SPACING
        wp = wp.moveTo(0, y_pos).box(WIDTH, SLOT_WIDTH, DEPTH - 1, centered=[True, True, False])
    return wp


def add_side_cutouts(wp):
    """Add cutouts on both sides of the case."""
    for i in range(8):
        y_pos = -HEIGHT / 2 + SLOT_START_OFFSET + i * SLOT_SPACING + SLOT_SPACING / 2
        z_pos = (-BOARD_THICKNESS - BOTTOM_HEIGHT - 2) / 2 + WALL_THICKNESS
        wp = wp.faces(">X").workplane()
        wp = wp.moveTo(y_pos, z_pos)
        wp = wp.rect(12.6, 5 + BOARD_THICKNESS + BOTTOM_HEIGHT + 2, centered=True).cutBlind(-WALL_THICKNESS)
    # Final right side cutout
    wp = wp.faces(">X").workplane()
    wp = wp.moveTo(HEIGHT / 2 - 15.5, (-BOARD_THICKNESS - BOTTOM_HEIGHT - 2) / 2 + WALL_THICKNESS)
    wp = wp.rect(8, 5 + BOARD_THICKNESS + BOTTOM_HEIGHT + 2, centered=True).cutBlind(-WALL_THICKNESS)
    # Left side cutouts (mirror)
    for i in range(8):
        y_pos = -(-HEIGHT / 2 + SLOT_START_OFFSET + i * SLOT_SPACING + SLOT_SPACING / 2)
        z_pos = (-BOARD_THICKNESS - BOTTOM_HEIGHT - 2) / 2 + WALL_THICKNESS
        wp = wp.faces("<X").workplane()
        wp = wp.moveTo(y_pos, z_pos)
        wp = wp.rect(12.6, 5 + BOARD_THICKNESS + BOTTOM_HEIGHT + 2, centered=True).cutBlind(-WALL_THICKNESS)
    return wp


def add_top_cutouts(wp):
    """Add cutouts and extrusions on the top face."""
    # Large rectangle cutout and extrusion
    wp = wp.faces("<Z").workplane(centerOption="CenterOfBoundBox", invert=True).moveTo(9.5, HEIGHT / 2 - 9 / 2)
    wp = wp.rect(19, 10, centered=True).extrude(DEPTH)
    wp = wp.faces("<Z").workplane(centerOption="CenterOfBoundBox", invert=True).moveTo(9.5, HEIGHT / 2 - 9 / 2)
    wp = wp.rect(18, 9, centered=True).cutThruAll()
    wp = wp.faces("<Z").workplane(centerOption="CenterOfBoundBox", invert=True).moveTo(10, HEIGHT / 2 - 9 / 2)
    wp = wp.rect(18, 8, centered=True).extrude(WALL_THICKNESS)
    # Small rectangle cutout and extrusion
    wp = wp.faces("<Z").workplane(centerOption="CenterOfBoundBox", invert=True).moveTo(5, HEIGHT / 2 - 8 / 2)
    wp = wp.rect(6, 4, centered=True).extrude(DEPTH - 1)
    # Left side rectangle cutout and extrusion
    wp = wp.faces("<Z").workplane(centerOption="CenterOfBoundBox", invert=True).moveTo(-7.5, HEIGHT / 2 - 9 / 2)
    wp = wp.rect(7, 5, centered=True).extrude(DEPTH)
    wp = wp.faces("<Z").workplane(centerOption="CenterOfBoundBox", invert=True).moveTo(-7.5, HEIGHT / 2 - 9 / 2)
    wp = wp.rect(6, 4, centered=True).cutBlind(DEPTH)
    return wp


def add_mounting_posts(wp, tag_face, post_depth, diameter=HOLE_DIAMETER):
    """Add three mounting posts to the given face."""
    positions = [
        (HOLE_DISTANCE / 2, HEIGHT / 2 - HOLE_BORDER_OFFSET),
        (-HOLE_DISTANCE / 2, HEIGHT / 2 - HOLE_BORDER_OFFSET),
        (0, -(HEIGHT / 2 - HOLE_BORDER_OFFSET))
    ]
    for x, y in positions:
        wp = create_mounting_post(wp.workplaneFromTagged(tag_face), x, y, depth=post_depth, diameter=diameter)
    return wp


def build_main_case():
    """Build the main case."""
    wp = cq.Workplane("XY")
    wp = wp.box(WIDTH + WALL_THICKNESS * 2, HEIGHT + WALL_THICKNESS * 2,
                DEPTH + BOTTOM_HEIGHT + BOARD_THICKNESS + WALL_THICKNESS, centered=True)
    wp = wp.edges().filter(lambda e: e.Center().z < wp.faces(">Z").val().Center().z).fillet(2)
    wp = wp.faces(">Z").rect(WIDTH, HEIGHT).cutBlind(-DEPTH - BOTTOM_HEIGHT - BOARD_THICKNESS)
    wp = add_partitions(wp)

    wp = wp.faces("<Z").workplane(centerOption="CenterOfBoundBox", invert=True, offset=BOARD_THICKNESS).moveTo(
        -(WIDTH / 2 - 8.6), HEIGHT / 2 - 22.5).circle(5 / 2).extrude(DEPTH - 3.5)
    wp = wp.faces("<Z").workplane(centerOption="CenterOfBoundBox", invert=True, offset=BOARD_THICKNESS).moveTo(
        -(WIDTH / 2 - 8.6), HEIGHT / 2 - 22.5).circle(4.5 / 2).cutBlind(DEPTH - 3.5)

    wp = wp.faces("<Z[-2]").workplane().tag("bottom_face")
    wp = add_mounting_posts(wp, "bottom_face", post_depth=DEPTH, diameter=HOLE_DIAMETER / 1.5)
    wp = add_side_cutouts(wp)
    wp = add_top_cutouts(wp)
    return wp


def build_bottom_plate():
    """Build the bottom plate."""
    wp = cq.Workplane("XY")
    wp = wp.box(WIDTH + WALL_THICKNESS * 2, HEIGHT + WALL_THICKNESS * 2, WALL_THICKNESS, centered=True)
    wp = wp.faces("<Z").workplane(invert=True).tag("bottom_face")
    wp = add_mounting_posts(wp, "bottom_face", post_depth=BOTTOM_HEIGHT + WALL_THICKNESS)
    # Additional mounting posts
    wp = create_mounting_post(wp.faces("<Z").workplane(invert=True), 0,
                              -(HEIGHT / 2 + HOLE_BORDER_OFFSET + WALL_THICKNESS), depth=WALL_THICKNESS)
    wp = create_mounting_post(wp.faces("<Z").workplane(invert=True), 0,
                              (HEIGHT / 2 + HOLE_BORDER_OFFSET + WALL_THICKNESS), depth=WALL_THICKNESS)
    wp = wp.edges("<Z").fillet(.68)
    return wp


def add_text(main_case):
    assy = cq.Assembly()

    for i in range(1, 9):

        z_offset = -DEPTH / 2 - WALL_THICKNESS * 2
        x_offset = 3
        y_offset = - HEIGHT / 2 + (8 - i) * SLOT_SPACING + SLOT_SPACING / 2

        main_case = inject_text(assy, f"{i}", main_case, x_offset, y_offset, z_offset)

        if i in LABELS:
            main_case = inject_text(assy, f"{LABELS[i]}", main_case, - x_offset, y_offset + SLOT_SPACING / 4, z_offset)

    assy.add(main_case, loc=cq.Location((0, 0, 0), (1, 0, 0), 0), name="case", color=cq.Color("green"))

    return assy


def inject_text(assy, t, main_case, x_offset, y_offset, z_offset):
    text_shape = (cq.Workplane("XY").text(t, 8, WALL_THICKNESS + .1, font="Consolas", kind="bold",
                                          halign="right" if x_offset < 0 else "left")
                  .mirror("XZ"))
    main_case = (main_case.faces("<Z").workplane()
                 .cut(text_shape.val().translate((x_offset, y_offset, z_offset))))
    assy.add(text_shape, loc=cq.Location((x_offset, y_offset, z_offset), (1, 0, 0), 0), name=t, color=cq.Color("red"))
    return main_case


def main():
    """Main workflow."""
    main_case = build_main_case()
    render(main_case, 'irrigation.stl')

    render(add_text(main_case), "irrigation.step")

    render(build_bottom_plate(), 'irrigation_bottom.stl')


if __name__ == "__main__":
    main()
