import math
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import render, cq

# Rozměry v mm
LENGTH = 60.0  # Délka vajíčka (osa X) v mm
WIDTH = 55.0  # Šířka vajíčka (osa Y) v mm
HEIGHT = 50.0  # Výška vytažení (5 cm = 50 mm)
ASYMMETRY = 0.15  # Tvarový koeficient vajíčka (0 = elipsa, >0 = vajíčko s užším a širším koncem)
NUM_POINTS = 120  # Počet vzorkovacích bodů pro hladkou křivku


def create_egg_points(length: float, width: float, asymmetry: float, num_points: int = 120) -> list[tuple[float, float]]:
    """Vypočítá body pro uzavřený půdorys tvaru vajíčka o přesných rozměrech length x width."""
    a = length / 2.0
    k = asymmetry

    if abs(k) < 1e-6:
        y_norm_max = 1.0
    else:
        # Analytické maximum funkce sin(t) * (1 - k * cos(t))
        cos_t_max = (1.0 - math.sqrt(1.0 + 8.0 * k * k)) / (4.0 * k)
        sin_t_max = math.sqrt(max(0.0, 1.0 - cos_t_max * cos_t_max))
        y_norm_max = sin_t_max * (1.0 - k * cos_t_max)

    b = (width / 2.0) / y_norm_max

    points = []
    for i in range(num_points):
        t = 2.0 * math.pi * i / num_points
        x = a * math.cos(t)
        y = b * math.sin(t) * (1.0 - k * math.cos(t))
        points.append((x, y))

    return points


def build_egg(
    length: float = LENGTH,
    width: float = WIDTH,
    height: float = HEIGHT,
    asymmetry: float = ASYMMETRY,
    num_points: int = NUM_POINTS,
) -> cq.Workplane:
    """Vytvoří 3D model s půdorysem vajíčka vytažený do výšky height."""
    pts = create_egg_points(length, width, asymmetry, num_points)
    body = cq.Workplane("XY").spline(pts, periodic=True, makeWire=True).extrude(height)
    return body


def main():
    model = build_egg()
    render(model, "vajicko.stl")


if __name__ == "__main__":
    main()
