import os

import cadquery as cq

os.environ["FONTCONFIG_FILE"] = "/etc/fonts/fonts.conf"
os.environ["FONTCONFIG_PATH"] = "/etc/fonts/"

dist = 24
diameter = 8
width = 60
height = 15
depth = 35

text_offset = 2

wp = cq.Workplane("XY")
object = wp.box(width + 15, height + 15, depth + 10, centered=True)
object = object.edges().fillet(3)
object = object.faces(">Y").moveTo(0, 0).circle(
    diameter / 2).cutThruAll().moveTo(-dist, 0).circle(diameter / 2).cutThruAll().moveTo(dist, 0).circle(
    diameter / 2).cutThruAll()
object = object.faces(">Z").workplane().moveTo(0, 0).rect(width + 10, height + 10).cutBlind(-depth - 8)

for i in range(0, 30, 5):
    for j in range(-10, -35, -5):
        object = object.faces("<Y").workplane().moveTo(i, j).circle(2).cutBlind(-5)

volume = cq.Workplane("XZ").text("- V +", 3, text_offset)
treble = cq.Workplane("XZ").text("- T +", 3, text_offset)
bass = cq.Workplane("XZ").text("- B +", 3, text_offset)

assembly = cq.Assembly()
assembly.add(object, name="body")
assembly.add(volume, name="volume")
assembly.add(treble, name="treble")
assembly.add(bass, name="bass")


def placement(name, x, y, z):
    assembly.constrain("body", cq.Vertex.makeVertex(1, 1, -1), name,
                       cq.Vertex.makeVertex(1 - x, 1 - y, -1 - z), "Point")
    assembly.constrain("body", cq.Vertex.makeVertex(1, -1, 1), name,
                       cq.Vertex.makeVertex(1 - x, -1 - y, 1 - z), "Point")
    assembly.constrain("body", cq.Vertex.makeVertex(-1, 1, 1), name,
                       cq.Vertex.makeVertex(-1 - x, 1 - y, 1 - z), "Point")


placement("volume", -dist, -(height + 15) / 2 + text_offset - .001, -depth / 2)
placement("treble", 0, -(height + 15) / 2 + text_offset - .001, -depth / 2)
placement("bass", dist, -(height + 15) / 2 + text_offset - .001, -depth / 2)

assembly.solve()

if 'show_object' not in globals():
    def show_object(*args, **kwargs):
        pass

show_object(object)

assembly.save("amplifier_case.step")
# cq.exporters.export(object, "amplifier_case.stl")
