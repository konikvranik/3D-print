difference() {
    cylinder(h = 8.2, d = 35);
    translate([0, 0, 3+10/2]) {
        cube([22, 40, 10], center=true);
    }
}