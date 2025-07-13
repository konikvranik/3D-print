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

text_offset = 2


def sloupek(face, x, y) -> Workplane:
    return (face.tag("my_face")
            .moveTo(x, y)
            .rect(hole_from_border * 2, hole_from_border * 2).extrude(depth)
            .workplaneFromTagged("my_face")
            .moveTo(x, y)
            .circle(hole_dia / 2)
            .cutBlind(depth)
            )


wp = cq.Workplane("XY")
wp = wp.box(width + wall * 2, height + wall * 2, depth + bottom + board + wall, centered=True)
wp = wp.faces(">Z").rect(width, height).cutBlind(-depth - bottom - board)
wp = wp.faces("<Z[-2]").workplane().tag("spodni_dno")
wp = sloupek(wp, hole_dist / 2, (height / 2 - hole_from_border))
wp = sloupek(wp.workplaneFromTagged("spodni_dno"), -hole_dist / 2, (height / 2 - hole_from_border))
wp = sloupek(wp.workplaneFromTagged("spodni_dno"), 0, -(height / 2 - hole_from_border))

render(wp, 'irrigation.stl')
