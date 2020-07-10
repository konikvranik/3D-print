zasobnik=[79, 6.7, 6.7];
ocko=13;
thick=2.5;

$fa=1;
$fs=.2;

difference() {
	union() {
		cube(zasobnik+[thick, 2*thick, 2*thick]);
		translate([zasobnik[0]-ocko/2, zasobnik[1]/2+thick, zasobnik[2]]) rotate([0, 30, 0]) translate([0, 0, 0]) cylinder(d1=4.7+thick, d2=35+thick/2, h=40);
	}
	translate([0, thick, thick]) cube(zasobnik);
	translate([zasobnik[0]-ocko/2, zasobnik[1]/2+thick, zasobnik[2]]) rotate([0, 30, 0]) translate([0, 0, 0]) cylinder(d1=4.7, d2=35, h=40+1);
}