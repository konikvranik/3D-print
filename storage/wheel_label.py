import os
import sys

import cadquery as cq
from ocp_vscode import set_port

set_port(3939)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import render

diameter = 52
depth = 10
cut_thick = 5
thick = 2
cut = 0.2
offset = 15
torus_radius = .5
cutout_radius = diameter / 2 + thick * 4


def main():
    for p in ["rl", "fl", "rr", "fr"]:
        # Cylinder
        wp = cq.Workplane("XY").cylinder(thick, diameter / 2 + 5, centered=(True, True, False))
        wp = wp.faces(">Z").workplane(invert=False)
        wp = wp.cylinder(depth + torus_radius, diameter / 2, centered=(True, True, False))

        # Get the height of the top face to place the torus correctly
        z_pos = thick + depth + torus_radius

        # Create the torus and add it to the cylinder
        torus = (
            cq.Workplane("XZ")
            .moveTo(diameter / 2 - torus_radius, z_pos)  # Move to the ring's major radius
            .circle(torus_radius + torus_radius)  # The circle is now "standing up"
            .revolve(360, (0, 0, 0), (0, 1, 0))  # Revolve around global Z axis
        )
        wp = wp.union(torus)

        # Instead of finding the face on the torus (which is hard),
        # create a helper workplane at the same height as before.
        wp = cq.Workplane("XY").workplane(offset=z_pos).add(wp)

        # Create all cuts at once using a sketch or polar array if possible, 
        # but here we can just create one and use it in a loop
        cut_template = (
            cq.Workplane("XY", origin=(0, 0, z_pos + torus_radius*2))
            .rect(diameter * 2, cut_thick)
            .extrude(-(depth + torus_radius * 3), combine=False)
        )
        for i in range(16):
            wp = wp.cut(cut_template.rotate((0, 0, 0), (0, 0, 1), 360 / 16 * i))

        wp = wp.cut(cq.Workplane("XY").workplane(offset=thick + cutout_radius).sphere(cutout_radius))

        t = cq.Workplane("XY")
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

        render(wp, "wheel_label_%s.stl" % p)


if __name__ == "__main__":
    main()
