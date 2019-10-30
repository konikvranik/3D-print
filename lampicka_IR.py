# This is a CadQuery script template
# Add your script code below
import cadquery as cq

# The show function will still work, but is outdated now
# Use the following to render your model with grey RGB and no transparency
# show(my_model, (204, 204, 204, 0.0))

# New method to render script results using the CadQuery Gateway Interface
# Use the following to render your model with grey RGB and no transparency
# show_object(result, options={"rgba":(204, 204, 204, 0.0)})
NO_CENTER = (False, False, False)
pcb = {"x": 25.3, "y": 21.7, "z": 1.5, "border": .5, "hole": 4}
connector = {"x": 14.5, "y": 9, "z": 11, "x_offset": 13}
esp_connector = {"x": 4.9, "y": 10.5, "z": 8.3, "y_offset": 9.5}
esp = {"x": 25, "y": 15, "z": 3.5, "y_offset": (esp_connector["y_offset"] + esp_connector["y"] / 2 - 15 / 2),
       "z_offset": 11}
wall = 1
inner_offset = 1

workplane = cq.Workplane("XY")
pcb_solid = workplane \
    .box(pcb["x"], pcb["y"], esp["z_offset"] + esp["z"] + pcb["z"], centered=NO_CENTER)
pcb_hole = workplane.workplane(invert=True) \
    .move(pcb["border"], pcb["border"] - pcb["y"]) \
    .box(pcb["x"] - 2 * pcb["border"], pcb["y"] - 2 * pcb["border"], pcb["hole"], centered=NO_CENTER)

workplane = workplane.workplane(offset=pcb["z"])
connector_solid = workplane \
    .workplane(offset=-.5) \
    .move(connector["x_offset"], 0) \
    .box(connector["x"], connector["y"], connector["z"]+1, centered=NO_CENTER)

esp_connector_solid = workplane \
    .move(0, esp_connector["y_offset"]) \
    .box(esp_connector["x"], esp_connector["y"], esp_connector["z"], centered=NO_CENTER)

esp_solid = workplane \
    .workplane(offset=esp["z_offset"]).move(0, esp["y_offset"]) \
    .box(esp["x"], esp["y"], esp["z"], centered=NO_CENTER)

chamber = pcb_solid \
    .faces("<Z") \
    .vertices("<XY") \
    .workplane(offset=inner_offset) \
    .move(-15, inner_offset) \
    .box(15, pcb["y"] - 2 * inner_offset, esp["z_offset"] + esp["z"] + pcb["z"] - inner_offset, centered=NO_CENTER)

hole = pcb_solid.union(pcb_hole).union(esp_solid).union(chamber)

bbox = hole.findSolid().BoundingBox()
xdim = bbox.xlen
ydim = bbox.ylen
zdim = bbox.zlen
box = cq.Workplane("XY").workplane(offset=- pcb["hole"]).moveTo(bbox.xmin - wall, bbox.ymin - wall) \
    .box(xdim + 2*wall, ydim + 2 * wall, zdim, centered=NO_CENTER)
result = box.cut(hole)

show_object(result.cut(connector_solid))
