inner_depth=50;
outer_depth=5;
thickness=2;
bottom_height=10;
top_height=15;
hole=3.5;
width=220;

$fa=1;
$fs=.2;

difference() {
	union() {
		translate([0, 0, 10]) union() {
			translate([0, -outer_depth, 0]) cube([width, inner_depth+outer_depth, thickness]);
			translate([0, -outer_depth-thickness, 0]) cube([width, thickness, top_height+thickness]);
		}
		translate([10, 0, 0]) cube([width-20, inner_depth-10, 10]);
		translate([0, -thickness, -bottom_height]) cube([width, thickness, bottom_height+10]);
	}
	translate([width/5, 0, -bottom_height/2]) rotate([90, 0, 0]) cylinder(d=hole, h=4*thickness, center=true);
	translate([4*width/5, 0, -bottom_height/2]) rotate([90, 0, 0]) cylinder(d=hole, h=4*thickness, center=true);
}