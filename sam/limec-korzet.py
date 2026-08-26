import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import math

from common import render, cq
from cadquery import Workplane, selectors

# Korzet je vodorovná deska položená na ramena. Krk prochází nákrčníkem
# u přední hrany, límec (limec.py) stojí na desce kolem krku a připevňuje
# se suchými zipy. Deska se nosí stranou s opěrami dolů:
# přední opěry se opírají o hrudník, zadní opěrka o páteř - společně drží
# desku (a límec) na místě vpřed i vzad.
# V souřadnicích modelu (= tisková orientace): přední hrana je y=0,
# zadní hrana y=-PANEL_HEIGHT, opěry stojí na ploše z=PANEL_THICKNESS.

PANEL_TOP_WIDTH = 200  # šířka přední hrany u krku (leží na ramenou)
PANEL_BOTTOM_WIDTH = 140  # šířka zadní hrany
PANEL_HEIGHT = 100  # hloubka desky od přední hrany k zadní
PANEL_THICKNESS = 4  # tloušťka desky

NECK_DIAMETER = 120  # průměr díry pro krk
NECK_CENTER_Y = -20  # střed díry pro krk pod přední hranou -> otvor se otevírá vpřed jako nákrčník

CORNER_FILLET = 20  # zaoblení vnějších rohů desky
NECK_EDGE_FILLET = 5  # zaoblení hran, kde nákrčník protíná přední hranu

# Sloty pro suché zipy kolem nákrčníku; zip prochází deskou a objímá spodní
# přítlačnou plochu límce (limec.py), která má 6 protilehlých děr.
SLOT_COUNT = 6  # počet slotů (odpovídá HOLE_COUNT v limec.py)
SLOT_RADIUS = 70  # vzdálenost středů slotů od středu díry pro krk
SLOT_WIDTH = 3  # šířka slotu, únosný suchý zip s vůlí
SLOT_LENGTH = 10  # délka slotu v radiálním směru, umožňuje doladit polohu zipu
SLOT_ANGLE_START = 190  # úhel prvního slotu (0=+X, 270=vpřed k hrudníku)
SLOT_ANGLE_END = 350  # úhel posledního slotu

# Přední opěry - stěny kotvené u přední hrany po stranách nákrčníku.
# Po nasazení míří dolů a opírají se o hrudník; brání desce (a límci)
# sklouznout po ramenou dozadu.
REST_INNER_X = 65  # vnitřní okraj opěry od středu (hrana nákrčníku je ~57)
REST_OUTER_X = 86  # vnější okraj opěry od středu
REST_TOP_OFFSET = 1  # posun opěry od přední hrany (okraj materiálu pro čistou geometrii)
REST_THICKNESS = 5  # tloušťka opěry
REST_REACH = 50  # délka opěry dolů k hrudníku
REST_SLOPE_DROP = 9  # pokles opěry k ramennímu kloubu (svah ramene od krku)
REST_TOP_FILLET = 2  # zaoblení dolního konce opěry

# Zadní opěrka - širší stěna uprostřed zadní hrany. Po nasazení se opírá
# o páteř (vzdálenost hrudník-páteř je ~140 mm, přední a zadní opěra se
# proto doplňují) a brání desce sklouznout dopředu.
BACK_BRACE_WIDTH = 70  # šířka zadní opěrky (přední opěry mají po 21 mm)
BACK_BRACE_REACH = 50  # délka zadní opěrky dolů k páteři
BACK_BRACE_THICKNESS = 5  # tloušťka zadní opěrky (stejná jako přední opěry)


def build_korzet() -> Workplane:
    """Vytvoří korzet - vodorovnou desku na ramena s předními a zadními opěrami."""
    body = cq.Workplane("XY")
    body = shoulder_panel(body)
    body = neck_hole(body)
    body = shoulder_rest(body, 1)
    body = shoulder_rest(body, -1)
    body = back_brace(body)
    body = zip_tie_slots(body)
    return body


def shoulder_panel(workplane: Workplane) -> Workplane:
    """Tělo desky - lichoběžník se zaoblenými rohy, vytištěný na plocho."""
    half_top = compensated_front_half_width()
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


def compensated_front_half_width() -> float:
    """Půlšířka přední hrany před zaoblením rohů.

    Zaoblení CORNER_FILLET zmenšuje maximální šířku desky o r*(cot(phi/2)-1),
    kde phi je vnitřní úhel předního rohu. Sklon boku ale závisí na této
    (ještě neznámé) šířce, proto řešíme pevný bod iterativně.

    Returns:
        Půlšířka přední hrany před aplikací zaoblení.
    """
    half = PANEL_TOP_WIDTH / 2
    for _ in range(10):
        run = half - PANEL_BOTTOM_WIDTH / 2  # vodorovný sklon boku
        phi = math.acos(run / math.hypot(run, PANEL_HEIGHT))  # vnitřní úhel rohu
        half = PANEL_TOP_WIDTH / 2 + CORNER_FILLET * (1 / math.tan(phi / 2) - 1)
    return half


def neck_hole(body: Workplane) -> Workplane:
    """Vyřízne díru pro krk; vpředu se otevírá do přední hrany jako nákrčník."""
    body = (body
            .faces(">Z")
            .workplane()
            .center(0, NECK_CENTER_Y)
            .circle(NECK_DIAMETER / 2)
            .cutThruAll())
    # Zaoblit svislé hrany v průsečíku nákrčníku s přední hranou (bod y=0)
    neck_half = math.sqrt((NECK_DIAMETER / 2) ** 2 - NECK_CENTER_Y ** 2)
    return (body
            .edges("|Z")
            .edges(selectors.BoxSelector((-neck_half - 5, -5, -1),
                                         (neck_half + 5, 5, PANEL_THICKNESS + 1)))
            .fillet(NECK_EDGE_FILLET))


def shoulder_rest(body: Workplane, side: int) -> Workplane:
    """Přidá přední opěru - stěnu opírající se po nasazení o hrudník.

    Opěra je kotvená u přední hrany desky po straně nákrčníku a míří
    dolů; spodní okraj je vůči přední hraně zešikmený o REST_SLOPE_DROP,
    aby kopíroval klesající svah ramene od krku k ramennímu kloubu.

    Args:
        body: Deska s vyříznutou dírou pro krk.
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
    # dolní konec opěry
    # (kotvící fillet u desky záměnně chybí - OCC ho u přední hrany
    # desky neumí korektně postavit a poškodil by těleso)
    body = (body
            .edges(selectors.BoxSelector((x_min - 1, y_min - 1, PANEL_THICKNESS + REST_REACH - 1),
                                         (x_max + 1, y_max + 0.1, PANEL_THICKNESS + REST_REACH + 1)))
            .fillet(REST_TOP_FILLET))
    return body


def back_brace(body: Workplane) -> Workplane:
    """Přidá zadní opěrku - širokou stěnu uprostřed zadní hrany desky.

    Po nasazení se opírá o páteř; spolu s předními opěrami na hrudníku
    tak deska nemůže klouzat dopředu ani dozadu.
    """
    half_w = BACK_BRACE_WIDTH / 2
    y_center = -PANEL_HEIGHT + REST_TOP_OFFSET + BACK_BRACE_THICKNESS / 2
    # pilulkový průřez stěny (zaoblené konce, tloušťka = šířka slotu)
    brace = (cq.Workplane("XY", origin=(0, 0, PANEL_THICKNESS))
             .center(0, y_center)
             .slot2D(BACK_BRACE_WIDTH, BACK_BRACE_THICKNESS)
             .extrude(BACK_BRACE_REACH))
    body = body.union(brace)
    # dolní konec opěrky
    body = (body
            .edges(selectors.BoxSelector((-half_w - 1, y_center - BACK_BRACE_THICKNESS - 1,
                                          PANEL_THICKNESS + BACK_BRACE_REACH - 1),
                                         (half_w + 1, y_center + BACK_BRACE_THICKNESS + 1,
                                          PANEL_THICKNESS + BACK_BRACE_REACH + 1)))
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
