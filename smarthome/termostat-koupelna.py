import cadquery as cq
from ezdxf.zoom import center

width = 80
between_holes = 60
thickness = 3

wp = cq.Workplane("XY")
object = wp.box(width, width, thickness).edges("|Z").fillet(3).edges(">Z").fillet(2).faces(">Z").moveTo(
    -between_holes / 2, 0).circle(3 / 2).cutThruAll().moveTo(-between_holes / 2, 0).circle(5 / 2).cutBlind(10).moveTo(
    between_holes / 2, 0).circle(3 / 2).cutThruAll().moveTo(between_holes / 2, 0).circle(5 / 2).cutBlind(10).faces("<Z").moveTo(0,-width/2).rect(10,width).cutBlind(-10)

if 'show_object' not in globals():
    def show_object(*args, **kwargs):
        pass

show_object(object)

cq.exporters.export(object, "termostat-koupelna.stl")
