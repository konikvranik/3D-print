import cadquery as cq

def create_cone(base_diameter=40, top_diameter=60, height=150, inner_diameter=12.5):
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
            .circle(base_diameter/2)
            .workplane(offset=height)
            .circle(top_diameter/2)
            .loft()
            .faces("<Z")
            .workplane()
            .circle(inner_diameter/2)
            .cutThruAll())
    return cone

def create_gardena_connector(params=None):
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
    # Výchozí parametry Gardena konektoru
    default_dims = {
        'total_length': 29.0,        # Celková délka konektoru
        'outer_diameter': 20.8,      # Základní vnější průměr
        'inner_diameter': 12.5,      # Průměr vnitřního otvoru
        'stop_ring_diameter': 25.0,  # Průměr dorazového kroužku
        'stop_ring_width': 4.0,      # Šířka dorazového kroužku
        'stop_ring_position': 23.0,  # Pozice dorazového kroužku od začátku
        'groove1_pos': 10.0,         # Pozice první drážky od konce
        'groove1_width': 3.0,        # Šířka první drážky
        'groove1_depth': 1.4,        # Hloubka první drážky
        'groove2_pos': 16.0,         # Pozice druhé drážky od konce
        'groove2_width': 3.0,        # Šířka druhé drážky
        'groove2_depth': 1.4,        # Hloubka druhé drážky
        'seal_pos': 22.0,            # Pozice těsnící drážky od konce
        'seal_width': 4.0,           # Šířka těsnící drážky
        'seal_inner_diameter': 16.2, # Vnitřní průměr v místě těsnění
        'chamfer_length': 2.5,       # Délka zkosení na konci
    }
    
    # Použij poskytnuté parametry nebo výchozí
    dims = default_dims
    if params:
        dims.update(params)
    
    wp = cq.Workplane("XY")
    
    # Základní tělo konektoru
    base = (wp.circle(dims['outer_diameter']/2)
           .extrude(dims['total_length']))
    
    # Dorazový kroužek
    stop_ring = (wp.workplane(offset=dims['stop_ring_position'])
                .circle(dims['stop_ring_diameter']/2)
                .extrude(dims['stop_ring_width']))
    
    # První drážka pro zacvaknutí
    groove1 = (wp.workplane(offset=dims['groove1_pos'])
              .circle(dims['outer_diameter']/2)
              .circle(dims['outer_diameter']/2 - dims['groove1_depth'])
              .extrude(dims['groove1_width']))
              
    # Druhá drážka pro zacvaknutí
    groove2 = (wp.workplane(offset=dims['groove2_pos'])
              .circle(dims['outer_diameter']/2)
              .circle(dims['outer_diameter']/2 - dims['groove2_depth'])
              .extrude(dims['groove2_width']))
              
    # Drážka pro těsnění (O-kroužek)
    seal_groove = (wp.workplane(offset=dims['seal_pos'])
                  .circle(dims['outer_diameter']/2)
                  .circle(dims['seal_inner_diameter']/2)
                  .extrude(dims['seal_width']))
    
    # Vnitřní otvor - průchod vody
    inner_hole = (wp.circle(dims['inner_diameter']/2)
                 .extrude(dims['total_length']))
    
    # Zkosení na konci
    chamfer = (wp.workplane(offset=dims['total_length'])
              .circle(dims['outer_diameter']/2)
              .workplane(offset=dims['chamfer_length'])
              .circle(dims['outer_diameter']/2 - 1.5)
              .loft())
    
    # Složení všech částí
    result = base.union(stop_ring).union(chamfer)
    result = result.cut(groove1).cut(groove2).cut(seal_groove).cut(inner_hole)
    
    # Zaoblení hran
    try:
        # Zaoblení vnějších hran
        result = result.edges("|Z").fillet(0.5)
        # Zaoblení vnitřních hran v drážkách
        result = result.edges(">Z and |X").fillet(0.3)
    except:
        print("Varování: Některá zaoblení se nezdařila")
    
    return result

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
        .circle(body_diam/2)
        .workplane(offset=length)
        .circle(gardena_diam/2)
        .loft()
    )
    
    # Vnitřní průchod skrz přechod
    transition_hole = (
        cq.Workplane("XY")
        .circle(inner_diam/2)
        .extrude(length)
    )
    
    return transition.cut(transition_hole)

# Demonstrační kód pro použití funkcí (můžete smazat nebo upravit)
if __name__ == "__main__":
    # Vytvoření jednotlivých částí
    cone = create_cone()
    connector = create_gardena_connector()
    
    # Umístění konektoru na vrchol kužele
    connector_positioned = connector.translate((0, 0, 150))
    
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
    cq.exporters.export(result, "gardena_adapter.stl")