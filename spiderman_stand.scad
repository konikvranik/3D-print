rotate([10,0,0]) {
    cube([70,4,24]);
    difference() {
        cube([70,8.6,4]);
        translate([1.2,4,2]) cube([70-1.2*2,3.4,4]);
    }
}

difference() {
            translate([0,-15,0]) cube([70,15,23]);
            translate([-1,-35,0]) rotate([-22.1,0,0]) cube([72,20,50]);
            translate([4,-15,-1]) cube([62,30,6]);
}
        
for(i=[0,66]) {
    translate([i,0,0]) {
        cube([4,8.47,1.5]);
    }
}