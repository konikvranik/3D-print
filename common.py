import os
import sys

import cadquery as cq
from cadquery import Workplane, Assembly
from ocp_vscode import (
    show,
    show_object,
    reset_show,
    set_port,
    set_defaults,
    get_defaults,
)


def render(object_to_draw, file_name=None, tolerance=0.0001, angularTolerance=0.1):
    # Check if show_object is available (for CQ-editor)
    # if 'show_object' not in globals():
    #     def show_object(*args, **kwargs):
    #         pass

    import __main__

    caller_file = getattr(__main__, "__file__", sys.argv[0])
    script_dir = os.path.dirname(os.path.abspath(caller_file))

    if file_name is None:
        base_name = os.path.splitext(os.path.basename(caller_file))[0]
        file_name = os.path.join(script_dir, f"{base_name}.stl")
    else:
        if not os.path.isabs(file_name) and not os.path.dirname(file_name):
            file_name = os.path.join(script_dir, file_name)

    # Zajistíme existenci adresáře
    dir_name = os.path.dirname(file_name)
    if dir_name and not os.path.exists(dir_name):
        os.makedirs(dir_name)

    print(f"Exporting model to {os.path.abspath(file_name)}...")
    # Export the model to STL
    if isinstance(object_to_draw, Assembly):
        object_to_draw.export(
            file_name, tolerance=tolerance, angularTolerance=angularTolerance
        )
    else:
        cq.exporters.export(
            object_to_draw, file_name, None, tolerance, angularTolerance
        )

    if os.path.exists(file_name):
        print(
            f"Successfully saved to {os.path.abspath(file_name)} ({os.path.getsize(file_name)} bytes)"
        )
    else:
        print(f"FAILED to save to {os.path.abspath(file_name)}")

    try:
        show_object(object_to_draw)
    except Exception as e:
        print(f"Note: Could not show object in viewer: {e}")


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


def build_toothed_cylinder(radius, cylinder_height, num_teeth=60, tooth_depth=2):
    import math

    # Vypočítáme úhel pro jeden zub
    angle_per_tooth = 360 / num_teeth

    # Vytvoříme ozubení jako průběžný polygon po obvodu
    points = []
    for i in range(num_teeth):
        # Úhel pro začátek zubu (údolí)
        angle_start = math.radians(i * angle_per_tooth)
        # Úhel pro vrchol zubu
        angle_peak = math.radians(i * angle_per_tooth + angle_per_tooth / 2)

        # Bod v údolí (na poloměru radius)
        x_start = radius * math.cos(angle_start)
        y_start = radius * math.sin(angle_start)
        points.append((x_start, y_start))

        # Bod na vrcholu (na poloměru radius + tooth_depth)
        x_peak = (radius + tooth_depth) * math.cos(angle_peak)
        y_peak = (radius + tooth_depth) * math.sin(angle_peak)
        points.append((x_peak, y_peak))

    # Vytvoříme profil ozubení jako uzavřený polygon
    result = cq.Workplane("XY").polyline(points).close().extrude(cylinder_height)

    return result
