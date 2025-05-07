# -*- coding: utf-8 -*-


TTGO_WIDTH = 25.09
TTGO_HEIGHT = 51.49
TTGO_HEIGHT_WITH_USB = 53
TTGO_DEPTH_WITH_DISPLAY = 3
TTGO_DEPTH_WITH_RESET = 3
TTGO_DEPTH_WITH_USB = 4.3
USB_WIDTH = 9
USB_HEIGHT = 7.3
DISPLAY_HEIGHT = 26
DISPLAY_WIDTH = 16.5
DISPLAY_OFFSET = 6.7
BUTTON_WIDTH = 3.3
BUTTON_HEIGHT = 4.1
BUTTON_CENTER_OFFSET_X = 4.5
BUTTON_CENTER_OFFSET_Y = 3.2
RESET_CENTER_OFFSET_Y = 11
RESET_HEIGHT = 4.5
VOLNY_KONEC = 5.4

WALL_THICKNESS = 1

CASE_HEIGHT = TTGO_HEIGHT_WITH_USB + WALL_THICKNESS * 2
CASE_WIDTH = TTGO_WIDTH + WALL_THICKNESS * 2
CASE_DEPTH = 30

import cadquery as cq

from common import render

wp = cq.Workplane("XY")


def shell():
    global wp
    wp = wp.box(CASE_WIDTH, CASE_HEIGHT, CASE_DEPTH, centered=[True, False, False])
    wp = wp.faces(">Z").workplane().move(0, WALL_THICKNESS).rect(CASE_WIDTH - WALL_THICKNESS * 2,
                                                                 CASE_HEIGHT - WALL_THICKNESS * 2,
                                                                 centered=[True, False]).cutBlind(
        -CASE_DEPTH + WALL_THICKNESS)


shell()

wp = (wp.faces("<Z").workplane(offset=-WALL_THICKNESS)
      .move(0, -TTGO_HEIGHT_WITH_USB + DISPLAY_OFFSET)
      .rect(DISPLAY_WIDTH, DISPLAY_HEIGHT, centered=[True, False])
      .cutBlind(WALL_THICKNESS, taper=-80))

render(wp, 'hydroponic_controller_ttgo_case.stl')
