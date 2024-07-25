import cadquery as cq

if 'show_object' not in globals():
    def show_object(*args, **kwargs):
        pass

wp = cq.Workplane("XY")
wp = wp.cylinder(9.2, 35 / 2)
wp = wp.faces("<Z").workplane(invert=True).rect(22, 40).cutBlind(4.6)

wp = wp.faces(">Z").workplane(invert=True).moveTo(11, 5).rect(2, 2).cutBlind(7)
wp = wp.faces(">Z").workplane(invert=True).moveTo(-14, 5).rect(5, 2).cutBlind(7)
wp = wp.faces(">Z").workplane(invert=False).cylinder(2.2, 13.3 / 2, centered=[True, True, False])
wp = wp.faces(">Z").workplane(invert=False).cylinder(2.2, 11.5 / 2, centered=[True, True, False])
wp = wp.faces(">Z").workplane(invert=False).cylinder(3.6, 13.3 / 2, centered=[True, True, False])
wp = wp.faces(">Z").workplane(invert=True).polygon(6, 9.3).cutBlind(8.2)
wp = wp.cut(cq.Workplane("YZ").move(-9, -2).cylinder(22, 3))

show_object(wp)

cq.exporters.export(wp, "kolecko_k_aku_batercy.stl")
