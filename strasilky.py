import cadquery as cq

width = 210
height = 320
glass = 2.6
thick = 1
depth = 12

hole = 10


def top_part():
    s = cq.StringSyntaxSelector
    box = cq.Workplane("XY") \
        .rect(width + 2 * thick, height + 2 * thick) \
        .extrude(depth) \
        .faces('+Z') \
        .rect(width - 2 * glass - 2 * thick, height - 2 * glass - 2 * thick) \
        .cutThruAll().faces('>Z').shell(-thick)
    cell = cq.Workplane("XY").move(-width / 2 + hole / 2 + thick, -height / 2 + hole / 2 + thick) \
        .box(hole + thick, hole + thick, thick).faces(
        '>Z').rect(
        hole, hole).cutThruAll()
    for i in range(thick, width - hole - 2 * thick, hole + 2 * thick):
        for j in range(thick, int(height / 2) - hole - 2 * thick, hole + 2 * thick):
            cell = cell.union(cell.translate((hole + thick + i, hole + thick + j, 0)))
            pass

    return box.union(cell)  # .faces(s('>Z') + s('<Z') - s('<X') - s('>X')).fillet(1.3)


show_object(top_part())
