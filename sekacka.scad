d1=22.5;
d2=48;
d3=25.2;
h=11.73;
h1=2.67;

di1=10.2;
di2=12.05;

$fs=.2;

difference() {
    union() {
        cylinder(d=d1,h=h);
        translate([0,0,h1]) {
            translate([0,0,h-h1-4]) cylinder(d=d3,h=h1+2);
            cylinder(d1=d1,d2=32,h=h-2*h1-5);
            translate([0,0,h-2*h1-5]) {
                difference() {
                    cylinder(d=d2,h=5);
                    translate([0,0,4]) cylinder(d1=25,d2=35,h=1.1);
                }
            }
        }
    }
    translate([0,0,-1]) {
        cylinder(d=di1, h=h+2);
        for (a = [0:30:360]) {
            rotate([0,0,a]) translate([di1/2,0,0]) cylinder(d=di2-di1,h=h+2);
        }
    }
}