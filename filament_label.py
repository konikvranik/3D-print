import cadquery as cq

texts = ["ABS", "PET", "PLA", "PETG", "rPET"]

font_size = 7
tube_diameter = 3.9
cylinder_outer_diameter = 7.2
clip_length = 5
box_height = 3


def clip_body(object):
    object = object.faces("<X").workplane(offset=-box_length / 2).cylinder(clip_length, cylinder_outer_diameter / 2,
                                                                           centered=(True, False, True))
    return object.faces("<X").workplane(offset=-box_length / 2).box(cylinder_outer_diameter,
                                                                    cylinder_outer_diameter / 2,
                                                                    clip_length, centered=(True, False, True))


def clip_circle_cut(object):
    return object.faces("right").workplane().move(0, cylinder_outer_diameter / 2 + 1).circle(
        tube_diameter / 2).cutThruAll().workplane()


for text in texts:
    wp = cq.Workplane("XY")

    t = wp.workplane(offset=-1.8).text(text, font_size, .4)
    box_length = t.val().BoundingBox().xlen + font_size * .6
    box_width = t.val().BoundingBox().ylen + font_size * .6

    object = wp.box(box_length, box_width, box_height)
    object = clip_body(object)

    object = clip_circle_cut(object)
    object = object.move(-(tube_diameter - .8) / 2, box_height / 2).rect(tube_diameter - .8,
                                                                         clip_length + tube_diameter,
                                                                         centered=False).cutThruAll()
    object = object.workplane().move(-(tube_diameter + .7) / 2, box_height / 2 + clip_length-.5).rect(tube_diameter + .7,
                                                                                                   clip_length + tube_diameter,
                                                                                                   centered=False).cutThruAll()
    first = object.workplane().move(tube_diameter / 2 + .11, cylinder_outer_diameter - 1.3).cylinder(clip_length,
                                                                                                      1 / 2)
    second = first.mirror(mirrorPlane="XZ", basePointVector=(0, 0, 0))
    object = object.union(first).union(second)

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
