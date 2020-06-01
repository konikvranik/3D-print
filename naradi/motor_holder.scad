motor_d = 20.5;
motor = 15.5;
h = 32;
hole_h =19.4;

hole_distance = 13.2;
hole_d = 2.9;
rounding = false;

$fn=0;
$fa=.01;
$fs=$preview ? 2 : .5;


 module offset_3d(r=1, size=1e12) {
     n = ($fs==undef || $preview) ? 3: $fs;
     if(r==0) children();
     else 
         if( r>0 )
             minkowski(){
                 children();
                 sphere(r, $fs=n);
             }
         else {
             size2 = size*[1,1,1];
             size1 = size2*0.99;
             difference(){
                 cube(size2, center=true);
                 minkowski(){
                     difference(){
                         cube(size1, center=true);
                         children();
                     }
                     sphere(-r, $fs=n);
                 }
             }
         }
}
 
module fillet(r=1.5) {
	if ($preview || ! rounding) {
		children();
	} else {
	offset_3d(r) offset_3d(-r) // exterior fillets
         offset_3d(-r) offset_3d(r)  // interior fillets
	 render() children();
	}
	
}


module motor(motor_d, motor, h) {
	intersection() {
		cylinder(d=motor_d, h = h, center = true);
		cube([motor_d, motor, h], center = true);
	}
}


difference() {

	fillet() {
		cube([24.4,4,h], center = true);
		translate([0,10,0]) cube([6.5,20,h], center = true);
		translate([0,28,0]) {
			motor(motor_d + 9, motor + 9, h);
			translate([6+motor_d/2,0,0]) cube([12, 12.3, h],center = true);
		}
	}

	translate([hole_distance/2, 0, hole_h/2]) rotate([90,0,0]) cylinder(d=hole_d, h = 10, center = true);
	translate([-hole_distance/2, 0, hole_h/2]) rotate([90,0,0]) cylinder(d=hole_d, h = 10, center = true);
	translate([-hole_distance/2, 0, -hole_h/2]) rotate([90,0,0]) cylinder(d=hole_d, h = 10, center = true);
	translate([hole_distance/2, 0, -hole_h/2]) rotate([90,0,0]) cylinder(d=hole_d, h = 10, center = true);

	translate([0,28,0]) {
		motor(motor_d, motor, 100);
		translate([30/2,0,0]) cube([30, 3.8, h+2], center = true);
		translate([18, 0, hole_h/2]) rotate([90,0,0]) cylinder(d=hole_d, h = 50, center = true);
		translate([18, 0, -hole_h/2]) rotate([90,0,0]) cylinder(d=hole_d, h = 50, center = true);
	}

}
