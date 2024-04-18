$fa=1;
$fs=.2;

module noha(a = 0) {
    rotate([0, 40, a]) union() {
        translate([0, 0, 0]) cylinder(h = 100, d = 10, center = false);
        translate([0, 0, 100]) sphere(d = 11);
    }
}

difference() {
    union() {
        noha(a = 0);
        noha(a = 120);

        noha(a = 240);

        translate([0, 0, 0]) cylinder(h = 20, d1 = 60, d2 = 30, center = false);
    }

    cylinder(d = 20, h = 80, center = true);
    translate([0, 0, -1]) cylinder(d1 = 50, d2 = 20, h = 21, center = false);
}