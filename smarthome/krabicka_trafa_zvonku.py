import cadquery as cq
from cadquery.selectors import SubtractSelector

from common import calculate_pla_bore_diameter
from common import render

width = 100
height = 60
depth = 150


def build_tapered_prism():
    """Create a prism that starts as 10x10 and tapers to 10x2 over a height.

    Uses a loft between two centered rectangles.
    """
    wp = cq.Workplane("XY")
    # bottom rectangle at Z=0 and top rectangle at Z=TAPER_HEIGHT
    solid = (
        wp.rect(width, depth)
        .workplane(offset=height)
        .polyline([(-50, 75), (50, 75), (25, -50), (-25, -50)])
        .close()
        .loft()
    )

    # Apply fillet only to edges that are not on the base
    # Use negative selector to exclude edges from bottom face (<Z)
    solid = solid.edges("~<Z").fillet(24)

    return solid


def main():
    """Main workflow."""
    # render the tapered prism (10x10 -> 10x2)
    tapered = build_tapered_prism()
    render(tapered, "tapered_prism.stl")


if __name__ == "__main__":
    main()
