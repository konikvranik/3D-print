import os
import sys

import cadquery as cq
from cadquery import Workplane

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
    body = (Workplane("XY")
            .cylinder(M_COLLAR_RADIUS * 2, M_COLLAR_RADIUS, centered=True)
            .rotate((0, 0, 0), (0, 1, 0), 90)
            .cylinder(M_COLLAR_RADIUS, M_COLLAR_RADIUS, centered=(True, True, False))
            .rotate((0, 0, 0), (1, 0, 0), 90)
            .translate((M_COLLAR_RADIUS, 0, 0)))
    body = koncovka(body).translate((-M_COLLAR_RADIUS, 0, 0))
    body = body.union(koncovka().translate((-M_COLLAR_RADIUS, 0, 0)).rotate((0, 0, 0), (0, 0, 1), 90))
    body = body.union(koncovka().translate((-M_COLLAR_RADIUS, 0, 0)).rotate((0, 0, 0), (0, 0, 1), 180))
    return body


def koncovka(workplane=cq.Workplane("XY")) -> Workplane:
    """
    Vytvoří model koncovky RainBird konektoru.
    """

    return (workplane.moveTo(-(A + B + C + D + E + F), J_INNER_RADIUS)
            .line(0, H_STARTING_OUTER_RADIUS - J_INNER_RADIUS)
            .line(A, 0)
            .line(B, K_BIG_TOOTH_RADIUS - H_STARTING_OUTER_RADIUS)
            .line(0, I_OUTER_RADIUS - K_BIG_TOOTH_RADIUS)
            .line(C, 0)
            .line(D, L_SMALL_TOOTH_RADIUS - I_OUTER_RADIUS)
            .line(0, I_OUTER_RADIUS - L_SMALL_TOOTH_RADIUS)
            .line(E, 0)
            .line(0, M_COLLAR_RADIUS - I_OUTER_RADIUS)
            .line(F, 0)
            .line(0, J_INNER_RADIUS - M_COLLAR_RADIUS)
            .close()
            .revolve(angleDegrees=360, axisStart=(0, 0, 0), axisEnd=(1, 0, 0)))


def main():
    """Hlavní workflow."""
    render(build_body())


if __name__ == "__main__":
    main()
