# -*- coding: utf-8 -*-


TTGO_WIDTH = 25.09
TTGO_HEIGHT = 51.49
TTGO_HEIGHT_WITH_USB = 53
TTGO_DEPTH_WITH_DISPLAY = 3
TTGO_DEPTH_WITH_RESET = 3
TTGO_DEPTH_WITH_USB = 4.3
USB_WIDTH = 9
USB_HEIGHT = 7.3
USB_DEPTH = 2.8
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
BOARD_DEPTH = 1.25

WALL_THICKNESS = 1

CASE_HEIGHT = TTGO_HEIGHT + 10 + WALL_THICKNESS * 2
CASE_WIDTH = TTGO_WIDTH + 20 + WALL_THICKNESS * 2
CASE_DEPTH = TTGO_DEPTH_WITH_USB + 2 * WALL_THICKNESS

import cadquery as cq

from common import render

wp = cq.Workplane("XY")


def shell():
    global wp
    wp = wp.move(0, -WALL_THICKNESS).box(CASE_WIDTH, CASE_HEIGHT, CASE_DEPTH, centered=[True, False, False])
    wp = (wp.faces(">Z").workplane()
          .rect(CASE_WIDTH - WALL_THICKNESS * 2, CASE_HEIGHT - WALL_THICKNESS * 2, centered=[True, False])
          .cutBlind(-CASE_DEPTH + WALL_THICKNESS))


def display_window():
    global wp
    wp = (wp.faces("<Z[1]").workplane()
          .move(0, TTGO_HEIGHT - DISPLAY_OFFSET - DISPLAY_HEIGHT)
          .rect(DISPLAY_WIDTH, DISPLAY_HEIGHT, centered=[True, False])
          .cutBlind(-WALL_THICKNESS, taper=-70))


def usb_hole():
    global wp
    usb_offset = TTGO_HEIGHT_WITH_USB - TTGO_HEIGHT
    wp = (wp.faces("<Y").workplane(offset=usb_offset)
          .move(0, WALL_THICKNESS + TTGO_DEPTH_WITH_DISPLAY - TTGO_DEPTH_WITH_USB)
          .rect(USB_WIDTH - USB_DEPTH, USB_DEPTH, centered=[True, False])
          .cutBlind(-USB_HEIGHT)

          .faces("<Y").workplane(offset=usb_offset)
          .move((USB_WIDTH - USB_DEPTH) / 2,
                WALL_THICKNESS + TTGO_DEPTH_WITH_DISPLAY - TTGO_DEPTH_WITH_USB + USB_DEPTH / 2)
          .circle(USB_DEPTH / 2)
          .cutBlind(-USB_HEIGHT)

          .faces("<Y").workplane(offset=usb_offset)
          .move(-(USB_WIDTH - USB_DEPTH) / 2,
                WALL_THICKNESS + TTGO_DEPTH_WITH_DISPLAY - TTGO_DEPTH_WITH_USB + USB_DEPTH / 2)
          .circle(USB_DEPTH / 2)
          .cutBlind(-USB_HEIGHT))

    #
    # wp = (wp.faces(">Y").workplane(offset=-WALL_THICKNESS)
    #       .move(0, WALL_THICKNESS + TTGO_DEPTH_WITH_DISPLAY - TTGO_DEPTH_WITH_USB)
    #       .rect(USB_WIDTH - USB_DEPTH, USB_DEPTH, centered=[True, False])
    #       .cutBlind(WALL_THICKNESS, taper=-30)
    #       .workplane()
    #       .move((USB_WIDTH - USB_HEIGHT) / 2, 0)
    #       .circle(USB_DEPTH / 2)
    #       .cutBlind(WALL_THICKNESS, taper=-30)
    #       .workplane()
    #       .move(-(USB_WIDTH - USB_HEIGHT), 0)
    #       .circle(USB_DEPTH / 2)
    #       .cutBlind(WALL_THICKNESS, taper=-30))

    # skew on corner
    # wp = (wp.faces(">Y").workplane(offset=-WALL_THICKNESS)
    #   .move(0, WALL_THICKNESS + TTGO_DEPTH_WITH_DISPLAY - TTGO_DEPTH_WITH_USB)
    #   .rect(USB_WIDTH, USB_DEPTH, centered=[True, False])
    #   .cutBlind(WALL_THICKNESS, taper=-30))


def board_holder():
    global wp
    wp = (wp.faces(">Y[1]").workplane(offset=TTGO_HEIGHT - VOLNY_KONEC)
          # .move(0, TTGO_HEIGHT - VOLNY_KONEC)
          .box(TTGO_WIDTH + WALL_THICKNESS * 2, TTGO_DEPTH_WITH_DISPLAY + WALL_THICKNESS, VOLNY_KONEC,
               centered=[True, False, False]))
    wp = (wp.faces("<Y[2]").workplane()
          .move(0, 0)
          # .box(1,1,1,centered=[True,False,False])
          .rect(TTGO_WIDTH, TTGO_DEPTH_WITH_DISPLAY, centered=[True, False])
          .cutBlind(-VOLNY_KONEC)
          )


## ============================

shell()
display_window()
usb_hole()
board_holder()

render(wp, 'hydroponic_controller_ttgo_case.stl')
