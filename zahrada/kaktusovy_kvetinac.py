DIAMETER = 60
LENGTH = 48
WALL_THICKENSS = 3

import cadquery as cq

from common import render

wp = cq.Workplane("XY")

wp = (wp.cylinder(LENGTH + WALL_THICKENSS, DIAMETER / 2 + WALL_THICKENSS)
      .faces(">Z")
      .workplane()
      .circle(DIAMETER / 2)
      .cutBlind(-LENGTH))
render(wp, 'kaktusovy_kvetinac.stl')
