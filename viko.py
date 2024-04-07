import cadquery as cq

object = cq.Workplane("XY").cylinder(11 + 4, 107 / 2, centered=(True, True, False)).faces(
    "bottom").cut(
    cq.Solid.makeCylinder(92 / 2, 11)).edges().fillet(2)
object = object.faces("<Z").workplane(invert=True).cylinder(11 - 5.5, 107 / 2, angle=20,
                                                            centered=(True, True, False)).cut(
    cq.Solid.makeCylinder(83 / 2, 11))
object = object.rotateAboutCenter([0, 0, 1], 180).faces("<Z").workplane(invert=True).cylinder(11 - 5.5, 107 / 2, angle=20,
                                                                                              centered=(
                                                                                                  True, True,
                                                                                                  False)).cut(
    cq.Solid.makeCylinder(83 / 2, 11))

if 'show_object' not in globals():
    def show_object(*args, **kwargs):
        pass

show_object(object)

cq.exporters.export(object, "viko.stl")
