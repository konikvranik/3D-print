import cadquery as cq

diameter = 50
depth = 50
thick = 5
cut = 0.2

if 'show_object' not in globals():
    def show_object(*args, **kwargs):
        pass

for p in ["rl", "fl", "rr", "fr"]:
    wp = cq.Workplane("XY")
    wp = wp.cylinder(depth, diameter / 2)

    wp = wp.faces(">Z").workplane(offset=15).circle(diameter / 2)
    wp = wp.workplane(offset=-15)
    wp = wp.circle(diameter / 2 + 5)
    wp = wp.loft()

    wp = wp.faces(">Z").workplane(invert=True)
    wp = wp.circle(diameter / 2 - 3).cutBlind(depth * 2)

    wp = wp.faces(">Z").workplane(invert=True)
    wp = wp.rect(diameter * 2, thick).cutBlind(depth * 2)

    wp = wp.faces(">Z").workplane(invert=True)
    wp = wp.rect(10, diameter * 2).cutBlind(depth * 2)

    wp = wp.faces("<Z").workplane(invert=True)
    wp = wp.cylinder(10, diameter / 2 + 10)

    t = cq.Workplane("XY").workplane(offset=-depth / 2 - thick - 1).workplane(offset=1)
    t = t.text('↥', fontsize=60, distance=cut)

    if p == "rl":
        t = t.workplane().move(10, -17).cylinder(cut, 4)
    elif p == "rr":
        t = t.workplane().move(-10, -17).cylinder(cut, 4)
    elif p == "fr":
        t = t.workplane().move(-10, 6).cylinder(cut, 4)
    elif p == "fl":
        t = t.workplane().move(10, 6).cylinder(cut, 4)

    wp = wp.cut(t)

    cq.exporters.export(wp, "wheel_label_%s.stl" % p)

show_object(wp)
