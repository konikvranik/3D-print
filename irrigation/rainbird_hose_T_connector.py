import os
import sys

import cadquery as cq

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import render

#                 ← H -→
#                ←- I -→
#                    ←J→
#                  ___________
#                 |#|_______|#|            ↕ A
#                /##|       |##\           ↑
#               /###|       |###\          | B
#              /####|_______|####\         ↓
#            K ← |##|  →    |##|           ↑
#                |##|       |##|           | C
#                |##|_______|##|           ↓
#               /###|_______|###\          ↕ D
#             L ←|##|  →    |##|           ↑
#                |##|       |##|           ↓ E
#               |###|       |###|          ↕ F
#               ||##|_______|##||          ↕ G
#             M ←      →

A = 1.5
B = 7.117
C = 6.65
D = 2
E = 5
F = 1.247
G = 2.453
H_STARTING_OUTER_RADIUS = 6.5
I_OUTER_RADIUS = 7
J_INNER_RADIUS = 5.5
K_BIG_TOOTH_RADIUS = 8.5
L_SMALL_TOOTH_RADIUS = 7.5
M_COLLAR_RADIUS = 8.25


def build_body():
    """Vytvoří model stolního držáku na křeslo.
    """

    body = (cq.Workplane("XY").moveTo(0,J_INNER_RADIUS)
            .line(0,H_STARTING_OUTER_RADIUS-J_INNER_RADIUS)
            .line(A,0)
            .line(B,K_BIG_TOOTH_RADIUS-H_STARTING_OUTER_RADIUS)
            .line(0,I_OUTER_RADIUS-K_BIG_TOOTH_RADIUS)
            .line(C,0)
            .line(D,L_SMALL_TOOTH_RADIUS-I_OUTER_RADIUS)
            .line(0,I_OUTER_RADIUS-L_SMALL_TOOTH_RADIUS)
            .line(E,0)
            .line(0,M_COLLAR_RADIUS-I_OUTER_RADIUS)
            .line(F,0)
            .line(0,J_INNER_RADIUS-M_COLLAR_RADIUS)
            .close()
            .revolve(angleDegrees=360, axisStart=(0, 0, 0), axisEnd=(1, 0, 0)))
    return body


def main():
    """Hlavní workflow."""
    render(build_body(), "limec.stl")


if __name__ == "__main__":
    main()
