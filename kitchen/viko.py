import cadquery as cq

outer_diameter = 107
inner_height = 11 + 4
outer_height = inner_height + 4
inner_diameter = 92 + 1
tip_offset = 4
tip_height = 5.5
tip_length = 9


def make_outer_shell(wp):
    return (wp.cylinder(outer_height, outer_diameter / 2, centered=(True, True, False))
            .faces("<Z")
            .circle(inner_diameter / 2).cutBlind(inner_height)
            )


def make_tips(object):
    first = object.cylinder(tip_height, (outer_diameter - tip_offset) / 2, angle=20,
                            centered=(True, True, False)).faces("<Z").moveTo(0, 0).circle(
        (inner_diameter - tip_length) / 2).cutBlind(inner_height).rotate([0, 0, 0], [0, 0, 1], -10)
    second = first.mirror(mirrorPlane="YZ", basePointVector=(0, 0, 0))
    both = first.union(second).combineSolids()
    return both


wp = cq.Workplane("XY")
object = make_outer_shell(wp).edges().fillet(2)
tips = make_tips(wp).edges().fillet(2)

object = object.union(tips)

if 'show_object' not in globals():
    def show_object(*args, **kwargs):
        pass

show_object(object)

cq.exporters.export(object, "viko.stl")
