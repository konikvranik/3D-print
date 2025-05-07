# -*- coding: utf-8 -*-


TTGO_WIDTH = 25.7
TTGO_HEIGHT = 51.6
TTGO_HEIGHT_WITH_USB = 53
TTGO_DEPTH_WITH_DISPLAY = 3
TTGO_DEPTH_WITH_RESET = 3
TTGO_DEPTH_WITH_USB = 4.3
USB_WIDTH = 9.5
USB_HEIGHT = 7.4
USB_DEPTH = 3
DISPLAY_HEIGHT = 26
DISPLAY_WIDTH = 16.5
DISPLAY_OFFSET = 8
BUTTON_WIDTH = 3.3
BUTTON_HEIGHT = 4.1
BUTTON_CENTER_OFFSET_X = 4.5
BUTTON_CENTER_OFFSET_Y = 3.2
RESET_CENTER_OFFSET_Y = 11
RESET_HEIGHT = 4.5
VOLNY_KONEC = 5.4
BOARD_DEPTH = 1.25

WALL_THICKNESS = 1

CASE_HEIGHT = TTGO_HEIGHT + 10 + 50
CASE_WIDTH = max(TTGO_WIDTH + 10, 40)
CASE_DEPTH = 30

# CASE_HEIGHT = TTGO_HEIGHT + 10
# CASE_WIDTH = TTGO_WIDTH + 10
# CASE_DEPTH = TTGO_DEPTH_WITH_USB

import cadquery as cq

from common import render

wp = cq.Workplane("XY")


def shell():
    global wp
    wp = wp.moveTo(0, -WALL_THICKNESS).box(CASE_WIDTH, CASE_HEIGHT, CASE_DEPTH, centered=[True, False, False])
    wp = (wp.faces(">Z").workplane()
          .rect(CASE_WIDTH - WALL_THICKNESS * 2, CASE_HEIGHT - WALL_THICKNESS * 2, centered=[True, False])
          .cutBlind(-CASE_DEPTH + WALL_THICKNESS))


def display_window():
    global wp
    wp = (wp.faces("<Z[1]").workplane()
          .moveTo(0, TTGO_HEIGHT - DISPLAY_OFFSET - DISPLAY_HEIGHT)
          .rect(DISPLAY_WIDTH, DISPLAY_HEIGHT, centered=[True, False])
          .cutBlind(-WALL_THICKNESS, taper=-70))


def usb_hole():
    global wp
    usb_offset = TTGO_HEIGHT_WITH_USB - TTGO_HEIGHT
    wp = (wp.faces("<Y").workplane(offset=usb_offset - WALL_THICKNESS)
          .moveTo(0, WALL_THICKNESS + TTGO_DEPTH_WITH_DISPLAY - TTGO_DEPTH_WITH_USB)
          .rect(USB_WIDTH - USB_DEPTH, USB_DEPTH, centered=[True, False])
          .cutBlind(-USB_HEIGHT)

          .faces("<Y").workplane(offset=usb_offset - WALL_THICKNESS)
          .moveTo((USB_WIDTH - USB_DEPTH) / 2,
                  WALL_THICKNESS + TTGO_DEPTH_WITH_DISPLAY - TTGO_DEPTH_WITH_USB + USB_DEPTH / 2)
          .circle(USB_DEPTH / 2)
          .cutBlind(-USB_HEIGHT)

          .faces("<Y").workplane(offset=usb_offset - WALL_THICKNESS)
          .moveTo(-(USB_WIDTH - USB_DEPTH) / 2,
                  WALL_THICKNESS + TTGO_DEPTH_WITH_DISPLAY - TTGO_DEPTH_WITH_USB + USB_DEPTH / 2)
          .circle(USB_DEPTH / 2)
          .cutBlind(-USB_HEIGHT))

    #
    # skew on corner
    # wp = (wp.faces(">Y").workplane(offset=-WALL_THICKNESS)
    #   .moveTo(0, WALL_THICKNESS + TTGO_DEPTH_WITH_DISPLAY - TTGO_DEPTH_WITH_USB)
    #   .rect(USB_WIDTH, USB_DEPTH, centered=[True, False])
    #   .cutBlind(WALL_THICKNESS, taper=-30))


def board_holder():
    global wp
    wp = (wp.faces(">Y[1]").workplane(offset=TTGO_HEIGHT - VOLNY_KONEC)
          # .moveTo(0, TTGO_HEIGHT - VOLNY_KONEC)
          .box(TTGO_WIDTH + WALL_THICKNESS * 2, TTGO_DEPTH_WITH_DISPLAY + WALL_THICKNESS, VOLNY_KONEC,
               centered=[True, False, False]))
    wp = (wp.faces("<Y[2]").workplane()
          .moveTo(0, 0)
          # .box(1,1,1,centered=[True,False,False])
          .rect(TTGO_WIDTH, TTGO_DEPTH_WITH_DISPLAY, centered=[True, False])
          .cutBlind(-VOLNY_KONEC)
          )


def buttons():
    global wp
    button_width = 5
    button_height = 5
    space = .2
    extension = 5

    wp = (wp
          .faces("<Z")
          .workplane(origin=cq.Vector(0, 0, 0), centerOption="ProjectedOrigin", invert=True)
          .moveTo(-TTGO_WIDTH / 2 + BUTTON_CENTER_OFFSET_X, BUTTON_CENTER_OFFSET_Y)
          .rect(button_width + space, button_height + space)
          .cutThruAll()

          .faces("<Z")
          .workplane(invert=True)
          .moveTo(-TTGO_WIDTH / 2 + BUTTON_CENTER_OFFSET_X, BUTTON_CENTER_OFFSET_Y + button_height / 2)
          .rect(3, extension, centered=[True, False])
          .cutThruAll()

          .faces("<Z")
          .workplane(invert=True)
          .moveTo(-TTGO_WIDTH / 2 + BUTTON_CENTER_OFFSET_X, BUTTON_CENTER_OFFSET_Y)
          .rect(button_width, button_height)
          .extrude(WALL_THICKNESS)

          .faces("<Z")
          .workplane(invert=True)
          .moveTo(-TTGO_WIDTH / 2 + BUTTON_CENTER_OFFSET_X, BUTTON_CENTER_OFFSET_Y + button_height / 2)
          .rect(3 - space, extension, centered=[True, False])
          .extrude(WALL_THICKNESS)

          )

    wp = (wp.faces("<Z")
          .workplane(invert=True)
          .moveTo(TTGO_WIDTH / 2 - BUTTON_CENTER_OFFSET_X, BUTTON_CENTER_OFFSET_Y)
          .rect(button_width + space, button_height + space).cutThruAll()

          .faces("<Z")
          .workplane(invert=True)
          .moveTo(TTGO_WIDTH / 2 - BUTTON_CENTER_OFFSET_X, BUTTON_CENTER_OFFSET_Y + button_height / 2)
          .rect(3, extension, centered=[True, False])
          .cutThruAll()

          .faces("<Z")
          .workplane(invert=True)
          .moveTo(TTGO_WIDTH / 2 - BUTTON_CENTER_OFFSET_X, BUTTON_CENTER_OFFSET_Y)
          .rect(button_width, button_height)
          .extrude(WALL_THICKNESS)

          .faces("<Z")
          .workplane(invert=True)
          .moveTo(TTGO_WIDTH / 2 - BUTTON_CENTER_OFFSET_X, BUTTON_CENTER_OFFSET_Y + button_height / 2)
          .rect(3 - space, extension, centered=[True, False])
          .extrude(WALL_THICKNESS)

          )


def division():
    global wp
    wp = (wp
          .faces("<Z[-2]")
          .workplane()
          .moveTo(0, TTGO_HEIGHT + 5)
          .box(CASE_WIDTH, WALL_THICKNESS, max(CASE_DEPTH - 5, TTGO_DEPTH_WITH_DISPLAY), centered=[True, False, False])
          )


## ============================

shell()
display_window()
usb_hole()
board_holder()
buttons()
division()

render(wp, 'hydroponic_controller_ttgo_case.stl')
