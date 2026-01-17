import cadquery as cq

from common import calculate_pla_bore_diameter
from common import render

width = 48
height = 133
between_holes = 77
screw_hole = 4
drat_branky = 5
napajeci_kabel = 5


def build_case():
    wp = cq.Workplane("XY")
    inner_body = wp.slot2D(height, width).extrude(7)
    inner_body = inner_body.moveTo(10.5, 0).slot2D(44, 20)
    inner_body = inner_body.moveTo(38.5, 0).circle(screw_hole / 2).moveTo(-38.5, 0).circle(screw_hole / 2).cutThruAll()
    inner_body = inner_body.faces('<Y').workplane().moveTo(25 + drat_branky / 2, 0).circle(drat_branky / 2).moveTo(
        -25 - drat_branky / 2, 0).circle(
        drat_branky / 2).cutThruAll()

    hole_offset = napajeci_kabel / 2
    outer_body = wp.slot2D(height, width).extrude(15)
    outer_body = outer_body.faces('<Z').workplane().moveTo(10.5, 0).slot2D(44, 20).cutBlind(
        -hole_offset - napajeci_kabel / 2)
    outer_body = outer_body.faces('>Z[-2]').fillet(napajeci_kabel / 2)
    outer_body = outer_body.faces('<Z').workplane().moveTo(38.5, 0).circle(
        calculate_pla_bore_diameter(screw_hole) / 2).moveTo(-38.5, 0).circle(
        calculate_pla_bore_diameter(screw_hole) / 2).cutBlind(-13)
    outer_body = outer_body.faces('>Z').fillet(12)
    outer_body = outer_body.faces('<Y').workplane().moveTo(25 + drat_branky / 2, 0).circle(drat_branky / 2).moveTo(
        -25 - drat_branky / 2, 0).circle(
        drat_branky / 2).cutThruAll()

    outer_body = outer_body.faces('>Y').workplane().moveTo(-10.5 - 44 / 2 + napajeci_kabel / 2, hole_offset).circle(
        napajeci_kabel / 2).cutBlind(-width / 2)

    return inner_body.union(outer_body.translate((0, width + 10, 0)))


def main():
    """Main workflow."""
    main_case = build_case()
    render(main_case, 'reolink_zvonek.stl')


if __name__ == "__main__":
    main()
