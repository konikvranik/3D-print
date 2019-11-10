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
ir_connector = {"x": 2.5, "y": 8, "z": 8.5, "bottom_x": 2.5, "bottom_y": 6.3}
wall = 1
inner_offset = 1

###########################################################


workplane = cq.Workplane("XY")
pcb_solid = workplane \
    .box(pcb["x"], pcb["y"], esp["z_offset"] + esp["z"] + pcb["z"], centered=NO_CENTER)
pcb_hole = workplane.workplane(invert=True) \
    .move(pcb["border"], pcb["border"] - pcb["y"]) \
    .box(pcb["x"] - 2 * pcb["border"], pcb["y"] - 2 * pcb["border"], pcb["hole"], centered=NO_CENTER)

workplane = workplane.workplane(offset=pcb["z"])
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

connector_solid = workplane \
    .workplane(offset=-1) \
    .move(connector["x_offset"], 0) \
    .box(connector["x"], connector["y"], connector["z"] + 1, centered=NO_CENTER).edges("|X").fillet(.3)

bbox = hole.findSolid().BoundingBox()
xdim = bbox.xlen
ydim = bbox.ylen
zdim = bbox.zlen

box = cq.Workplane("XY") \
    .workplane(offset=- pcb["hole"]) \
    .moveTo(bbox.xmin - wall, bbox.ymin - wall) \
    .box(xdim + 2 * wall, ydim + 2 * wall, zdim, centered=NO_CENTER)

result = box.cut(hole)

ir_connector_solid = chamber.faces("<X").vertices(">Z and <Y").workplane(offset=-ir_connector["z"] - 3) \
    .box(ir_connector["x"] + wall, ir_connector["y"] + wall, ir_connector["z"], centered=NO_CENTER, combine=False) \
    .faces("|Z") \
    .shell(wall)

result = result.union(ir_connector_solid)

ir_connector_solid = ir_connector_solid.union(ir_connector_solid
                                              .faces("<Z")
                                              .workplane(offset=-.5)
                                              .box(ir_connector["x"] + wall, ir_connector["y"] + wall, 5,
                                                   centered=(True, True, False), combine=False)
                                              .faces("|Z").shell(-wall))
result = result.union(ir_connector_solid).cut(
    ir_connector_solid
        .faces("<Z")
        .workplane(invert=True, offset=1)
        .box(ir_connector["x"] + wall, ir_connector["y"] - wall, ir_connector["z"] + 5, centered=(False, True, False),
             combine=False))

x__workplane = result.faces("<X") \
    .rotate((0, 0, 0), (0, 1, 0), 90) \
    .workplane(centerOption="CenterOfBoundBox") \
    .move(-60, 0)

result.faces("<X").workplane().move(-4, 6).hole(5, 3)
result = result.cut(cq.Workplane("YZ", (bbox.xmin, bbox.ymin, bbox.zmax))
                    .move(15.12, -4)
                    .box(5, 5, 5, centered=(True, False, True)))

result = result.cut(cq.Workplane("YZ", (bbox.xmin, bbox.ymin, bbox.zmax))
                    .move(wall + .5, -1)
                    .box(ir_connector["y"], 5, 5, centered=(False, False, True)))

result.faces("<X or >X or <Y or > Y").fillet(.5)

show_object(result.cut(connector_solid))

##############################################################

bb = result.findSolid().BoundingBox()

koule = x__workplane.sphere(30, combine=False)
dira = x__workplane.move(3).box(bb.xlen, bb.ylen, bb.zlen, combine=False).faces(">X").box(10, bb.ylen + .7,
                                                                                          bb.zlen + .7,
                                                                                          centered=(False, True, True))

dish = x__workplane.move(-39, 0).sphere(25)

koule = koule.cut(dish)
koule = koule.cut(dira)
wp = koule.workplane()
#for i in range(10, 60, 10):
wp.hole(3)
for j in range(0, 360, 45):
    wp.workplane().transformed(rotate=(10, 0, j)).hole(3)
    wp.workplane().transformed(rotate=(20, 0, j+22.5)).hole(4)
    wp.workplane().transformed(rotate=(30, 0, j )).hole(6)
    wp.workplane().transformed(rotate=(40, 0, j+22.5)).hole(8)
    wp.workplane().transformed(rotate=(50, 0, j )).hole(10)

show_object(koule)
