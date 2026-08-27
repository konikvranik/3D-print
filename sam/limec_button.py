import os
import sys

HANDLE_WIDTH = 10

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import render, cq

BUTTON_WIDTH_WITH_PINS = 15
BUTTON_WIDTH = 12
BUTTON_BODY_HEIGHT = 4
BUTTON_BODY_AND_BUTTON_HEIGHT = 7.5
BUTTON_BODY_AND_PINS_HEIGHT = 7.5
BUTTON_BODY_AND_CABLE_HEIGHT = 4.5
PIN_OUTER_DIST = 6
PIN_INNER_DIST = 3
THICK = 1
BUTTON_PEAK_WIDTH = BUTTON_WIDTH - 4 * THICK


def build_button_body():
    """Vytvoří model límce z CyberPunku s konstantní tloušťkou.
    """
    body = (cq.Workplane("XY")
            .box(BUTTON_WIDTH + 2 * THICK, BUTTON_WIDTH_WITH_PINS + 2 * THICK,
                 BUTTON_BODY_AND_BUTTON_HEIGHT + BUTTON_BODY_AND_PINS_HEIGHT - BUTTON_BODY_HEIGHT + 2 * THICK)
            .faces("<Y").workplane()
            .polyline([(-BUTTON_WIDTH / 2, BUTTON_BODY_HEIGHT / 2),
                       (-BUTTON_PEAK_WIDTH / 2 - THICK, BUTTON_BODY_HEIGHT / 2),

                       (-BUTTON_PEAK_WIDTH / 2 - THICK, BUTTON_BODY_AND_BUTTON_HEIGHT - BUTTON_BODY_HEIGHT / 2 + THICK),
                       (-BUTTON_PEAK_WIDTH / 2, BUTTON_BODY_AND_BUTTON_HEIGHT - BUTTON_BODY_HEIGHT / 2 + THICK),
                       (-BUTTON_PEAK_WIDTH / 2, BUTTON_BODY_AND_BUTTON_HEIGHT - BUTTON_BODY_HEIGHT / 2),
                       (BUTTON_PEAK_WIDTH / 2, BUTTON_BODY_AND_BUTTON_HEIGHT - BUTTON_BODY_HEIGHT / 2),
                       (BUTTON_PEAK_WIDTH / 2, BUTTON_BODY_AND_BUTTON_HEIGHT - BUTTON_BODY_HEIGHT / 2 + THICK),
                       (BUTTON_PEAK_WIDTH / 2 + THICK, BUTTON_BODY_AND_BUTTON_HEIGHT - BUTTON_BODY_HEIGHT / 2 + THICK),

                       (BUTTON_PEAK_WIDTH / 2 + THICK, BUTTON_BODY_HEIGHT / 2),
                       (BUTTON_WIDTH / 2, BUTTON_BODY_HEIGHT / 2),
                       (BUTTON_WIDTH / 2, -BUTTON_BODY_HEIGHT / 2),
                       (PIN_OUTER_DIST / 2, -BUTTON_BODY_HEIGHT / 2),
                       (PIN_OUTER_DIST / 2, -BUTTON_BODY_AND_PINS_HEIGHT / 2 - BUTTON_BODY_HEIGHT / 2),
                       (PIN_INNER_DIST / 2, -BUTTON_BODY_AND_PINS_HEIGHT / 2 - BUTTON_BODY_HEIGHT / 2),
                       (PIN_INNER_DIST / 2, -BUTTON_BODY_AND_CABLE_HEIGHT / 2 - BUTTON_BODY_HEIGHT / 2),
                       (-PIN_INNER_DIST / 2, -BUTTON_BODY_AND_CABLE_HEIGHT / 2 - BUTTON_BODY_HEIGHT / 2),
                       (-PIN_INNER_DIST / 2, -BUTTON_BODY_AND_PINS_HEIGHT / 2 - BUTTON_BODY_HEIGHT / 2),
                       (-PIN_OUTER_DIST / 2, -BUTTON_BODY_AND_PINS_HEIGHT / 2 - BUTTON_BODY_HEIGHT / 2),
                       (-PIN_OUTER_DIST / 2, -BUTTON_BODY_HEIGHT / 2),
                       (-BUTTON_WIDTH / 2, -BUTTON_BODY_HEIGHT / 2)]).close()
            .cutBlind(-BUTTON_WIDTH_WITH_PINS - THICK)
            .faces(">Z")
            .workplane()
            .move(0, BUTTON_WIDTH_WITH_PINS / 2 + THICK)
            .rect(BUTTON_PEAK_WIDTH, BUTTON_WIDTH_WITH_PINS / 2)
            .extrude(THICK)
            .faces("<Z")
            .box(BUTTON_WIDTH + 2 * HANDLE_WIDTH, BUTTON_WIDTH_WITH_PINS + 2 * THICK, THICK)
            .faces("<Z")
            .workplane()

            .moveTo(-BUTTON_WIDTH / 2 - HANDLE_WIDTH / 2 + THICK / 2, -BUTTON_WIDTH_WITH_PINS / 2 - THICK)
            .rect(HANDLE_WIDTH - 2 * THICK - THICK, BUTTON_WIDTH_WITH_PINS - 2 * THICK)
            .cutThruAll()

            .moveTo(BUTTON_WIDTH / 2 + HANDLE_WIDTH / 2 - THICK / 2, -BUTTON_WIDTH_WITH_PINS / 2 - THICK)
            .rect(HANDLE_WIDTH - 2 * THICK - THICK, BUTTON_WIDTH_WITH_PINS - 2 * THICK)
            .cutThruAll()
            )

    return body


def main():
    """Hlavní workflow."""
    render(build_button_body(), "limec_button.stl")


if __name__ == "__main__":
    main()
