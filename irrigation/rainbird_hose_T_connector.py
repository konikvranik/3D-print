import os
import sys

from cadquery import Workplane

from rainbird_hose_connector_common import koncovka, J_INNER_RADIUS, M_COLLAR_RADIUS

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import render


def build_body():
    body = (Workplane("XY")
            .cylinder(M_COLLAR_RADIUS * 2, M_COLLAR_RADIUS, centered=True, direct=(1, 0, 0))
            .cylinder(M_COLLAR_RADIUS, M_COLLAR_RADIUS, centered=(True, True, False), direct=(0, 1, 0))
            .faces(">Y").workplane(centerOption="CenterOfBoundBox")
            .circle(J_INNER_RADIUS).cutBlind(-M_COLLAR_RADIUS)
            .faces(">X").workplane(centerOption="CenterOfBoundBox")
            .circle(J_INNER_RADIUS).cutBlind(-2 * M_COLLAR_RADIUS)
            )
    body = koncovka(M_COLLAR_RADIUS).union(body)
    body = koncovka(M_COLLAR_RADIUS).rotate((0, 0, 0), (0, 0, 1), -90).union(body)
    body = koncovka(M_COLLAR_RADIUS).rotate((0, 0, 0), (0, 0, 1), 180).union(body)
    return body


def main():
    """Hlavní workflow."""
    render(build_body())


if __name__ == "__main__":
    main()
