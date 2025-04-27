import cadquery as cq

from common import render

wp = cq.Workplane("XY")

wp = wp.box(50, 7, 16 + 6)
wp = wp.faces(">Y").workplane().move(-25, 0).circle(16 / 2 + 3).extrude(-7)

wp = wp.faces(">Y").workplane().move(-25, 0).circle(16 / 2).cutThruAll()

wp = wp.fillet(1.49)


def zigzag():
    global wp
    for i in range(10, -25, -4):
        wp = wp.cut(cq.Workplane("XY").transformed([0, 0, 45], [i, 0, 0]).box(3, 1, 16 + 6))
        wp = wp.cut(cq.Workplane("XY").transformed([0, 0, -45], [i - 2, 0, 0]).box(3, 1, 16 + 6))


def squared():
    global wp
    hole = cq.Workplane("XY")
    for i in range(10, -25, -6):
        hole = hole.workplane().move(i, 1).box(3, 1, 16 + 6)
        hole = hole.workplane().move(i - 3, -1).box(4, 1, 16 + 6)
        hole = hole.workplane().move(i - 1.5, 0).box(1, 3, 16 + 6)
        hole = hole.workplane().move(i + 1.5, 0).box(1, 3, 16 + 6)

    wp = wp.cut(hole)


zigzag()

wp = wp.cut(cq.Workplane("XY").transformed([0, 0, 45], [-28, 0, 0]).box(7, 7, 16 + 6))

render(wp, 'vesak_na_uterky.stl')
