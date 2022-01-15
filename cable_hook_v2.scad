diameter = 4.5;
width = 30;
thickness = 2;
height = 12;
hole = 4;
space = 3;
$fa = 1;
$fs = .2;


module holes() {
	translate([- width / 2 + space + hole / 2, height / 2 - space - hole / 2, 0]) cylinder(d = hole, h = thickness * 2, center = true);
	translate([width / 2 - space - hole / 2, height / 2 - space - hole / 2, 0]) cylinder(d = hole, h = thickness * 2, center = true);

}

module stand() {
	translate([0, height / 2, thickness / 2]) difference() {
		union() {
			translate([0, thickness - height / 2, 0]) rotate([45, 0, 0]) cube([width, diameter, diameter], center = true);
			translate([0, - thickness / 2, 0]) cube([width, height, thickness], center = true);
		}
		holes();
	}
}

module holder() {
	translate([- width / 2, 0, 0]) {
		translate([0, - diameter / 2, diameter/2 + thickness ]) rotate([0, 90, 0])
			difference() {
				cylinder(d = diameter + 2 * thickness, h = width);
				translate([0, 0, - .5]) {
					cylinder(d = diameter, h = width + 1);
					translate([- .1 * diameter, - 2 * diameter, 0]) cube([2 * diameter, 2.1 * diameter, width + 1]);
				}
			}
	}
}

difference() {
	union() {
		holder();
		stand();
	}
	translate([0, 0, - 3 / 2 * thickness]) cube([width + 2 * (hole + 2 * space), height, 3 * thickness], center = true);
}