import os

import cadquery as cq
from cadquery import Workplane

from common import render

os.environ["FONTCONFIG_FILE"] = "/etc/fonts/fonts.conf"
os.environ["FONTCONFIG_PATH"] = "/etc/fonts/"

width = 90
height = 165
board = 1.45
depth = 16.7 - board
bottom = 4 - board
wall = 1.5

hole_dist = 81.5
hole_from_border = 3.7
hole_dia = 2.75

41
131.5

2 - 1.5 / 2

text_offset = 2


def sloupek(face, x, y, depth=depth, diameter=hole_dia) -> Workplane:
    return (face.tag("my_face")
            .moveTo(x, y)
            .rect(hole_dia * 2, hole_from_border * 2).extrude(depth)
            .workplaneFromTagged("my_face")
            .workplane(offset=depth)
            .moveTo(x, y)
            .circle(diameter / 2)
            .cutBlind(-depth)
            )


wp = cq.Workplane("XY")
wp = wp.box(width + wall * 2, height + wall * 2, depth + bottom + board + wall, centered=True)
wp = wp.edges().filter(lambda e: e.Center().z < wp.faces(">Z").val().Center().z).fillet(2)
wp = wp.faces(">Z").rect(width, height).cutBlind(-depth - bottom - board)

wp = wp.faces("<Z").workplane(offset=wall, invert=True)
wp = wp.moveTo(0, (-height + 131.5) / 2 + (2 - 1.5 / 2)).box(.5, 131.5, depth - 1, centered=[True, True, False])
for i in range(0, 9):
    wp = wp.faces("<Z").workplane(offset=wall, invert=True)
    wp = wp.moveTo(0, - height / 2 + (2 - 1.5 / 2) + i * (15 + 1.5)).box(width, .5, depth - 1,
                                                                         centered=[True, True, False])

wp = wp.faces("<Z[-2]").workplane().tag("spodni_dno")
wp = sloupek(wp, hole_dist / 2, (height / 2 - hole_from_border), diameter=hole_dia / 1.5)
wp = sloupek(wp.workplaneFromTagged("spodni_dno"), -hole_dist / 2, (height / 2 - hole_from_border),
             diameter=hole_dia / 1.5)
wp = sloupek(wp.workplaneFromTagged("spodni_dno"), 0, -(height / 2 - hole_from_border), diameter=hole_dia / 1.5)

for i in range(0, 8):
    wp = wp.faces(">X").workplane()
    wp = wp.moveTo(-height / 2 + (2 - 1.5 / 2) + i * (15 + 1.5) + (15 + 1.5) / 2, (-board - bottom - 2) / 2 + wall)
    wp = wp.rect(12.6, 5 + board + bottom + 2, centered=True).cutBlind(-wall)

wp = wp.faces(">X").workplane()
wp = wp.moveTo(height / 2 - 15.5, (-board - bottom - 2) / 2 + wall).rect(8, 5 + board + bottom + 2,
                                                                         centered=True).cutBlind(-wall)

for i in range(0, 8):
    wp = wp.faces("<X").workplane()
    wp = wp.moveTo(-(-height / 2 + (2 - 1.5 / 2) + i * (15 + 1.5) + (15 + 1.5) / 2), (-board - bottom - 2) / 2 + wall)
    wp = wp.rect(12.6, 5 + board + bottom + 2, centered=True).cutBlind(-wall)

wp = wp.faces("<Z").workplane(centerOption="CenterOfBoundBox", invert=True).moveTo(9.5, height / 2 - 9 / 2)
wp = wp.rect(18 + 1, 9 + 1, centered=True).extrude(depth)
wp = wp.faces("<Z").workplane(centerOption="CenterOfBoundBox", invert=True).moveTo(9.5, height / 2 - 9 / 2)
wp = wp.rect(18, 9, centered=True).cutThruAll()
wp = wp.faces("<Z").workplane(centerOption="CenterOfBoundBox", invert=True).moveTo(10, height / 2 - 9 / 2)
wp = wp.rect(18, 8, centered=True).extrude(wall)
wp = wp.faces("<Z").workplane(centerOption="CenterOfBoundBox", invert=True).moveTo(5, height / 2 - 8 / 2)
wp = wp.rect(6, 4, centered=True).extrude(depth - 1)

wp = wp.faces("<Z").workplane(centerOption="CenterOfBoundBox", invert=True).moveTo(-7.5, height / 2 - 9 / 2)
wp = wp.rect(6 + 1, 4 + 1, centered=True).extrude(depth)
wp = wp.faces("<Z").workplane(centerOption="CenterOfBoundBox", invert=True).moveTo(-7.5, height / 2 - 9 / 2)
wp = wp.rect(6, 4, centered=True).cutBlind(depth)

render(wp, 'irrigation.stl')

wp = cq.Workplane("XY")
wp = wp.box(width + wall * 2, height + wall * 2, wall, centered=True)

wp = wp.faces("<Z").workplane(invert=True).tag("spodni_dno")
wp = sloupek(wp, hole_dist / 2, (height / 2 - hole_from_border), depth=bottom + wall)
wp = sloupek(wp.workplaneFromTagged("spodni_dno"), -hole_dist / 2, (height / 2 - hole_from_border), depth=bottom + wall)
wp = sloupek(wp.workplaneFromTagged("spodni_dno"), 0, -(height / 2 - hole_from_border), depth=bottom + wall)

wp = sloupek(wp.faces("<Z").workplane(invert=True), 0, -(height / 2 + hole_from_border + wall), depth=wall)
wp = sloupek(wp.faces("<Z").workplane(invert=True), 0, (height / 2 + hole_from_border + wall), depth=wall)
wp = wp.edges("<Z").fillet(.68)

render(wp, 'irrigation_bottom.stl')
