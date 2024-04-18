$fa=.01;
$fs=.1;

difference() {
    union() {
        cylinder(h=20, d=6);
        translate([0,0,21]) cylinder(h=6,d1=8,d2=10);
        translate([0,0,20]) cylinder(h=1,d1=6,d2=8);
    }
    translate([0,0,4]) cylinder(d=4.1,h=50);
    translate([0,0,-1]) cylinder(d=2.7,h=50);
}