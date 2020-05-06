hole = [180, 23, 40];


module base() {
	difference() {
		translate([- 2, - 2, - 2]) cube([hole[0] + hole[1] + 1 + 2 * 2, hole[0] + hole[1] + 1 + 2 * 2, hole[2] + 2 + 1 +
		1.8]);
		translate([- 1, - 1, hole[2]]) cube([hole[0] + hole[1] + 3, hole[0] + hole[1] + 3 + 10, 2]);
		translate([.5, .5, hole[2] + 1.8]) cube([hole[0] + hole[1], hole[0] + hole[1] + 10, hole[2]]);
		cube(hole + [0, 0, 1]);
		translate([hole[0] + hole[1] + 1, 0, 0]) rotate([0, 0, 90]) cube(hole + [0, 0, 1]);
		translate([hole[0] + hole[1] + 1, hole[0] + hole[1] + 1, 0]) rotate([0, 0, 180]) cube(hole + [0, 0, 1]);
		translate([0, hole[0] + hole[1] + 1, 0]) rotate([0, 0, 270]) cube(hole + [0, 0, 1]);

		translate([hole[1] + 1, hole[1] + 1, 0]) cube([hole[0] - hole[1] - 1, hole[0] - hole[1] - 1, hole[2] + 1]);
	}
}

module viko() {
	cube([hole[0] + hole[1] + 1 + 1 + 1, hole[0] + hole[1] + 1 + 3, 1.6]);
	translate([1, 0, 0]) difference() {
		cube([hole[0] + hole[1], hole[0] + hole[1] + 2, 2.8]) ;
		translate([- 1 + (hole[0] + hole[1] + 1) / 2, 2 + (hole[0] + hole[1] + 1) / 2, 2.4]) linear_extrude(h = .8) {
			translate([0, 20]) text(text = "Scrabble", valign = "center", halign = "center", size = 23, font =
			"Comic Sans MS:style=Bold");
			translate([0, - 40]) text(text = "česká verze", valign = "center", halign = "center", size = 10);
		}

	}
}

base();

translate([hole[0] + hole[1] + 10, 0, 0]) viko();