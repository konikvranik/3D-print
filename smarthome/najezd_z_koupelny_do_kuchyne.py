import sys
import os

import cadquery as cq

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import render

# Rozměry nájezdu (šířka, hloubka, výška)
# Uživatel požaduje: šířka 250, výška 30, hloubka 65
WIDTH = 250.0
DEPTH = 65.0
HEIGHT = 30.0


def build_ramp():
    """Vytvoří nájezd pro vysavač s rozměry 250x30x65 mm.

    Nájezd je tvořený profilem v rovině XZ, který je následně vytažen do šířky.
    Profil má výšku HEIGHT a délku DEPTH.
    """

    # Vytvoříme profil nájezdu (pravúhlý trojúhelník s odlehčením na špičce)
    # Pro 3D tisk je dobré mít malou hranu na začátku, aby se první vrstva lépe uchytila
    tip_height = 0.5

    # Profil v rovině XZ (v CadQuery je defaultní pracovní rovina XY)
    # X=hloubka, Z=výška
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

    # Přidáme zaoblení na horní hraně (kde je plná výška)
    # Selektor ">Z" vybere horní hrany, "|Y" hrany rovnoběžné s osou Y (šířka)
    ramp = ramp.edges("|Y").edges(">Z").fillet(2.0)

    # Otočení tak, aby ležel na nájezdové ploše (šířka 250, výška 30, hloubka 65)
    # Úhel sklonu nájezdu: atan((HEIGHT - tip_height) / DEPTH)
    import math
    angle = math.degrees(math.atan2(HEIGHT - tip_height, DEPTH))
    
    # Otočíme kolem osy Y (šířka)
    # Původně je profil v rovině XZ, extrude do směru Y.
    # Aby šikmá plocha ležela na podložce (rovina XY), otočíme model o vypočtený úhel.
    return ramp.rotate((0, 0, 0), (0, 1, 0), 180 + angle)


def main():
    """Hlavní workflow."""
    render(build_ramp(), "out/najezd_z_koupelny_do_kuchyne.stl")


if __name__ == "__main__":
    main()
