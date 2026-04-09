DIAMETER = 9.9
LENGTH = 50
WALL_THICKENSS = 1

import cadquery as cq

from common import render

wp = cq.Workplane("XY")

wp = (wp.cylinder(LENGTH + WALL_THICKENSS, DIAMETER / 2 + WALL_THICKENSS)
      .faces(">Z")
      .workplane()
      .circle(DIAMETER / 2)
      .cutBlind(-LENGTH))
render(wp, 'vicko_na_propisku.stl')
