from cadquery import cq, Workplane

from common import build_toothed_cylinder

outer_width = 152
inner_width = 133
outer_depth = 170
bottom_depth = 240
bottom_width = 200
inner_depth = 151
socket_width = 15
socket_height = 7
step_height = 11
socket_offset = 33
outer_radius = 20
bottom = 20
cylinder_radius = outer_depth / 2

inset = 1 / 2

num_teeth = 180
tooth_depth = 2


def build_cylinder_part():
    cylinder = build_toothed_cylinder(cylinder_radius, outer_width, num_teeth, tooth_depth).translate(
        (0, 0, -outer_width / 2))
    cylinder = cylinder.cut(
        Workplane('XY').box(outer_depth, outer_depth, inner_width).translate(
            (-cylinder_radius * inset + outer_depth / 2, - cylinder_radius * inset + outer_depth / 2, 0)))
    cylinder = cylinder.cut(
        Workplane('XY').box(outer_depth, outer_depth, outer_width).translate(
            (-cylinder_radius * inset + outer_depth / 2,
             - cylinder_radius * inset + outer_depth / 2 + step_height, 0)))
    cylinder = cylinder.cut(
        Workplane('XY').box(outer_depth * 2 + tooth_depth * 2, socket_height, socket_width).translate(
            (0, - cylinder_radius * inset + outer_depth / 2 - socket_offset, 0)))

    return cylinder


def build_matching_block(cylinder):
    height = cylinder_radius - cylinder_radius * inset + bottom
    wall = 5
    block = (
        cq.Workplane("XY")
        .rect(bottom_depth, bottom_width)  # Spodní podstava v Z=0
        .workplane(offset=height)  # Přesun do výšky pyramidy
        .rect(outer_depth, outer_width + wall * 2)  # Horní podstava
        .loft(combine=True)
        .translate((0, 0, -height / 2))  # Zarovnání na střed jako byl původní box
    )

    cylinder_to_cut = build_toothed_cylinder(cylinder_radius + .5, outer_width + 1, num_teeth,
                                             tooth_depth + .5).translate(
        (0, 0, -outer_width / 2)).rotate((0, 0, 0), (1, 0, 0), 90).translate(
        (0, 0, cylinder_radius - height / 2 + bottom))

    return block.cut(cylinder_to_cut).cut(
        cq.Workplane("XZ").cylinder(socket_width, (cylinder_radius + bottom)).cut(
            cq.Workplane("XZ").box(cylinder_radius + bottom, cylinder_radius + bottom, socket_width,
                                   centered=(False, False, True)).translate(
                (socket_height, 0, -cylinder_radius - bottom))).translate(
            (0, 0, cylinder_radius - height / 2 + bottom)))


def main():
    cylinder = build_cylinder_part()
    block = build_matching_block(cylinder)

    from common import render
    render(cylinder.add(block.translate((outer_depth, 0, 0))))


if __name__ == "__main__":
    main()
