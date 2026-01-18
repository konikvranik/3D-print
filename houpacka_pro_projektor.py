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

num_teeth = 12
tooth_depth = 2
tooth_width = 4


def build_toothed_cylinder(radius, cylinder_height):
    # 1. Základní válec
    cylinder = cq.Workplane("XY").cylinder(cylinder_height, radius)

    # 2. Definice jednoho zubu
    # Zub vytvoříme jako malý kvádr na okraji válce
    tooth = (
        cq.Workplane("XY")
        .workplane(offset=cylinder_height / 2)  # Přesun na horní plochu pro kreslení profilu
        .center(radius, 0)
        .rect(tooth_depth * 2, tooth_width)
        .extrude(-cylinder_height)  # Protlačení skrz celou výšku válce
    )

    # 3. Rozmístění zubů po obvodu (polární pole)
    teeth = (
        cq.Workplane("XY")
        .polarArray(radius=radius, startAngle=0, angle=360, count=num_teeth)
        .eachpoint(lambda loc: tooth.val().located(loc))
    )

    # Spojení válce se zuby
    return cylinder.union(teeth)


def build_matching_block(toothed_cylinder):
    # Vytvoření bloku, ve kterém bude výřez
    block_size = 60
    block = (
        cq.Workplane("XY")
        .box(block_size, block_size, outer_width)
        .translate((outer_radius + 10, 0, 0))  # Posuneme blok kousek stranou od středu válce
    )

    # Odečtení válce od bloku (vytvoření negativu)
    # cut() vytvoří v bloku přesný výřez podle tvaru válce i se zuby
    return block.cut(toothed_cylinder)


def build_case():
    wp = cq.Workplane("XY")
    return wp.cylinder(outer_width, outer_depth / 4)


def main():
    cylinder = build_toothed_cylinder(outer_depth / 2, outer_width)
    block = build_matching_block(cylinder)

    # Zobrazení obou objektů najednou
    # (V PyCharm/CadQuery editoru se zobrazí jako sestava)
    from common import render
    render(cylinder.union(block))


if __name__ == "__main__":
    main()
