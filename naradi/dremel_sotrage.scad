d=10;
x=200;
y=100;
drill_hole=4;
saw_thick=2;
$fa=10;
$fs=.8;

module base(x=200, y=100, h=70, t=20) {
	difference() {
		union() {
			difference() {
				cube([x, y, 15]);
				for (i=[0, x-d/2]) {
					for (j=[0, y-d/2]) {
						translate([i, j, 0]) cube([d/2, d/2, t]);
					}
				}

			}
			for (i=[d/2, x-d/2]) {
				for (j=[d/2, y-d/2]) {
					translate([i, j, 0]) {
						cylinder(d=d, h=h);
						translate([0, 0, h]) cylinder(d=d*3/4-.5, h=t/2-d*3/4/2);
						translate([0, 0, h+t/2-d*3/4/2]) sphere(d=d*3/4-.5);
					}
				}
			}
		}
		for (i=[d/2, x-d/2]) {
			for (j=[d/2, y-d/2]) {
				translate([i, j, 0]) {
					cylinder(d=d*3/4, h=t/2);
				}
			}
		}
	}
}

module peg_array(x_range, y_range, dia, t=20) {
	for (i=x_range) {
		for (j=y_range) {
			translate([i, j, 0]) cylinder(d=dia, h=t);
		}
	}
}

module cyl_hole(d, w=saw_thick) {
	translate([0, 0, d/2]) rotate([0, 90, 0]) cylinder(d=d, h=w);
}

module plate1() {
	h=70;
	difference() {
		union() {
			base(x, y);
			peg_array([d/2, x-d/2], [d+5:10:x/2-d-5], 5, h-15);
		}
		translate([0, 0, 5]) peg_array([145:6:x-d], [d:6:y-d], drill_hole, 20);
		translate([0, 0, 5]) peg_array([109:6:145], [64:6:y-d], drill_hole, 20);
		translate([0, 0, 5]) peg_array([61:6:109], [88:6:y-d], drill_hole, 20);
		translate([48+d/2, 0, 0]) {
			translate([0, 0, 5]) peg_array([27/2+6:28:x/2-d], [27/2+6:28:y-30], 27, 20);
			translate([0, 0, 5]) peg_array([23/2+6:24:50], [74:24:y-23/2-5], 23, 20);
		}
		for (i=[d:12:48])
		translate([i, d/2, 5]) cube([11, 88, 20]);
	}
}

module plate2() {
	h=70;
	saws=[
	[x-d-5, 5, 51],
	[x-d-5, y-5-23, 23],

	[x-d-5-5, 5, 46],
	[x-d-5-5, y-5-27, 27],

	[x-d-5-5-5, 5, 37],
	[x-d-5-5-5, y-5-33, 33],

	[x-d-5-30, y-5-30, 33, 10],

	[x-d-5-20, 2, 20, 4],
	[x-d-5-20, 22, 20, 4],
	[x-d-5-20, 42, 20, 4],

	[x-d-5-25, 2, 20, 4],
	[x-d-5-25, 22, 20, 4],
	[x-d-5-25, 42, 20, 4],

	[x-d-5-30, 2, 20, 4],
	[x-d-5-30, 22, 20, 4],
	[x-d-5-30, 42, 20, 4],

	[x-d-5-35, 2, 20, 4],
	[x-d-5-35, 22, 20, 4],
	[x-d-5-35, 42, 20, 4],

	[x-d-5-40, 2, 20, 4],
	[x-d-5-40, 22, 20, 4],
	[x-d-5-40, 42, 20, 4],

	[x-d-5-45, 2, 20, 4],
	[x-d-5-45, 22, 20, 4],
	[x-d-5-45, 42, 20, 4],

	[x-d-5-50, 2, 20, 4],
	[x-d-5-50, 22, 20, 4],
	[x-d-5-50, 42, 20, 4],

	[x-d-5-55, 2, 20, 4],
	[x-d-5-55, 22, 20, 4],
	[x-d-5-55, 42, 20, 4],

	];

	difference() {
		union() {
			difference() {
				union() {
					base(x, y, h);
					for (s=saws) {
						translate([s[0]-2, s[1]-1, 5]) cube([2*2+(s[3]?s[3]:saw_thick), s[2]+2, s[2]/2]);
					}
					translate([0, 0, 0]) cube([34, y, 30]);

					peg_array([x-d/2], [d+5:10:x/2-d-5], 5, h-15);
				}
				translate([33, 0, 5]) peg_array([d:6:x/2-d], [d:6:y-d], drill_hole, 20);
				for (s=saws) {
					translate([s[0], s[1]+s[2]/2, 5]) cyl_hole(s[2], s[3]?s[3]:saw_thick);
				}
				translate([x-d-5-5, 59, 5]) cylinder(d=drill_hole, h=20);

				translate([0, 0, 5]) peg_array([133:10:150], [70:8:95], 5.5, 20);

				translate([1, 1, 2]) cube([32, 32, 31]);
				translate([1, 34, 2]) cube([32, y-35, 31]);
				cube([d/2, d/2, 33]);
				translate([0, y-d/2, 0])cube([d/2, d/2, 33]);

			}

			translate([d/2, d/2, 0]) cylinder(d=d, h=h);
			translate([d/2, y-d/2, 0]) cylinder(d=d, h=h);

		}
		translate([d/2, d/2, 0]) cylinder(d=d*3/4-.5, h=10);
		translate([d/2, y-d/2, 0]) cylinder(d=d*3/4-.5, h=10);
	}
}

plate1();

translate([0, y+10, 0]) plate2();