import cadquery as cq
from cadquery import Workplane, Assembly


def render(object , fname, tolerance=0.0001, angularTolerance=0.1):
    # Check if show_object is available (for CQ-editor)
    if 'show_object' not in globals():
        def show_object(*args, **kwargs):
            pass

    show_object(object)


    # Export the model to STL
    if isinstance(object, Assembly):
        object.export(fname, tolerance=tolerance, angularTolerance=angularTolerance)
    else:
        cq.exporters.export(object, fname, None, tolerance, angularTolerance)


def calculate_pla_bore_diameter(screw_diameter: float) -> float:
    """
    Calculates the recommended pilot hole diameter for 3D printed PLA parts.

    The calculation accounts for material stiffness and 3D printing
    inner hole shrinkage. For PLA, a hole diameter of roughly 80-85%
    of the screw diameter is ideal for standard wood/plastic screws.

    Args:
        screw_diameter (float): The nominal outer diameter of the screw in mm.

    Returns:
        float: The calculated drill/bore diameter for the 3D model.
    """
    if screw_diameter < 2.0:
        # Very small screws need more clearance to prevent snapping
        ratio = 0.85
    elif screw_diameter <= 4.0:
        # Standard range (3mm - 4mm)
        ratio = 0.82
    else:
        # Larger screws
        ratio = 0.80

    # Standard formula: (Diameter * ratio) + 3D printing compensation
    # Most hobbyist printers shrink internal holes by ~0.1mm to 0.2mm
    printing_compensation = 0.1

    calculated_hole = (screw_diameter * ratio) + printing_compensation

    return round(calculated_hole, 2)
