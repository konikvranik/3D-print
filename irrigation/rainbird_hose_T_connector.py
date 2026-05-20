import os
import sys

import cadquery as cq

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import render

#                ←- H -→
#                    ←I→
#                 _____________
#                |##|_______|##|           ↕ A
#                /##|       |##\           ↑
#               /###|       |###\          | B
#              /####|_______|####\         ↓
#            J ← |##|  →    |##|           ↑
#                |##|       |##|           | C
#                |##|_______|##|           ↓
#               /###|_______|###\          ↕ D
#             K ←|##|  →    |##|           ↑
#                |##|       |##|           ↓ E
#               |###|       |###|          ↕ F
#               ||##|_______|##||          ↕ G
#              L ←     →

A = 1.5
B = 7.117
C = 6.65
D = 2
E = 5
F = 1.247
G = 2.453
OUTER_RADIUS_H = 6.5 / 2
INNER_RADIUS_I = 5.502 / 2
BIG_TOOTH_RADIUS_J = 16.854 / 2
SMALL_TOOTH_RADIUS_K = 14.871 / 2
COLLAR_RADIUS_L = 8.25 / 2


def build_body():
    """Vytvoří model stolního držáku na křeslo.
    """

    body = cq.Workplane("XY").moveTo(0, 0).radiusArc((WIDTH, 0), 100).line(0, -50).radiusArc((0, -50), -100).lineTo(0,
                                                                                                                    0).close().extrude(
        20)
    return body


def main():
    """Hlavní workflow."""
    render(build_body(), "limec.stl")


if __name__ == "__main__":
    main()
