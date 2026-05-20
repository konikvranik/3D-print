import os
import sys

import cadquery as cq

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import render

WIDTH=230


def build_body():
    """Vytvoří model stolního držáku na křeslo.
    """

    body=cq.Workplane("XY").moveTo(0,0).radiusArc((WIDTH, 0), 100).line(0, -50).radiusArc((0, -50),-100) .lineTo(0, 0).close().extrude(20)
    return body


def main():
    """Hlavní workflow."""
    render(build_body(), "limec.stl")


if __name__ == "__main__":
    main()
