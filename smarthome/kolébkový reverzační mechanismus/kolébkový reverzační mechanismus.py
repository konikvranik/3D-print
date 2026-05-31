import cadquery as cq
import math

# --- PARAMETRY ---
modul = 1.5
vule = 0.2  # Vůle pro volný rotační pohyb dílů (0.2mm je ideální pro 3D tisk)

zuby_slunce = 12
zuby_satelit = 10

d_slunce = modul * zuby_slunce
d_satelit = modul * zuby_satelit

tloustka_kol = 8.0
hridel_motoru = 8.0 / 2
osova_vzdalenost_ramene = (d_slunce + d_satelit) / 2

uhel_v = 40.0
uhel_rad = math.radians(uhel_v)

# Výpočet pozic konců ramen
x_l = osova_vzdalenost_ramene * math.sin(-uhel_rad)
y_l = osova_vzdalenost_ramene * math.cos(-uhel_rad)
x_p = osova_vzdalenost_ramene * math.sin(uhel_rad)
y_p = osova_vzdalenost_ramene * math.cos(uhel_rad)

# --- FUNKCE PRO OZUBENÉ KOLO ---
def vytvor_ozubene_kolo(zuby, modul, tloustka, prumer_diry):
    r_roztecna = (modul * zuby) / 2
    r_hlavova = r_roztecna + modul
    r_patova = r_roztecna - 1.25 * modul
    r_valce = r_patova + 0.1

    kolo = cq.Workplane("XY").cylinder(tloustka, r_valce)

    uhel_zubu = 360.0 / zuby
    sirka_hlavy = modul * 0.5
    sirka_paty = modul * 1.25

    for i in range(zuby):
        uhel_deg = i * uhel_zubu
        uhel_rad = math.radians(uhel_deg)

        dir_x = math.sin(uhel_rad)
        dir_y = math.cos(uhel_rad)
        tan_x = math.cos(uhel_rad)
        tan_y = -math.sin(uhel_rad)

        p1 = ((r_patova - 0.2) * dir_x - (sirka_paty/2) * tan_x, (r_patova - 0.2) * dir_y - (sirka_paty/2) * tan_y)
        p2 = (r_hlavova * dir_x - (sirka_hlavy/2) * tan_x, r_hlavova * dir_y - (sirka_hlavy/2) * tan_y)
        p3 = (r_hlavova * dir_x + (sirka_hlavy/2) * tan_x, r_hlavova * dir_y + (sirka_hlavy/2) * tan_y)
        p4 = ((r_patova - 0.2) * dir_x + (sirka_paty/2) * tan_x, (r_patova - 0.2) * dir_y + (sirka_paty/2) * tan_y)

        zub = (
            cq.Workplane("XY")
            .workplane(offset=-tloustka/2)
            .moveTo(p1[0], p1[1])
            .lineTo(p2[0], p2[1])
            .lineTo(p3[0], p3[1])
            .lineTo(p4[0], p4[1])
            .close()
            .extrude(tloustka)
        )
        kolo = kolo.union(zub)

    if prumer_diry > 0:
        kolo = kolo.faces(">Z").workplane().hole(prumer_diry * 2)

    return kolo

# --- 1. CENTRÁLNÍ KOLO (SLUNCE) ---
slunce = vytvor_ozubene_kolo(zuby_slunce, modul, tloustka_kol, hridel_motoru)
slunce = slunce.faces(">Z").workplane().rect(8.0, 0.5).extrude(-tloustka_kol, combine="cut")

# --- 2. SATELITNÍ KOLO ---
satelit = vytvor_ozubene_kolo(zuby_satelit, modul, tloustka_kol, (5.0 + vule) / 2)

# --- 3. VÝKYVNÉ RAMENO S ČEPY A DRÁŽKAMI ---
# Základní deska ramene
rameno_deska = (
    cq.Workplane("XY")
    .cylinder(4.0, hridel_motoru + 4.0)
    .faces(">Z").workplane()
    .line(x_l, y_l).circle(6.0).extrude(-4.0)
    .faces(">Z").workplane()
    .line(x_p, y_p).circle(6.0).extrude(-4.0)
    .faces(">Z").workplane().hole((hridel_motoru * 2) + vule)
)

# Tvorba čepů (os)
cepy = (
    cq.Workplane("XY")
    .workplane(offset=2.0)
    .moveTo(x_l, y_l).circle(2.5).extrude(11.0)
    .moveTo(x_p, y_p).circle(2.5).extrude(11.0)
)

# Sloučení základny a čepů do jednoho solidu
rameno_komplet = rameno_deska.union(cepy)

# Tělesa pro vyříznutí drážek (odčítaný solid)
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

# Finální vyříznutí drážek z ramene
rameno = rameno_komplet.cut(drazka_leva).cut(drazka_prava)

# --- 4. POJISTNÝ C-KLIP (SÉGROVKA) ---
klip = (
    cq.Workplane("XY")
    .cylinder(1.0, 5.0)
    .faces(">Z").workplane().hole(3.6)
    .faces(">Z").workplane().rect(10.0, 3.2).extrude(-1.0, combine="cut")
)

# --- SESTAVENÍ DO ASSEMBLY ---
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

sestava.save("kolebkovy_mechanismus_sestava.step", "STEP")
print("Hierarchická sestava exportována bez chyb.")
