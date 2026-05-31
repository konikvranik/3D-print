import cadquery as cq
import cq_gears as gear
import math

# --- PARAMETRY ---
modul = 2
vule = 0.2  # Vůle pro volný rotační pohyb (0.2mm pro 3D tisk)
tloustka_kol = 8.0
hridel_motoru = 8.0 / 2  # Poloměr hřídele (4mm)

zuby_slunce = 12
zuby_satelit = 12

# --- 1. GENEROVÁNÍ OZUBENÝCH KOL POMOCÍ CQ_GEARS ---

# Převod cq_gears tvaru na standardní CadQuery Workplane
slunce = cq.Workplane("XY").add(
    gear.SpurGear(module=modul, teeth_number=zuby_slunce, width=tloustka_kol, bore_d=8.0).build())

# Vyříznutí plošky pro D-profil hřídele (hloubka 0.5mm z průměru)
slunce = slunce.faces(">Z").workplane().rect(8.0, 0.5).extrude(-tloustka_kol, combine="cut")

satelit = cq.Workplane("XY").add(
    gear.SpurGear(module=modul, teeth_number=zuby_satelit, width=tloustka_kol, bore_d=5.0 + vule).build())

# --- 2. VÝPOČET GEOMETRIE RAMENE ---
# Matematicky přesný výpočet roztečného poloměru (r = (m * z) / 2)
r_slunce = (modul * zuby_slunce) / 2.0
r_satelit = (modul * zuby_satelit) / 2.0

osova_vzdalenost_ramene = r_slunce + r_satelit

uhel_v = 52.5
uhel_rad = math.radians(uhel_v)

# Pozice středů satelitů
x_l = osova_vzdalenost_ramene * math.sin(-uhel_rad)
y_l = osova_vzdalenost_ramene * math.cos(-uhel_rad)
x_p = osova_vzdalenost_ramene * math.sin(uhel_rad)
y_p = osova_vzdalenost_ramene * math.cos(uhel_rad)

# --- 3. VÝKYVNÉ RAMENO S ČEPY A DRÁŽKAMI PRO SÉGROVKY ---
rameno_deska = (
    cq.Workplane("XY")
    .cylinder(4.0, hridel_motoru + 4.0)
    .faces(">Z").workplane()
    .line(x_l, y_l).circle(6.0).extrude(-4.0)
    .faces(">Z").workplane()
    .line(x_p, y_p).circle(6.0).extrude(-4.0)
    .faces(">Z").workplane().hole((hridel_motoru * 2) + vule)
)

# Tvorba čepů (os pro satelity, průměr 5mm, výška 11mm)
cepy = (
    cq.Workplane("XY")
    .workplane(offset=2.0)
    .moveTo(x_l, y_l).circle(2.5).extrude(11.0)
    .moveTo(x_p, y_p).circle(2.5).extrude(11.0)
)

rameno_komplet = rameno_deska.union(cepy)

# Solidy pro vyříznutí drážek na ségrovky
drazka_leva = (
    cq.Workplane("XY")
    .workplane(offset=2.0 + 8.5)
    .moveTo(x_l, y_l)
    .circle(3.5)
    .extrude(1.2)
)
drazka_prava = (
    cq.Workplane("XY")
    .workplane(offset=2.0 + 8.5)
    .moveTo(x_p, y_p)
    .circle(3.5)
    .extrude(1.2)
)

rameno = rameno_komplet.cut(drazka_leva).cut(drazka_prava)

# --- 4. POJISTNÝ C-KLIP (SÉGROVKA) ---
klip = (
    cq.Workplane("XY")
    .cylinder(1.0, 5.0)
    .faces(">Z").workplane().hole(3.6)
    .faces(">Z").workplane().rect(10.0, 3.2).extrude(-1.0, combine="cut")
)

# --- SESTAVENÍ DO ASSEMBLY A MANUÁLNÍ POLOHOVÁNÍ ---
sestava = cq.Assembly()

sestava.add(slunce, name="stredove_slunce", color=cq.Color("red"))
sestava.add(rameno, name="vykyvne_rameno", color=cq.Color("gray"),
            loc=cq.Location(cq.Vector(0, 0, -tloustka_kol/2 - 2.0)))
sestava.add(satelit, name="satelit_levy", color=cq.Color("green"),
            loc=cq.Location(cq.Vector(x_l, y_l, 0)))
sestava.add(satelit, name="satelit_pravy", color=cq.Color("green"),
            loc=cq.Location(cq.Vector(x_p, y_p, 0)))
sestava.add(klip, name="pojistka_leva", color=cq.Color("blue"),
            loc=cq.Location(cq.Vector(x_l, y_l, tloustka_kol/2 + 1.0)))
sestava.add(klip, name="pojistka_prava", color=cq.Color("blue"),
            loc=cq.Location(cq.Vector(x_p, y_p, tloustka_kol/2 + 1.0)))

# Export do jednoho STEP souboru
sestava.save("kolebkovy_mechanismus_cq_gears.step", "STEP")
print("Sestava úspěšně uložena.")