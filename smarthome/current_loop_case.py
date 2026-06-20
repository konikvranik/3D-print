import os
import sys

from smarthome.reolink_zvonek import build_case

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import render, cq


def build_case():
    """Vytvoří tělo modelu - zvon s kupolí a svislým kulatým okem (vnitřní průměr 5 mm) na špici."""
    base_size = 50
    height = 50
    apex_radius = 3
    wall_size = 1.5
    eye_inner_diameter = 5.0
    bar_diameter = 10.0
    bar_clearance = 1.0

    # tělo: válec s kupolí nahoře, dole otevřený tenkostěnný shell
    body = (
        cq.Workplane("XY")
        .cylinder(height, base_size / 2)
        .faces(">Z").fillet(base_size / 2 - .1)
        .faces("<Z").shell(wall_size)
    )

    # svislé kulaté oko (obruč) na špici: torus, vnitřní průměr eye_inner_diameter
    tube_r = wall_size
    torus_r = eye_inner_diameter / 2 + tube_r  # vnitřní Ø = 2*(torus_r - tube_r) = 5 mm
    eye = cq.Solid.makeTorus(torus_r, tube_r)
    eye = eye.rotate((0, 0, 0), (1, 0, 0), 90)         # rovina oka = svislá (XZ), osa = Y
    z_top = body.val().BoundingBox().zmax              # reálný vrchol kupole
    eye = eye.translate((0, 0, z_top + torus_r))       # oko na špici, mírně zabořené pro čistý spoj

    result = body.union(eye)

    # vodorovný válec (příčka) dole uvnitř zvonu, průměr 1 cm, osa podél X
    bar_radius = bar_diameter / 2
    bar_z = body.val().BoundingBox().zmin + bar_radius + bar_clearance  # ~1 mm nad spodním okrajem
    crossbar = cq.Solid.makeCylinder(
        bar_radius,                                          # průměr 1 cm
        base_size,                                           # délka přes celou šířku (napojí se na stěny)
        cq.Vector(-base_size / 2, 0, bar_z),
        cq.Vector(1, 0, 0),
    )
    result = result.union(crossbar)
    return result


def main():
    """Hlavní workflow."""
    render(build_case())


if __name__ == "__main__":
    main()
