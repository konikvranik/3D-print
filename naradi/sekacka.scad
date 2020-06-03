d1=22.5;
d2=48;
d3=26;
h=13;
h1=2.67;

di1=10.2;
di2=12.05;

$fs=.2;
$fa=1;

difference() {
    union() {
        cylinder(d=d1,h=h);
        translate([0,0,h1]) {
            translate([0,0,h-h1-4]) cylinder(d=d3,h=h1+2);
            cylinder(d1=d1,d2=32,h=h-2*h1-5);
            translate([0,0,h-2*h1-5]) {
                difference() {
                    union() {
                        cylinder(d=d2, h=5);
                        cylinder(d=56, h=4);
                    }
                    translate([0,0,4]) cylinder(d1=25,d2=35,h=1.1);
        for (a = [0:40:360]) {
            rotate([0,0,a]) translate([d2/2+1.5,0,0]) cylinder(d=3,h=20);
        }
                }
            }
        }
    }
    translate([0,0,-1]) {
        cylinder(d=di1, h=h+2);
        for (a = [0:40:360]) {
            rotate([0,0,a])  translate([di1/2,0,0]) // cylinder(d=di2-di1,h=h+2);
                cube([di2-di1,1.8,3*h+2], center=true);
        }
    }
}