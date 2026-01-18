from cadquery import cq

outer_width = 152
inner_width = 133
outer_depth = 170
inner_depth = 151
socket_width = 15
socket_height = 7
step_height = 11
socket_offset = 33
outer_radius = 20

num_teeth = 240
tooth_depth = 2


def build_toothed_cylinder(radius, cylinder_height, num_teeth=60, tooth_depth=2):
    import math

    # Vypočítáme úhel pro jeden zub
    angle_per_tooth = 360 / num_teeth

    # Vytvoříme ozubení jako průběžný polygon po obvodu
    points = []
    for i in range(num_teeth):
        # Úhel pro začátek zubu (údolí)
        angle_start = math.radians(i * angle_per_tooth)
        # Úhel pro vrchol zubu
        angle_peak = math.radians(i * angle_per_tooth + angle_per_tooth / 2)

        # Bod v údolí (na poloměru radius)
        x_start = radius * math.cos(angle_start)
        y_start = radius * math.sin(angle_start)
        points.append((x_start, y_start))

        # Bod na vrcholu (na poloměru radius + tooth_depth)
        x_peak = (radius + tooth_depth) * math.cos(angle_peak)
        y_peak = (radius + tooth_depth) * math.sin(angle_peak)
        points.append((x_peak, y_peak))

    # Vytvoříme profil ozubení jako uzavřený polygon
    result = (
        cq.Workplane("XY")
        .polyline(points)
        .close()
        .extrude(cylinder_height)
    )

    return result


def build_matching_block(width, depth, height, cylinder):
    # Vytvoření bloku, ve kterém bude výřez
    # Blok bude dostatečně velký, aby se do něj válec vešel

    # Vytvoříme blok a posuneme ho tak, aby se částečně překrýval s válcem
    # Válec je centrovaný na (0,0), blok posuneme v ose X
    block = (
        cq.Workplane("XY")
        .box(width, depth, height)
        .translate((depth / 2, 0, height / 2))
    )

    # Odečtení válce od bloku (vytvoření negativu)
    # Musíme zajistit, aby válec byl ve správné výšce (také od 0 nahoru)
    cylinder_to_cut = cylinder.translate((0, 0, 0))  # Už je extrudovaný od 0 nahoru

    return block.cut(cylinder_to_cut)


def build_case():
    wp = cq.Workplane("XY")
    return wp.cylinder(outer_width, outer_depth / 4)


def main():
    # Vytvoření válce se zuby
    cylinder = build_toothed_cylinder(outer_depth / 2, outer_width, num_teeth=24, tooth_depth=3)
    # Vytvoření bloku s výřezem pro tento válec
    block = build_matching_block(outer_width, outer_depth, outer_depth / 2 + 20, cylinder)

    # Export a zobrazení
    from common import render
    # Vytvoříme sestavu (Assembly) pro lepší manipulaci s více objekty, 
    # nebo je prostě přidáme k sobě. Pro render() v common.py stačí add().
    # Blok je již posunutý v build_matching_block, tak aby se "zakousl" do válce.
    render(cylinder.add(block))


if __name__ == "__main__":
    main()
