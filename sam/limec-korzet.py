import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import math

from common import render, cq
from cadquery import Workplane, selectors

PANEL_TOP_WIDTH = 200  # šířka na ramenou (horní hrana)
PANEL_BOTTOM_WIDTH = 140  # šířka na hrudníku (spodní hrana)
PANEL_HEIGHT = 100  # celková výška od ramen po spodek přes hrudník
PANEL_THICKNESS = 4  # tloušťka desky

NECK_DIAMETER = 120  # průměr díry pro krk
NECK_CENTER_Y = -20  # střed díry pro krk pod horní hranou -> otvor se otevírá nahoře jako nákrčník

CORNER_FILLET = 20  # zaoblení vnějších rohů panelu
NECK_EDGE_FILLET = 5  # zaoblení hran, kde nákrčník protíná horní hranu

# Sloty pro suché zipy kolem nákrčníku; zip prochází korzetem a objímá spodní
# přítlačnou plochu límce (limec.py), která má 6 protilehlých děr.
SLOT_COUNT = 6  # počet slotů (odpovídá HOLE_COUNT v limec.py)
SLOT_RADIUS = 70  # vzdálenost středů slotů od středu díry pro krk
SLOT_WIDTH = 3  # šířka slotu, únosný suchý zip s vůlí
SLOT_LENGTH = 10  # délka slotu v radiálním směru, umožňuje doladit polohu zipu
SLOT_ANGLE_START = 190  # úhel prvního slotu (0=+X, 270=vpřed dolů k hrudníku)
SLOT_ANGLE_END = 350  # úhel posledního slotu

# Ramenní opěry - desky kotvené u horní hrany panelu, které se po nasazení
# kladou přes ramena a brání korzetu (a límci) sklouznout po hrudníku dolů.
# V tiskové orientaci (panel na plocho) jde o stěny stojící na horní ploše
# panelu; v souradnicích modelu je +Z směr dozadu k tělu, -Y nahoru k ramenům.
REST_INNER_X = 65  # vnitřní okraj opěry od středu (hrana nákrčníku je ~57)
REST_OUTER_X = 86  # vnější okraj opěry od středu
REST_TOP_OFFSET = 1  # posun opěry pod horní hranu (fillet kotvy vyžaduje materiál okolo)
REST_THICKNESS = 5  # tloušťka opěry
REST_REACH = 50  # dosah opěry přes rameno (výška stěny v tisku)
REST_SLOPE_DROP = 9  # pokles opěry k ramennímu kloubu (svah ramene od krku)
REST_BASE_FILLET = 2  # zaoblení kotvy opěry v panelu
REST_TOP_FILLET = 2  # zaoblení zadní hrany opěry


def build_korzet() -> Workplane:
    """Vytvoří podpůrný korzet na ramena, k němuž se suchými zipy připevňuje límec."""
    body = cq.Workplane("XY")
    body = shoulder_panel(body)
    body = neck_hole(body)
    body = shoulder_rest(body, 1)
    body = shoulder_rest(body, -1)
    body = zip_tie_slots(body)
    return body


def shoulder_panel(workplane: Workplane) -> Workplane:
    """Tělo korzetu - lichoběžník 200/140 x 100 se zaoblenými rohy, vytištěný na plocho."""
    half_top = compensated_top_half_width()
    half_bottom = PANEL_BOTTOM_WIDTH / 2
    return (workplane
            .moveTo(-half_top, 0)
            .lineTo(-half_bottom, -PANEL_HEIGHT)
            .lineTo(half_bottom, -PANEL_HEIGHT)
            .lineTo(half_top, 0)
            .close()
            .extrude(PANEL_THICKNESS)
            .edges("|Z")
            .fillet(CORNER_FILLET))


def compensated_top_half_width() -> float:
    """Půlšířka horní hrany před zaoblením rohů.

    Zaoblení CORNER_FILLET zmenšuje maximální šířku panelu o r*(cot(phi/2)-1),
    kde phi je vnitřní úhel horního rohu. Sklon boku ale závisí na této
    (ještě neznámé) šířce, proto řešíme pevný bod iterativně.

    Returns:
        Půlšířka horní hrany před aplikací zaoblení.
    """
    half = PANEL_TOP_WIDTH / 2
    for _ in range(10):
        run = half - PANEL_BOTTOM_WIDTH / 2  # vodorovný sklon boku
        phi = math.acos(run / math.hypot(run, PANEL_HEIGHT))  # vnitřní úhel horního rohu
        half = PANEL_TOP_WIDTH / 2 + CORNER_FILLET * (1 / math.tan(phi / 2) - 1)
    return half


def neck_hole(body: Workplane) -> Workplane:
    """Vyřízne díru pro krk; nahoře se otevírá do horní hrany jako nákrčník."""
    body = (body
            .faces(">Z")
            .workplane()
            .center(0, NECK_CENTER_Y)
            .circle(NECK_DIAMETER / 2)
            .cutThruAll())
    # Zaoblit svislé hrany v průsečíku nákrčníku s horní hranou (bod y=0)
    neck_half = math.sqrt((NECK_DIAMETER / 2) ** 2 - NECK_CENTER_Y ** 2)
    return (body
            .edges("|Z")
            .edges(selectors.BoxSelector((-neck_half - 5, -5, -1),
                                         (neck_half + 5, 5, PANEL_THICKNESS + 1)))
            .fillet(NECK_EDGE_FILLET))


def shoulder_rest(body: Workplane, side: int) -> Workplane:
    """Přidá ramenní opěru - desku ležící po nasazení na svahu ramene.

    Opěra je kotvená u horní hrany panelu a svou spodní (ležící) plochou
    kopíruje pokles ramene od krku k ramennímu kloubu. Korzet tak visí
    na ramenech a límec drží na místě.

    Args:
        body: Panel s vyříznutou dírou pro krk.
        side: Strana opěry (+1 vpravo, -1 vlevo).

    Returns:
        Tělo s přidanou opěrou.
    """
    x_in = side * REST_INNER_X
    x_out = side * REST_OUTER_X
    y_top = -REST_TOP_OFFSET
    y_bottom = y_top - REST_THICKNESS
    rest = (cq.Workplane("XY", origin=(0, 0, PANEL_THICKNESS))
            .polyline([(x_in, y_top),
                       (x_out, y_top - REST_SLOPE_DROP),
                       (x_out, y_bottom - REST_SLOPE_DROP),
                       (x_in, y_bottom)])
            .close()
            .extrude(REST_REACH))
    body = body.union(rest)
    x_min, x_max = min(x_in, x_out), max(x_in, x_out)
    y_min, y_max = y_bottom - REST_SLOPE_DROP, y_top
    # kotva opěry v panelu
    body = (body
            .edges(selectors.BoxSelector((x_min - 1, y_min - 1, PANEL_THICKNESS - 0.1),
                                         (x_max + 1, y_max + 0.1, PANEL_THICKNESS + 0.1)))
            .fillet(REST_BASE_FILLET))
    # zadní (nejvyšší) hrana opěry přes rameno
    body = (body
            .edges(selectors.BoxSelector((x_min - 1, y_min - 1, PANEL_THICKNESS + REST_REACH - 1),
                                         (x_max + 1, y_max + 0.1, PANEL_THICKNESS + REST_REACH + 1)))
            .fillet(REST_TOP_FILLET))
    return body


def zip_tie_slots(body: Workplane) -> Workplane:
    """Vyřízne radiální sloty pro suché zipy podél okraje nákrčníku."""
    for angle in slot_angles():
        rad = math.radians(angle)
        point = (SLOT_RADIUS * math.cos(rad),
                 NECK_CENTER_Y + SLOT_RADIUS * math.sin(rad))
        cutter = (cq.Workplane("XY")
                  .pushPoints([point])
                  .slot2D(SLOT_LENGTH, SLOT_WIDTH, angle=angle)
                  .extrude(PANEL_THICKNESS + 2, both=True))
        body = body.cut(cutter)
    return body


def slot_angles() -> list:
    """Úhly slotů rovnoměrně na oblouku kolem krku, symetricky k ose Y.

    Returns:
        Seznam úhlů ve stupních (0=+X, 270=směr k hrudníku).
    """
    if SLOT_COUNT == 1:
        return [(SLOT_ANGLE_START + SLOT_ANGLE_END) / 2]
    step = (SLOT_ANGLE_END - SLOT_ANGLE_START) / (SLOT_COUNT - 1)
    return [SLOT_ANGLE_START + i * step for i in range(SLOT_COUNT)]


def main():
    """Hlavní workflow."""
    render(build_korzet(), "limec_korzet.stl")


if __name__ == "__main__":
    main()
