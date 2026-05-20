import os
import sys

import cadquery as cq

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import render

THICK = 20
WIDTH = 230 -  THICK
SAGITA = 70
HEIGHT = 70


def build_body():
    """Vytvoří model límce z CyberPunku s konstantní tloušťkou.
    """

    body = (cq.Workplane("XY")
            .moveTo(0, 0)
            .sagittaArc((WIDTH, 0), SAGITA)
            .offset2D(THICK/2, kind='intersection')
            .extrude(HEIGHT))
    return body


def main():
    """Hlavní workflow."""
    render(build_body(), "limec.stl")


if __name__ == "__main__":
    main()
