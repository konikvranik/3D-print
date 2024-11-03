import cadquery as cq
from ezdxf.zoom import center

width = 80
from_corner = 5
thickness = 3

wp = cq.Workplane("XY")
object = wp.box(width, width, thickness).edges("|Z").fillet(3).edges(">Z").fillet(2).faces(">Z").moveTo(
    width / 2 - from_corner, 0).circle(3 / 2).cutThruAll().moveTo(width / 2 - from_corner, 0).circle(
    5 / 2).cutBlind(10).faces("<Z").moveTo( width/2,-width/4).rect(width, 10).cutBlind(-10)

if 'show_object' not in globals():
    def show_object(*args, **kwargs):
        pass

show_object(object)

cq.exporters.export(object, "termostat-zachod.stl")
