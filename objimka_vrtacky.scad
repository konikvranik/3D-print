outer=42.3;
inner = 35.8;
h=21;
$fs=.2;

difference() {
	union() {
		cylinder(d=outer,h=h,center=true);
		translate([0,0,h/2]) cylinder(d=outer+6,h=2,center=true);
	}
	cylinder(d=inner,h=h+3,center=true);
	translate([inner/2-1,0,0])cube([inner,3,h+13],center=true );
}