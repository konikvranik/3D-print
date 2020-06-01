outer=42.3;
outer2=42.3;
inner=35.8;
h=21;
h2=16.3;
$fs=.2;
$fn=128;

module ring1() {
	difference() {
		union() {
			cylinder(d=outer, h=h, center=true);
			translate([0, 0, h/2]) cylinder(d=outer+6, h=2, center=true);
		}
		cylinder(d=inner, h=h+3, center=true);
		translate([inner/2-1, 0, 0])cube([inner, 3, h+13], center=true);
	}
}

module ring2() {
	difference() {
		union() {
			cylinder(d=outer2, h=h2, center=true);
			translate([-2.5, 0, 0]) cylinder(d=outer2, h=4.5, center=true);
			translate([2.5, 0, 0]) cylinder(d=outer2, h=4.5, center=true);
			cube([outer2+2, 8, h2], center=true);
		}
		cylinder(d=inner, h=h2+3, center=true);
		cube([inner/4, outer2+6, h+13], center=true);
	}
}

//ring1();

translate([2*outer, 0, 0]) ring2();