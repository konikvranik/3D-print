import math
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import render, cq

# Rozměry spodního půdorysu (v mm)
BASE_LENGTH = 60.0  # Délka vajíčka (osa X) v mm
BASE_WIDTH = 55.0  # Šířka vajíčka (osa Y) v mm
ASYMMETRY = 0.15  # Tvarový koeficient vajíčka (0 = elipsa, >0 = vajíčko)
NUM_POINTS = 120  # Počet vzorkovacích bodů pro hladký profil vajíčka

# Výšky a rozměry zakulacené římsy (v mm)
# Celková výška modelu: BODY_HEIGHT + FLARE_HEIGHT = 50.0 mm (5 cm)
BODY_HEIGHT = 35.0  # Výška rovné svislé části klobouku v mm
FLARE_OFFSET = 10.0  # Přesah římsy ven (1 cm = 10 mm)
FLARE_HEIGHT = 15.0  # Výška plynulého zakulaceného přechodu římsy v mm
FLARE_STEPS = 8  # Počet mezilehlých řezů pro dokonale hladký přechod
TOP_SLOPE_DEG = 45.0  # Maximální sklon na vrcholu římsy ve stupních (ideální pro Spiral Vase)


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
    flare_offset: float = FLARE_OFFSET,
    flare_height: float = FLARE_HEIGHT,
    flare_steps: int = FLARE_STEPS,
    top_slope_deg: float = TOP_SLOPE_DEG,
    asymmetry: float = ASYMMETRY,
    num_points: int = NUM_POINTS,
) -> cq.Workplane:
    """Vytvoří model optimalizovaný pro tisk v režimu Spiral Vase s plynule zakulacenou horní římsou:

    - Spodek (Z=0): rovný základní půdorys vajíčka (60 × 55 mm) sedící přímo na podložce.
    - Svislé tělo (Z=0 až Z=body_height): svislé stěny.
    - Zakulacená římsa (Z=body_height až Z=body_height+flare_height): plynule (tečně) přechází
      ze svislé stěny do oblouku rozevírajícího se ven o flare_offset (1 cm) pod úhlem top_slope_deg (45°).
    """
    # 1. Spodní profil na podložce (Z = 0)
    base_pts = create_egg_points(base_length, base_width, asymmetry, num_points)
    w0 = cq.Workplane("XY").spline(base_pts, periodic=True, makeWire=True).val()

    # 2. Profil na konci svislého těla (Z = body_height)
    w1 = cq.Workplane("XY").workplane(offset=body_height).spline(base_pts, periodic=True, makeWire=True).val()

    wires = [w0, w1]

    # 3. Plynulá křivka zakulacení:
    # r(u) = flare_offset * (a * u^2 + b * u^3), kde u in [0, 1]
    # - V u=0 je sklon dr/dz = 0 (dokonale svislá tečna navazující na svislé stěny bez hrany)
    # - V u=1 je sklon přesně tan(top_slope_deg) (45° pro spolehlivý tisk ve spiral vase)
    tan_top = math.tan(math.radians(top_slope_deg))
    a = 3.0 - (flare_height / flare_offset) * tan_top
    b = 1.0 - a

    for i in range(1, flare_steps + 1):
        u = i / flare_steps
        dr = flare_offset * (a * u**2 + b * u**3)
        z = body_height + flare_height * u
        cur_pts = create_egg_points(base_length + 2 * dr, base_width + 2 * dr, asymmetry, num_points)
        w = cq.Workplane("XY").workplane(offset=z).spline(cur_pts, periodic=True, makeWire=True).val()
        wires.append(w)

    # Vytvoření plynulého tělesa (smooth loft přes všechny profily)
    loft_wp = cq.Workplane("XY")
    for w in wires:
        loft_wp = loft_wp.newObject([w]).toPending()

    hat = loft_wp.loft()
    return hat


def main():
    model = build_spiderman_hat()
    render(model, "spiderman-hat.stl")


if __name__ == "__main__":
    main()
