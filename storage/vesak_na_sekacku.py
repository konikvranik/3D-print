import cadquery as cq
from casadi import offset
from ezdxf.zoom import center

from common import render

wp = cq.Workplane("XY")

wp = (wp.box(200, 60, 20, centered=[True, True, False])
      .faces(">Y").workplane().move(0, 8).rect(200, 17).cutBlind(-40))

wp = wp.faces(">Z").workplane().rect(180, 20, forConstruction=True).vertices().circle(2).cutThruAll().workplane().move(0,-20).circle(2).cutThruAll()

cylinder = cq.Workplane("YZ").move(-30, 20).cylinder(200, 20)

wp = wp.union(cylinder)

cylinder = cq.Workplane("YZ").move(-30, 20).cylinder(200, 10)

wp = wp.cut(cylinder)

wp = wp.cut(cq.Workplane("XY").workplane(offset=20).box(200, 80, 20, centered=[True, True, False]))

wp = wp.cut(cq.Workplane("XY").workplane(offset=30).box(200, 1000, 20, centered=[True, True, False]))

wp = wp.faces(">Z").edges().fillet(4)

render(wp, 'vesak_na_sekacku.stl')
