import cadquery as cq

texts = ["ABS", "PET", "PLA", "PETG", "rPET"]

font_size = 8

for text in texts:
    wp = cq.Workplane("XY")

    t = wp.workplane(offset=-1.8).text(text, font_size, .4)
    object = wp.box(t.val().BoundingBox().xlen + font_size * .6, t.val().BoundingBox().ylen + font_size * .6, 3)
    object = object.copyWorkplane(cq.Workplane("right", origin=(0, 0, 9 / 2 - 1.5))).cylinder(10, 9 / 2,
                                                                                              centered=[True, True,
                                                                                                        True],
                                                                                              angle=195).faces(
        ">X").workplane().circle(4.2 / 2).cutThruAll()

    t = t.mirror("YZ")

    object = object.cut(t)

    o = 0.3

    assembly = cq.Assembly()
    assembly.add(object, name="body")
    assembly.add(t, name="text")
    assembly.constrain("body", cq.Vertex.makeVertex(1, 1, -1 + o), "text",
                       cq.Vertex.makeVertex(1, 1, -1), "Point")
    assembly.constrain("body", cq.Vertex.makeVertex(1, -1, 1 + o), "text",
                       cq.Vertex.makeVertex(1, -1, 1), "Point")
    assembly.constrain("body", cq.Vertex.makeVertex(-1, 1, 1 + o), "text",
                       cq.Vertex.makeVertex(-1, 1, 1), "Point")
    assembly.solve()
    assembly.save("%s.step" % text)

    if 'show_object' not in globals():
        def show_object(*args, **kwargs):
            pass

    show_object(object)

    cq.exporters.export(object, "%s.stl" % text)
