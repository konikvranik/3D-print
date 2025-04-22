import cadquery as cq
from ezdxf.render.forms import cylinder


def create_gardena_connector(wp=cq.Workplane("XY")):
    """
    Vytvoří Gardena rychlospojku s přesnými parametry.

    Parametry:
    ----------
    params : dict, optional
        Slovník s parametry konektoru. Pokud None, použijí se výchozí hodnoty.

    Vrací:
    ------
    cadquery.Workplane
        Gardena konektor jako CadQuery objekt
    """

    wp = wp.cylinder(2, 30 / 2, centered=[True, True, False])
    # Základní tělo konektoru
    wp = wp.faces(">Z").workplane().cylinder(12.5, 13.7 / 2, centered=[True, True, False])

    wp = wp.faces(">Z[-2]").edges().filter(lambda e: e.radius() < 10).fillet(8)

    # Dorazový kroužek
    wp = wp.faces(">Z").workplane().cylinder(1.5, 16.9 / 2, centered=[True, True, False])
    wp = wp.faces(">Z").circle(16.9 / 2).workplane(offset=1).circle(15.85 / 2).loft()

    # Drážky pro těsnění
    wp = wp.faces(">Z").workplane().cylinder(2.5, 15.85 / 2, centered=[True, True, False])
    wp = wp.faces(">Z").workplane().cylinder(3, 11.3 / 2, centered=[True, True, False])

    # Vytvoření víčka
    wp = wp.faces(">Z").workplane().cylinder(2.6, 15.85 / 2, centered=[True, True, False])

    # Získání hran pro zaoblení
    wp = wp.faces(">Z[-2]").edges().filter(lambda e: e.radius() < 7).fillet(1.4999)

    wp = wp.faces(">Z[-3]").edges().filter(lambda e: e.radius() < 7).fillet(1.4999)

    wp = wp.faces(">Z").fillet(1.5)

    wp = wp.faces(">Z").workplane().circle(8.7 / 2).cutThruAll()

    wp = wp.faces(">Z").fillet(.5)

    return wp


# Demonstrační kód pro použití funkcí (můžete smazat nebo upravit)
if __name__ == "__main__":
    # Vytvoření jednotlivých částí
    connector = create_gardena_connector()

    # Check if show_object is available (for CQ-editor)
    if 'show_object' not in globals():
        def show_object(*args, **kwargs):
            pass

    show_object(connector)

    # Export the model to STL
    cq.exporters.export(connector, "gardena_connector.stl")
