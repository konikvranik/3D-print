rotate([10,0,0]) {
    cube([70,4,24]);
    difference() {
        cube([70,8.6,4]);
        translate([1.2,4,2]) cube([70-1.2*2,3.4,4]);
    }
}
for(i=[0,66]) {
    translate([i,0,0]) {
        translate([0,-15,0]) cube([4,15,4]);
        cube([4,8.47,1.5]);
    }
}