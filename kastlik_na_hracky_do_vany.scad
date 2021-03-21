radius = 10;
height = 195;
x = 240;
y = 200;
angle = 5;
$fn=64;

module box() {
    translate([radius, radius, radius]) corner();
    translate([x - radius, radius, radius]) corner();
    translate([radius, y - radius, radius]) corner();
    translate([x - radius, y - radius, radius]) corner();

    translate([radius, radius, radius]) rotate([- 90, 0, 0]) cylinder(r = radius, h = y - 2 * radius);
    translate([radius, radius, radius]) rotate([0, 90, 0]) cylinder(r = radius, h = x - 2 * radius);
    translate([x - radius, radius, radius]) rotate([- 90, 0, 0]) cylinder(r = radius, h = y - 2 * radius);
    translate([radius, y - radius, radius]) rotate([0, 90, 0]) cylinder(r = radius, h = x - 2 * radius);

    translate([radius, radius, 0]) cube([x - 2 * radius, y - 2 * radius, height]);
    translate([0, radius, radius]) cube([x, y - 2 * radius, height - radius]);
    translate([radius, 0, radius]) cube([x - 2 * radius, y, height - radius]);
}

module corner() {
    cylinder(r = radius, h = height - radius);
    sphere(r = radius);
}

module inner() {
    intersection() {
        translate([3, 3, 3]) resize(([x - 6, y - 6, height]))  box();
        union() {
            inner1();}
    }

}

module inner1() {
    translate([radius + 3, radius + 3, radius + 3]) rotate([angle, - angle, 0]) union() {
        yd = sin(angle) * y;
        xd = sin(angle) * x;
        x = xd + x + 6;
        y = yd + y + 6;
        corner();
        translate([x - 2 * radius - 6, 0, 0]) corner();
        translate([0, y - 2 * radius - 6, 0]) corner();
        translate([x - 2 * radius - 6, y - 2 * radius - 6, 0]) corner();

        translate([- radius, 0, 0,]) cube([x - 2 * radius - 6, y, height]);
        translate([0, - radius, 0,]) cube([x, y - 2 * radius - 6, height]);
        translate([0, 0, - radius,]) cube([x - 2 * radius - 6, y - 2 * radius - 6, height]);

        rotate([- 90, 0, 0]) cylinder(r = radius, h = y - 2 * radius);
        rotate([0, 90, 0]) cylinder(r = radius, h = x - 2 * radius - 6);
        translate([x - 2 * radius - 3, 0, 0]) rotate([- 90, 0, 0]) cylinder(r = radius, h = y - 2 * radius - 6);
        translate([0, y - 2 * radius - 3, 0]) rotate([0, 90, 0]) cylinder(r = radius, h = x - 2 * radius - 6);

    }
}

module main() {
    difference() {
        box();
        inner();
        translate([radius, radius, radius]) rotate([0, 45, 45]) cylinder(r = radius, h = 100, center = true);
    }
}

main();
