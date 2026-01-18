from cadquery import cq

from common import render

outer_width = 152
inner_width = 133
outer_depth = 170
inner_depth = 151
socket_width = 15
socket_height = 7
step_height = 11
socket_offset = 33
outer_radius = 20


def build_case():
    wp = cq.Workplane("XY")
    return wp.cylinder(outer_width, outer_depth / 4)


def main():
    """Main workflow."""
    render(build_case())


if __name__ == "__main__":
    main()
