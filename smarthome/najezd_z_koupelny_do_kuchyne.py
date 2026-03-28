import sys
import os

import cadquery as cq

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import render

# Rozměry nájezdu (šířka, hloubka, výška)
# Uživatel požaduje: šířka 250, výška 30, hloubka 65
WIDTH = 245.0
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

    # Přidáme zaoblení (fillet) podle požadavku:
    # 1. Boční hrany nájezdové rampy (šikmé hrany na bocích)
    # 2. Spodní kolmá hrana (náběhová hrana u země)
    
    # Náběhová hrana (rovnoběžná s Y, na začátku X=0)
    # Použijeme menší poloměr, aby nedocházelo ke kolizi s tip_height
    # Zkusíme 0.2 mm pro náběhovou hranu
    try:
        # Vybereme náběhovou hranu (ta úplně dole u X=0)
        front_edge = ramp.edges("|Y").edges("<X").edges("<Z")
        ramp = ramp.newObject(front_edge.objects).fillet(3)
    except:
        print("Warning: Front fillet failed.")
    
    # Boční šikmé hrany
    try:
        skew_edges = [e for e in ramp.faces("|Y").edges().objects 
                      if e.geomType() == "LINE" and 
                      not (abs(e.endPoint().sub(e.startPoint()).normalized().dot(cq.Vector(1,0,0))) > 0.99 or
                           abs(e.endPoint().sub(e.startPoint()).normalized().dot(cq.Vector(0,1,0))) > 0.99 or
                           abs(e.endPoint().sub(e.startPoint()).normalized().dot(cq.Vector(0,0,1))) > 0.99)]
        if skew_edges:
            ramp = ramp.newObject(skew_edges).fillet(3)
    except Exception as e:
        print(f"Warning: Side fillet failed: {e}")
    
    # POZOR: fillet na hranách může změnit stack. Musíme zajistit, aby stack obsahoval původní těleso (Solid)
    # pro následné operace (jako rotace). V CadQuery fillet na hranách vrací těleso s aplikovaným zaoblením.
    # Ale pokud jsme na stacku měli jen hrany, musíme se vrátit k tělesu.
    # Většinou .fillet() na hranách v CQ funguje tak, že vybere hrany ze stacku a aplikuje to na Solid, 
    # ze kterého pocházejí.

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
    # Určíme absolutní cestu k výstupnímu souboru v kořenovém adresáři projektu
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    output_path = os.path.join(project_root, "out", "najezd_z_koupelny_do_kuchyne.stl")
    
    render(build_ramp(), output_path)


if __name__ == "__main__":
    main()
