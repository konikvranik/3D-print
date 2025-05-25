diameter=4.5;
width=20;
thickness=2;
height=10;
hole=4;
space=3;
$fa=1;
$fs=.2;

difference() {
	union() {
		cube([width+2*(hole+2*space), height, thickness], center=true);
		translate([-width/2, 0, thickness/2]) {
			cube([width, thickness, diameter]);
			translate([0, -diameter/2, diameter]) rotate([0, 90, 0]) difference() {
				cylinder(d=diameter+2*thickness, h=width);
				translate([0, 0, -.5]) {
					cylinder(d=diameter, h=width+1);
					translate([0, -diameter, 0]) cube([diameter, 2*diameter, width+1]);
				}
			}
		}
		translate([0, thickness, thickness/2]) rotate([45, 0, 0]) cube([width, diameter, diameter], center=true);
	}
	translate([-width/2-space-hole/2, 0, 0]) cylinder(d=hole, h=thickness*2, center=true);
	translate([width/2+space+hole/2, 0, 0]) cylinder(d=hole, h=thickness*2, center=true);
	translate([0, 0, -2*thickness])    cube([width+2*(hole+2*space), height, 3*thickness], center=true);
}