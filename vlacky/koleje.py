import cadquery as cq

width = 39.5
height = 12.5
circle = 12.7
len = 18
diff = 8
total_len = 40
inner = 18.5
track = 6
depth = 3.5
# Points we will use to create spline and polyline paths to sweep over
pts = [
    (1, 0),
    (100, 40),
    (199, 80),
    (200, 80)
]


# Spline path generated from our list of points (tuples)

def rail():
    box = cq.Workplane("XY").box(total_len, width, height)
    workplane = box.faces("<Z").workplane()
    workplane.move(0, (inner + track) / 2).rect(total_len, track).cutBlind(-depth)
    workplane.move(0, -(inner + track) / 2).rect(total_len, track).cutBlind(-depth)

    begining = workplane.move(-total_len / 2, 0)
    begining.move((len - circle / 2) / 2, 0).rect(len - circle / 2, diff).cutThruAll()
    begining.move(len - circle / 2).circle(circle / 2).cutThruAll()

    begining = workplane.move(total_len / 2, 0)
    begining.move(-(len - circle / 2) / 2, 0).rect(len - circle / 2, diff).cutThruAll()
    begining.move(-len + circle / 2).circle(circle / 2).cutThruAll()
    s = cq.StringSyntaxSelector
    return box.faces(s('>Z') + s('<Z') - s('<X') - s('>X')).fillet(1.3)


def brick():
    u = 1.6 * 2
    return cq.Workplane("XY", (0, 0, 3.5 * u)).transformed(rotate=(180, 0, 0)) \
        .box(8 * u + u, 8 * u + u, 3 * u).faces(
        ">Z").shell(-(u + .5) / 2) \
        .faces("<Z[1]") \
        .circle(4 * u / 2 + .5).circle(3 * u / 2).extrude(-2 * u)


show_object(brick().union(rail()))
