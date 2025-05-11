# -*- coding: utf-8 -*-

WALL_THICKNESS = 1

TTGO_WIDTH = 25.7
TTGO_HEIGHT = 51.6
TTGO_HEIGHT_WITH_USB = 53
TTGO_DEPTH_WITH_DISPLAY = 3
TTGO_DEPTH_WITH_RESET = 3
TTGO_DEPTH_WITH_USB = 4.3
TTGO_SPACE_ABOVE = 10
TTGO_SPACE_BEHIND = 10
BOARD_DEPTH = 1.25

VOLNY_KONEC = 5.4

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

IRF_WIDTH = 33.7
IRF_HEIGHT = 26
IRF_DEPTH = 23.5
IRF_SPACE_BEHIND = 8
IRF_PIN_LENGTH = 6.3
IRF_HOLE_OFFSET = 7

TDS_WIDTH = 31.55
TDS_HEIGHT = 42.6
TDS_CONNECTOR_LENGTH = 4.45
TDS_CONNECTOR_WIDTH = 20
TDS_CONNECTOR_DEPTH = 7.5
TDS_CONNECTOR_HEIGHT = 7.35
TDS_BOARD = 3.2
TDS_SPACE_BEHIND = 10

TDS_PIN_LENGTH = 4.35
TDS_DEPTH = 9.5
TDS_PIN_WIDTH = 10
TDS_PIN_DEPTH = 6
TDS_WIRE_WIDTH = 15
TDS_WIRE_HEIGHT = 5

PH_WIDTH = 42
PH_HEIGHT = 32
PH_DEPTH = 20

MOTOR_WIRE_DIAMETER = 3.7
DS_WIRE_MAX_DIAMETER = 6.45
DS_DIAMETER = 5.9
DS_WIRE_DIAMETER = 4.1
TDS_WIRE_DIAMETER = 3.4

CASE_HEIGHT = max(TTGO_HEIGHT + TTGO_SPACE_BEHIND + WALL_THICKNESS,
                  TDS_HEIGHT + TDS_CONNECTOR_LENGTH + TDS_PIN_LENGTH + 2 * TDS_SPACE_BEHIND) + 2 * (
                      IRF_HEIGHT + IRF_PIN_LENGTH + IRF_SPACE_BEHIND + WALL_THICKNESS) + WALL_THICKNESS
CASE_WIDTH = max(TTGO_WIDTH + 3 * WALL_THICKNESS + 10, IRF_WIDTH + 2 * WALL_THICKNESS, TDS_WIDTH + 4 * WALL_THICKNESS)
CASE_DEPTH = 2 * WALL_THICKNESS + max(
    TTGO_DEPTH_WITH_DISPLAY + TTGO_SPACE_ABOVE + TDS_DEPTH + TDS_BOARD + WALL_THICKNESS, IRF_DEPTH)

SPACE_BUFFER = .2

# CASE_HEIGHT = TTGO_HEIGHT + 10
# CASE_WIDTH = TTGO_WIDTH + 10
# CASE_DEPTH = TTGO_DEPTH_WITH_USB

import cadquery as cq

from common import render

wp = cq.Workplane("XY")


def shell():
    global wp
    wp = (wp.moveTo(0, -WALL_THICKNESS)
          .box(CASE_WIDTH, CASE_HEIGHT, CASE_DEPTH, centered=[True, False, False]))
    wp = (wp.faces(">Z").workplane()
          .rect(CASE_WIDTH - WALL_THICKNESS * 2, CASE_HEIGHT - WALL_THICKNESS * 2, centered=[True, False])
          .cutBlind(-CASE_DEPTH + WALL_THICKNESS))


def wire_holes():
    global wp
    wp = (wp.faces(">X").workplane(centerOption="CenterOfMass")
          .move(CASE_HEIGHT / 8, 0)
          .circle(max(DS_WIRE_MAX_DIAMETER, DS_WIRE_DIAMETER + MOTOR_WIRE_DIAMETER / 2)).cutBlind(-WALL_THICKNESS))

    wp = (wp.faces("<Y").workplane(invert=False, centerOption="ProjectedOrigin", origin=cq.Vector(0, 0, 0))
          .move(CASE_WIDTH / 4, 0)
          .moveTo(0, TTGO_DEPTH_WITH_DISPLAY + TTGO_SPACE_ABOVE - MOTOR_WIRE_DIAMETER / 2)
          .circle(MOTOR_WIRE_DIAMETER / 2).cutBlind(-WALL_THICKNESS)
          )


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
          .moveTo(0, max(TTGO_HEIGHT + TTGO_SPACE_BEHIND,
                         TDS_HEIGHT + TDS_CONNECTOR_LENGTH + TDS_PIN_LENGTH + 2 * TDS_SPACE_BEHIND))
          .box(CASE_WIDTH, WALL_THICKNESS, TTGO_DEPTH_WITH_DISPLAY + TTGO_SPACE_ABOVE + 3 * WALL_THICKNESS,
               centered=[True, False, False])
          .faces(">Y[-3]")
          .workplane(centerOption="CenterOfMass", invert=True)
          .move(-IRF_HOLE_OFFSET, 0)
          .rect(10, 15)
          .cutBlind(WALL_THICKNESS)
          )

    wp = (wp
          .faces("<Z[-2]")
          .workplane()
          .moveTo(0, WALL_THICKNESS + IRF_HEIGHT + IRF_PIN_LENGTH + IRF_SPACE_BEHIND)
          .box(CASE_WIDTH, WALL_THICKNESS, TTGO_DEPTH_WITH_DISPLAY + TTGO_SPACE_ABOVE + 3 * WALL_THICKNESS,
               centered=[True, False, False])
          .faces(">Y[-3]")
          .workplane(centerOption="CenterOfMass", invert=True)
          .move(-IRF_HOLE_OFFSET, 0)
          .rect(10, 15)
          .cutBlind(WALL_THICKNESS)
          )


def distancni_sloupky():
    global wp
    wp = (wp.faces("<Z[-3]").workplane(centerOption="ProjectedOrigin", origin=cq.Vector(0, 0, 0))
          .move(-CASE_WIDTH / 2 + WALL_THICKNESS * 1.5, 0)
          .box(WALL_THICKNESS * 3, 5, TTGO_DEPTH_WITH_DISPLAY + TTGO_SPACE_ABOVE, centered=[True, False, False]))
    wp = (wp.faces("<Z[-3]").workplane(centerOption="ProjectedOrigin", origin=cq.Vector(0, 0, 0))
          .move(CASE_WIDTH / 2 - WALL_THICKNESS * 1.5, 0)
          .box(WALL_THICKNESS * 3, 5, TTGO_DEPTH_WITH_DISPLAY + + TTGO_SPACE_ABOVE, centered=[True, False, False]))
    wp = (wp.faces("<Z[-3]").workplane(centerOption="ProjectedOrigin", origin=cq.Vector(0, 0, 0))
          .move(-CASE_WIDTH / 2 + WALL_THICKNESS * 1.5, TTGO_HEIGHT + TTGO_SPACE_BEHIND - 5)
          .box(WALL_THICKNESS * 3, 5, TTGO_DEPTH_WITH_DISPLAY + + TTGO_SPACE_ABOVE, centered=[True, False, False]))
    wp = (wp.faces("<Z[-3]").workplane(centerOption="ProjectedOrigin", origin=cq.Vector(0, 0, 0))
          .move(CASE_WIDTH / 2 - WALL_THICKNESS * 1.5, TTGO_HEIGHT + TTGO_SPACE_BEHIND - 5)
          .box(WALL_THICKNESS * 3, 5, TTGO_DEPTH_WITH_DISPLAY + + TTGO_SPACE_ABOVE, centered=[True, False, False]))


def tds_case():
    global wp
    wp = (wp.workplane(offset=-WALL_THICKNESS, centerOption="ProjectedOrigin", origin=cq.Vector(0, 0, 0))
          .box(CASE_WIDTH - 2 * WALL_THICKNESS, max(TTGO_HEIGHT + TTGO_SPACE_BEHIND,
                                                    TDS_HEIGHT + TDS_CONNECTOR_LENGTH + TDS_PIN_LENGTH + 2 * TDS_SPACE_BEHIND) - 2 * SPACE_BUFFER,
               WALL_THICKNESS,
               centered=[True, True, False])

          .faces(">Z").workplane()
          .moveTo(0, (max(TTGO_HEIGHT + TTGO_SPACE_BEHIND,
                          TDS_HEIGHT + TDS_CONNECTOR_LENGTH + TDS_PIN_LENGTH + 2 * TDS_SPACE_BEHIND) - 2 * SPACE_BUFFER) / 2)
          .rect(TDS_WIRE_WIDTH, TDS_WIRE_HEIGHT * 2)
          .cutBlind(-WALL_THICKNESS)

          .faces(">Z").workplane()
          .box(TDS_WIDTH + WALL_THICKNESS * 2, TDS_HEIGHT + WALL_THICKNESS * 2, TDS_DEPTH + WALL_THICKNESS + TDS_BOARD,
               centered=[True, True, False])
          .faces(">Z").workplane()
          .rect(TDS_WIDTH, TDS_HEIGHT).cutBlind(-TDS_DEPTH - WALL_THICKNESS - TDS_BOARD)

          .faces("<Y[-2]").workplane(centerOption="ProjectedOrigin", origin=cq.Vector(0, 0, 0))
          .move(0, TDS_BOARD)

          .rect(TDS_CONNECTOR_WIDTH, TDS_CONNECTOR_DEPTH, centered=[True, False]).cutBlind(-WALL_THICKNESS)
          .faces(">Y[-3]").workplane(centerOption="ProjectedOrigin", origin=cq.Vector(0, 0, 0))
          .move(0, TDS_BOARD)
          .rect(TDS_PIN_WIDTH, TDS_PIN_DEPTH + 20, centered=[True, False]).cutBlind(-WALL_THICKNESS)
          )


## ============================

shell()
display_window()
usb_hole()
board_holder()
buttons()
division()
distancni_sloupky()
wire_holes()

render(wp, 'hydroponic_controller_ttgo_case.stl')

wp = cq.Workplane("XY")
tds_case()
render(wp, 'hydroponic_controller_ttgo_case_tds.stl')
