d1 = 65.25;
d2 = 75.55;

w = 44.11;

d = 4;
t1 = 3;
t2 = 6.5;

$fa = 1;
$fs = .5;

holes = false;
conic = false;
spheric = false;
nut = false;

difference() {
    union() {
        difference() {
            union() {
                cylinder(h = w + 2 * t1, d = d1);
                cylinder(h = t1, d = d2);
                translate([0, 0, w + t1]) cylinder(h = t1, d = d2);
                translate([0, 0, t1 + d]) cylinder(h = 2, d = d1 + 2 * 2.5);
                translate([0, 0, w + t1 - 2 - d]) cylinder(h = 2, d = d1 + 2 * 2.5);
            }
            translate([0, 0, - 1]) cylinder(d = d1 - 2 * t1, h = (w + 2 * t1 - t2) / 2 + 1);
            translate([0, 0, (w + 2 * t1 + t2) / 2]) if (conic) {
                cylinder(d = d1 - 2 * t1, d1 = 20, h = (w + 2 * t1 - t2) / 2 + 1);
            } else if (spheric) {
                radius = (d1 - 2 * t1) / 2 + 7;
                translate([0, 0, radius]) sphere(r = radius);
            } else {
                cylinder(d = d1 - 2 * t1, h = (w + 2 * t1 - t2) / 2 + 1);
            }
            if (holes) {
                for (i = [0 : 5]) {
                    rotate(i * 60, [0, 0, 1])
                        translate([0, 21, 0])
                            cylinder(d = 17, h = w + 10);
                }
            }
        }
        if (!nut) {
            translate([0, 0, (w + 2 * t1 - t2)/2 - 1]) cylinder(d = 7.5, h = 2);
        }
    }
    if (nut) {
        cylinder(h = (w + 2 * t1 - t2) / 2 + 3, d = 13.8, $fn = 6);
    } else {
        cube([11.4, 2, (w + 2 * t1 - t2) + 3*2], center = true );
    }
    cylinder(h = w, d = 4);
}