import os
import sys

import cadquery as cq
from cadquery import Workplane

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import render

# Rozměry nájezdu (šířka, hloubka, výška)
# Uživatel požaduje: šířka 250, výška 30, hloubka 65
WIDTH = 249.0
DEPTH = 65.0
HEIGHT = 30.0


def build_ramp():
    """Vytvoří nájezd pro vysavač s rozměry 250x30x65 mm.

    Nájezd je tvořený profilem v rovině XZ, který je následně vytažen do šířky.
    Profil má výšku HEIGHT a délku DEPTH.
    """

    # Vytvoříme profil nájezdu (pravúhlý trojúhelník s odlehčením na špičce)
    # Pro 3D tisk je dobré mít malou hranu na začátku, aby se první vrstva lépe uchytila.
    # Abychom mohli zaoblit hranu, musí být tato výška aspoň 1.0 mm.
    tip_height = 0

    # Profil v rovině XZ (X=hloubka, Z=výška)
    profile = (
        cq.Workplane("XZ")
        .moveTo(0, 0)
        .lineTo(DEPTH, 0)
        .lineTo(DEPTH, HEIGHT)
        .lineTo(0, tip_height)
        .close()
    )

    # Extrude (vytažení) do šířky (WIDTH)
    ramp = profile.extrude(WIDTH)

    # Otočení tak, aby ležel na nájezdové ploše (šířka 250, výška 30, hloubka 65)
    # Úhel sklonu nájezdu: atan((HEIGHT - tip_height) / DEPTH)
    import math
    angle = math.degrees(math.atan2(HEIGHT - tip_height, DEPTH))

    # Otočíme kolem osy Y (šířka) tak, aby šikmá plocha byla nahoře a vodorovná (pro tisk)
    # Původní orientace: 
    # Spodek (0,0)-(DEPTH,0) je v rovině Z=0.
    # Šikmá plocha (0, tip_height)-(DEPTH, HEIGHT).
    # Po otočení o (180 + angle) kolem Y:
    # Šikmá plocha bude v rovině Z=0.
    ramp = ramp.rotate((0, 0, 0), (0, 1, 0), 180 + angle)

    # Nyní aplikujeme zaoblení (fillet) na modelu v tiskové orientaci:
    # 1. Horní hrana u země (bývalá pata nájezdu u bodu 0,0) - je to ta nejvyšší hrana po otočení.
    # 2. Boční hrany, které byly původně šikmé (nyní jsou to vodorovné hrany v Z=0).

    # Zaoblení "nejvyšší" hrany (původní 0,0)
    try:
        # Po otočení o 180+angle, bod (0,0) v XZ se dostane na vrchol.
        top_edge = ramp.edges("|Y").edges(">Z")
        ramp = ramp.newObject(top_edge.objects).fillet(2.0)
    except Exception as e:
        print(f"Warning: Top fillet failed: {e}")

    return ramp


def side_fillet(ramp: Workplane, direction="<") -> Workplane:
    # Zaoblení bočních hran (původně šikmé, nyní leží v Z=0 na bocích)
    try:
        # Boční hrany v rovině podložky (Z=0)
        side_edges = ramp.edges("<Z").edges("%sY" % direction)
        ramp = ramp.newObject(side_edges.objects).fillet(5.0)
    except Exception as e:
        print(f"Warning: Side fillet failed: {e}")
    return ramp


def main():
    """Hlavní workflow."""
    # Určíme absolutní cestu k výstupnímu souboru v kořenovém adresáři projektu
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    output_path = os.path.join(project_root, "out", "najezd_z_koupelny_do_kuchyne_left.stl")
    render(side_fillet(build_ramp()), output_path)
    output_path = os.path.join(project_root, "out", "najezd_z_koupelny_do_kuchyne_right.stl")
    render(side_fillet(build_ramp(), ">"), output_path)


if __name__ == "__main__":
    main()
