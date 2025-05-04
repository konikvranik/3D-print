import cadquery as cq

from common import render
from storage.nadoba_na_varechy import SMALL_DIAMETER

SMALL_DIAMETER = 10
BIG_DIAMETER = 15
THICK = 1
HEIGHT = 150

wp = cq.Workplane("XY")

wp = (wp.workplane().cylinder(THICK, BIG_DIAMETER / 2, centered=[True, True, False])
      .faces(">Z").workplane()
      .cylinder(HEIGHT, SMALL_DIAMETER / 2, centered=[True, True, False])
      .faces(">Z").workplane()
      .circle(SMALL_DIAMETER / 2 - THICK).cutThruAll())

render(wp, 'proticakaci_tyce.stl')
