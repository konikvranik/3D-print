import os
import sys

import cadquery as cq

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import render

WIDTH = 230
THICK = 20
SAGITA = 70


def build_body():
    """Vytvoří model límce z CyberPunku.
    """

    body = (cq.Workplane("XY")
            .moveTo(0, 0)
            .sagittaArc((WIDTH, 0), SAGITA)
            .line(0, -THICK)
            .sagittaArc((0, -THICK), -SAGITA)
            .close()
            .extrude(20))
    return body


def main():
    """Hlavní workflow."""
    render(build_body(), "limec.stl")


if __name__ == "__main__":
    main()
