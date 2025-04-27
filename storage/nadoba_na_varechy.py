import cadquery as cq

from common import render

SMALL_DIAMETER = 50
BIG_DIAMETER = 70
THICK = 3
HEIGHT = 150
TYC = 8.75

wp = cq.Workplane("XY")

wp = (wp.workplane().circle(BIG_DIAMETER / 2 + THICK)
      .workplane(offset=HEIGHT)
      .circle(SMALL_DIAMETER / 2 + THICK).loft())

drzak = (cq.Workplane("XY")
         .move(0, BIG_DIAMETER / 2)
         .box(30, TYC + THICK, TYC / 2 + THICK, centered=[True, False, False])
         .faces("+X")
         .workplane().move(BIG_DIAMETER / 2 + TYC / 2, TYC / 2 + THICK)
         .circle(TYC / 2).cutThruAll())
wp = wp.union(drzak)

wp = wp.cut(cq.Workplane("XY").workplane()
            .circle(BIG_DIAMETER / 2)
            .workplane(offset=HEIGHT - THICK)
            .circle(SMALL_DIAMETER / 2).loft()
            .faces(">Z")
            .edges()
            .fillet(SMALL_DIAMETER / 2 - .001))

wp = wp.faces(">Z").edges().fillet(SMALL_DIAMETER / 2 + THICK - .001)

render(wp, 'nadoba_na_varechy.stl')
