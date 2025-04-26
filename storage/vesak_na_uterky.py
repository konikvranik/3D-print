import cadquery as cq

from common import render

wp = cq.Workplane("XY")

wp = wp.box(50, 7, 16 + 6)
wp = wp.faces(">Y").workplane().move(-25, 0).circle(16 / 2 + 3).extrude(-7)

wp = wp.faces(">Y").workplane().move(-25, 0).circle(16 / 2).cutThruAll()

wp = wp.fillet(1.49)

hole = cq.Workplane("XY")
for i in range(10, -25, -6):
    hole = hole.workplane().move(i, 1).box(3, 1, 16 + 6)
    hole = hole.workplane().move(i - 3, -1).box(4, 1, 16 + 6)
    hole = hole.workplane().move(i - 1.5, 0).box(1, 3, 16 + 6)
    hole = hole.workplane().move(i + 1.5, 0).box(1, 3, 16 + 6)

wp = wp.cut(hole)

wp = wp.fillet(.49)

render(wp, 'vesak_na_uterky.stl')
