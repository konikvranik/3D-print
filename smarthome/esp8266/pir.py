import os
import sys

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


def build_body():
    """Vytvoří tělo modelu."""
    box = cq.Workplane("XY", origin=(0, 0, 0))
    box = box.box(SAW + SBW + SCW + 2 * W, BH + HT + 2 * W,  BRW + W, centered=(False))
    box = box.faces(">Z").workplane(centerOption="ProjectedOrigin").moveTo(W+SCW,W+LD).circle(LD / 2).cutBlind(BRW)
    return box


def main():
    """Hlavní workflow."""
    render(build_body())


if __name__ == "__main__":
    main()
