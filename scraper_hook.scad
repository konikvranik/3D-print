$fs=.1;
$fa=.1;

difference() {
    cube([15,5.1,10]);
    translate([1.5,1.5,0]) cube([12,2.1,12]);
    translate([1.5,1.5,0]) cube([30,1.3,12]);
}

translate([20,0,5]) rotate([90,0,0]) {
    intersection() {
        union(){
            cylinder(h=8,d=20);
            translate([0,0,8]) cylinder(h=1.5,d=40);
        }
        translate([-20,-5,0]) cube([15,10,30]);
    }
}