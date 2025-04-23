import cadquery as cq
import gardena_connector as gc


def create_cone(base_diameter=40, top_diameter=60, height=150, inner_diameter=30):
    """
    Vytvoří kónický přechod s vnitřním otvorem.
    
    Parametry:
    ----------
    base_diameter : float
        Průměr základny konusu
    top_diameter : float
        Průměr horní části konusu
    height : float
        Výška konusu
    inner_diameter : float
        Průměr vnitřního otvoru
        
    Vrací:
    ------
    cadquery.Workplane
        Kónický přechod jako CadQuery objekt
    """
    wp = cq.Workplane("XY")
    cone = (wp.workplane()
            .circle(base_diameter / 2)
            .workplane(offset=height)
            .circle(top_diameter / 2)
            .loft()
            .clean())

    # Vytvoření vnitřního kónického otvoru
    inner_cone = (cq.Workplane("XY")
                  .circle(inner_diameter / 2)
                  .workplane(offset=height - 2)
                  .circle(8.7 / 2)
                  .loft()
                  .faces(">Z")
                  .workplane()
                  .cylinder(2, 8.7 / 2, centered=[True, True, False]))

    cone = cone.faces(">Z").edges().fillet(14).faces("<Z").edges().fillet(1)
    return cone.cut(inner_cone).faces("<Z").edges().fillet(1).clean()


def create_transition(body_diam, gardena_diam, length, inner_diam=10.0):
    """
    Vytvoří přechodový kužel mezi tělem a konektorem.
    
    Parametry:
    ----------
    body_diam : float
        Průměr těla, ke kterému se připojuje přechod
    gardena_diam : float
        Průměr Gardena konektoru
    length : float
        Délka přechodového kužele
    inner_diam : float
        Průměr vnitřního otvoru
        
    Vrací:
    ------
    cadquery.Workplane
        Přechodový kužel jako CadQuery objekt
    """
    # Vytvoření přechodového kužele
    transition = (
        cq.Workplane("XY")
        .circle(body_diam / 2)
        .workplane(offset=length)
        .circle(gardena_diam / 2)
        .loft()
    )

    # Vnitřní průchod skrz přechod
    transition_hole = (
        cq.Workplane("XY")
        .circle(inner_diam / 2)
        .extrude(length)
    )

    return transition.cut(transition_hole)


# Demonstrační kód pro použití funkcí (můžete smazat nebo upravit)
if __name__ == "__main__":
    # Vytvoření jednotlivých částí
    cone = create_cone()
    connector = gc.create_gardena_connector()

    # Umístění konektoru na vrchol kužele
    connector_positioned = connector.translate((0, 0, 150 - 2))

    # Combine the parts
    result = cone.union(connector_positioned)

    # Add fillets where possible
    try:
        result = result.edges("%LINE").fillet(0.5)
    except:
        print("Varování: Zaoblení hran se nezdařilo, pokračuji bez zaoblení")

    # Check if show_object is available (for CQ-editor)
    if 'show_object' not in globals():
        def show_object(*args, **kwargs):
            pass

    show_object(result)

    # Export the model to STL
    cq.exporters.export(result, "gardena_adapter.stl",None, 0.00001,  0.1)
