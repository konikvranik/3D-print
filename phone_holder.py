import cadquery as cq
import numpy as np

charging_base = np.array([75, 75, 12])
phone = np.array([72, 153, 8.6]) + np.array([1, 0, 1])
wall = np.array([5, 5, 3])
grab_side = 2
grab_bottom = 2
grab_height = 40
tunnel_width = 20
tunnle_height = 10
total_height = phone.item(1) + grab_height + 15
outer_box = phone + np.array([0, 0, charging_base.item(2)]) + wall * 2
top_height = outer_box.item(2) - phone.item(2) - wall.item(2)
top_width = outer_box.item(0) / 2
top_half_size = charging_base.item(1) / 2 + wall.item(1)
current_length = outer_box.item(1) / 2 + top_half_size
top_length = total_height - outer_box.item(1) + (outer_box.item(1) - charging_base.item(1) - wall.item(1)) / 2
top_hole = 15
top_thickness = 8
top_depth = outer_box[2]
screw_places = 20
screw_diameter = 4
screw_head_diameter = 8

wp = cq.Workplane("XY")

# outer box
base = wp.box(outer_box.item(0), outer_box.item(1), outer_box.item(2))

# cut walls above grabs
base = base.faces(">Z").rect(outer_box.item(0), grab_height * 2).cutBlind(-phone.item(2) - wall.item(2))
# bottom cut through
base = base.faces(">Z").workplane().rect(phone.item(0) - grab_side * 2, phone.item(1) - grab_bottom * 2).cutBlind(
    -phone.item(2) - wall.item(2))
# bottom cut grabs
base = base.faces("<Z[1]").workplane().rect(phone.item(0), phone.item(1)).cutBlind(phone.item(2))
base = base.edges(">>Y[5] or +X ").fillet(1.24)
base = base.faces(">X or <X").edges("+Y").fillet(1.24)

# charging base
base = base.faces(">Z[1]").rect(charging_base.item(0), charging_base.item(1)).cutBlind(-charging_base.item(2))

# cut of top body top
base = base.faces(">Z").workplane().move(0, outer_box.item(1) / 2).rect(outer_box.item(0), outer_box.item(1)).cutBlind(
    -phone.item(2) - wall.item(2))
# cut of top body
base = base.faces(">Z").workplane().move(outer_box.item(0), top_half_size + 50).rect(outer_box.item(0) * 4,
                                                                                     100).cutThruAll()

base = base.faces(">Y").workplane().tag("top_of_base")

# top handle
base = base.move(0, -outer_box.item(2) + top_height / 2).rect(top_width, top_height).extrude(top_length)
base = base.workplaneFromTagged("top_of_base").move(0, -outer_box.item(2) + top_height / 2).rect(outer_box.item(0),
                                                                                                 top_height).extrude(
    wall.item(1) * 5)

# tunnel
base = base.faces(">Y").rect(tunnel_width, top_height - 2 * wall.item(1)).cutBlind(-top_length - wall.item(1))
# top hole
base = base.faces("<Z").workplane().move(0, -total_height / 2).rect(tunnel_width, top_hole * 2).cutBlind(-5)

# top
base = base.faces(">Y").workplane(offset=top_thickness / 2).move(0, top_depth / 2).box(outer_box.item(0),
                                                                                       top_depth, top_thickness)

hole_size = top_height - wall.item(1)
base = base.faces(">Y").workplane().move(0, hole_size / 2).rect(tunnel_width, hole_size).cutBlind(-top_thickness)
base = base.edges("<<Y[1]").fillet(2).faces("<<Y[2]").edges().fillet(2)

base = base.faces(">Y").workplane().move(outer_box.item(0) / 2 - 10, top_depth / 2).circle(screw_diameter / 2).cutBlind(
    -top_thickness)
base = base.faces(">Y").workplane(offset=-top_thickness).move(outer_box.item(0) / 2 - 10, top_depth / 2).circle(
    screw_head_diameter / 2).cutBlind(
    top_thickness - wall.item(1))
base = base.faces(">Y").workplane().move(-outer_box.item(0) / 2 + 10, top_depth / 2).circle(
    screw_diameter / 2).cutBlind(
    -top_thickness)
base = base.faces(">Y").workplane(offset=-top_thickness).move(-outer_box.item(0) / 2 + 10, top_depth / 2).circle(
    screw_head_diameter / 2).cutBlind(top_thickness - wall.item(1))

cq.exporters.export(base, "phone_holder.stl")
