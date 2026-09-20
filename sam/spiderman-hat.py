import math
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import render, cq

# Rozměry spodního půdorysu (v mm)
BASE_LENGTH = 60.0  # Délka vajíčka (osa X) v mm
BASE_WIDTH = 55.0  # Šířka vajíčka (osa Y) v mm
ASYMMETRY = 0.15  # Tvarový koeficient vajíčka (0 = elipsa, >0 = vajíčko)
NUM_POINTS = 120  # Počet vzorkovacích bodů pro hladkou křivku

# Výšky a rozměry šikmé římsy (v mm)
# Celková výška modelu: BODY_HEIGHT + BRIM_HEIGHT = 50.0 mm (5 cm)
BODY_HEIGHT = 40.0  # Výška svislé části těla klobouku v mm
BRIM_OFFSET = 10.0  # Přesah šikmé římsy ven (1 cm = 10 mm)
BRIM_HEIGHT = 10.0  # Výška šikmé římsy v mm (sklon 45° ideální pro Spiral Vase tisk)


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


def build_spiderman_hat(
    base_length: float = BASE_LENGTH,
    base_width: float = BASE_WIDTH,
    body_height: float = BODY_HEIGHT,
    brim_offset: float = BRIM_OFFSET,
    brim_height: float = BRIM_HEIGHT,
    asymmetry: float = ASYMMETRY,
    num_points: int = NUM_POINTS,
) -> cq.Workplane:
    """Vytvoří model optimalizovaný pro tisk v režimu Spiral Vase:

    - Spodek (Z=0): rovný základní půdorys vajíčka (60 × 55 mm) sedící přímo na podložce.
    - Tělo (Z=0 až Z=body_height): svislé stěny.
    - Šikmá římsa (Z=body_height až Z=body_height+brim_height): plynule se rozevírá ven o brim_offset (1 cm) pod úhlem 45°.
    """
    pts = create_egg_points(base_length, base_width, asymmetry, num_points)

    # 1. Spodní profil na podložce (Z = 0)
    w0 = cq.Workplane("XY").spline(pts, periodic=True, makeWire=True).val()

    # 2. Profil na konci svislého těla (Z = body_height)
    w1 = cq.Workplane("XY").workplane(offset=body_height).spline(pts, periodic=True, makeWire=True).val()

    # 3. Horní rozevřený profil šikmé římsy (Z = body_height + brim_height)
    w2 = (
        cq.Workplane("XY")
        .workplane(offset=body_height + brim_height)
        .spline(pts, periodic=True, makeWire=True)
        .offset2D(brim_offset)
        .val()
    )

    # Ruled loft mezi profily: od spodu po body_height svisle, od body_height nahoru šikmo 45°
    hat = (
        cq.Workplane("XY")
        .newObject([w0])
        .toPending()
        .newObject([w1])
        .toPending()
        .newObject([w2])
        .toPending()
        .loft(ruled=True)
    )

    return hat


def main():
    model = build_spiderman_hat()
    render(model, "spiderman-hat.stl")


if __name__ == "__main__":
    main()
