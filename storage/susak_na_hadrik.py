import cadquery as cq
import numpy as np


wp = cq.Workplane("XY")

object = wp.box(80, 80, 3).edges("|Z").fillet(3).edges(">Z").fillet(2).faces(">Z").moveTo(40, 0).circle(3 / 2).cutThruAll().moveTo(40, 0).circle(5 / 2).cutBlind(10).faces("<Z").moveTo(40,-20).rect(80, 10).cutBlind(-10)