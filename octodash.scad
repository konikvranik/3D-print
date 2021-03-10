display = [85.5, 55.5, 7]+[1,1,1];
lcd = [74.5, 50.5, 5];
rpi = [65.2, 56.2, 20]+[1,1,1];
thick = 1.5;
border=7;
drill = 4;
$fn=32;

difference() {
    union() {
        cube([display[0], display[1] + 45, display[2] + rpi[2]] + [2 * thick, 2 * thick, 2 * thick]);
        translate([- 15, display[1] + 45, - 15]) cube([display[0] + 30 + 2 * thick, 2 * thick, display[2] + rpi[2] + 15
            + 2 * thick]);
    }
    translate([thick, thick, 1]) cube(display + [0, 20 + 45, 0]);
    translate([thick, thick, 1 + display[2]]) cube(rpi + [0, 20 + 45, 0]);
    translate([40, 10, 1 + display[2]]) cube([50, 30, rpi[2]]);
    translate([(display[0] - lcd[0]) - thick, thick + (display[1] - lcd[1]) / 2, - 1]) cube(lcd);
    translate([thick, display[1] + 45 -5, display[2] + rpi[2]]) cube([rpi[0], 50, 10]);

    translate([- border, - 1, - border]) rotate([- 90, 0, 0]) cylinder(d = drill, h = 200);
        translate([- border, - 1, display[2] + rpi[2] + 2 * thick - border]) rotate([- 90, 0, 0]) cylinder(d = drill, h = 200);
    translate([display[0] + 30 + 2 * thick - border - 15, - 1, - border]) rotate([- 90, 0, 0]) cylinder(d = drill, h = 200);
    translate([display[0] + 30 + 2 * thick - border - 15, - 1, display[2] + rpi[2] + 2 * thick - border]) rotate([- 90, 0, 0])
        cylinder(d = drill, h = 200);
    translate([(display[0] + 30 + 2 * thick) / 2 - 15, - 1, - border]) rotate([- 90, 0, 0]) cylinder(d = drill, h = 200);
}

