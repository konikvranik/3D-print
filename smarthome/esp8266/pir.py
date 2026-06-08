import os
import sys
from typing import Any

from cadquery import Workplane
from cadquery.selectors import StringSyntaxSelector

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import render, cq

# Dimensions from annotated drawing
HT = 24  # total height of the left side
SAW = 21.77  # width of first section
SBW = 7  # width of second section
SCW = 32.8  # width of third section
CW = 5  # width of the top connector protrusion
BH = 25  # height of the main body
EW = 2  # width of left/right edge walls
LD = 25  # diameter of the PIR lens circle
BLH = 15  # height of the bottom-left section
BMH = 16.8  # height of the bottom-middle section
BRW = 28  # width of the bottom-right section
BAH = 4.5  # height of the bottom base strip
CD = 4  # connector depth
W = 3  # wall width
"""
  ______________
  |
  |
  |
  HT
  |                     
  |    |--------- SAW --------|-------- SBW -------|------------------ SCW -------------------|
  |      |CW |
  |       ___
  |      |   |
  ____ __+   +_________________                    ____________________________________________ 
  |    | |   |            |   |                    |     |         .----------.         |     |
  |    | |___|            |   |                    |     |       .-'          '-.       |     |
  |    |     |            |   |                    |     |     .'                '.     |     |
  |    |     |            |---+-----  --           |     |    /                    \    |     |
 BH    |     |            |        |  CW           |     |   |                      |   |     |
  |    |     |            |---+-----  --           |     |    \                    /    |     |
  |    |     |            |   |                    |     |     '.                .'     |     |
  |    |     |            |   |                    |     |       '-.          .-'       |     |
  |    |     |____________|   |                    |     |         '----------'         |     |
  ___  |______________________|                    |_____|______________________________|_____|
                                                                                       
       |EW|                |EW|                          |-------------- LD ------------|
  
  
  
  
  
                                                                            
  
                                   ______                _________________________________
                                   |                 __  |                     |         |  __
  _________  ______________        |                _____|                     |         |_____
  |          |            |        |               |                           |               |
  BLH        |            |       BMH              |                          BRW              |
  |          |            |        |               |                           |               |
  |          |            |        |               |                   |   |   |               |
  ---  ------+------------+----  ---                                   |   |   |
  BAH_ |______________________|                                        |   |   |
                                                                       |___| __|
  
                                                                       |CW |
  
  
"""


def cut_esp(box):
    box = (box.faces(">Z").workplane(centerOption="ProjectedOrigin")
           .moveTo(W + SCW + SBW, W)
           .rect(SAW, BH, centered=False)
           .cutBlind(-BRW + BMH))
    box = (box.faces(">Z").workplane(centerOption="ProjectedOrigin")
           .moveTo(W + SCW + SBW + EW, W)
           .rect(SAW - 2 * EW, BH, centered=False)
           .cutBlind(-BRW + BMH - BLH))
    box = (box.faces(">Z").workplane(centerOption="ProjectedOrigin")
           .moveTo(W + SCW + SBW + EW, W)
           .rect(SAW - 2 * EW, BH + HT, centered=False)
           .cutBlind(-BRW + BMH - CD))
    box = (box.faces(">Z").workplane(centerOption="ProjectedOrigin")
           .moveTo(W + SCW, W + BH / 2 - CW)
           .rect(SBW + EW, CW * 2, centered=False)
           .cutBlind(-BRW + BMH - CD))

    return box


def build_body():
    """Vytvoří tělo modelu."""
    box = cq.Workplane("XY", origin=(0, 0, 0))
    box = (box.box(SAW + SBW + SCW + 2 * W, BH + HT + 2 * W, BRW + W, centered=(False, False, False))
           .edges(StringSyntaxSelector("<Z") + StringSyntaxSelector("|Z"))
           .fillet(W))
    box = cut_pir(box)
    box = cut_esp(box)
    box = cut_upper_cave(box)
    return box


def cut_upper_cave(box) -> Any:
    box = (box.faces(">Z").workplane(centerOption="ProjectedOrigin")
           .moveTo(W, W + BH + W)
           .rect(SAW + SBW + SCW, HT - W, centered=False)
           .cutBlind(-BRW))
    return box


def cut_pir(box: Workplane) -> Workplane:
    box = (box.faces(">Z").workplane(centerOption="ProjectedOrigin")
           .moveTo(W + SCW / 2, W + LD / 2)
           .circle(LD / 2)
           .cutBlind(-BRW - W))
    box = (box.faces(">Z").workplane(centerOption="ProjectedOrigin")
           .moveTo(W, W)
           .rect(SCW, BH, centered=False)
           .cutBlind(-BRW)
           )
    box = (box.faces(">Z").workplane(centerOption="ProjectedOrigin")
           .moveTo(W, W)
           .rect(SCW, BH + W, centered=False)
           .cutBlind(-BRW + BMH - CD)
           )
    return box


def main():
    """Hlavní workflow."""
    render(build_body())


if __name__ == "__main__":
    main()
