$fn=128;

module vyrez() {
    //translate([0,-17,-1]) mirror([1,0,0])rotate([0,0,60]) cube([20,20,42]);
    //translate([30,-17,-1]) rotate([0,0,60]) cube([20,20,42]);
    //translate([7,0,-1]) cube([16,10,42]);
    translate([20,-15,-1]) cylinder(h=42, d=56);
}

module half() {
difference () {
translate([0,-7,0]) rotate([0,0,4])  difference() {
    cube([150,20,40]);
    translate([10,-15,-1]) rotate([0,0,60]) cube([20,50,42]);
    translate([35,0,0]) vyrez();
    translate([90,-18,-1]) rotate([0,0,13]) cube([200,20,42]);
    translate([82,3,-1]) rotate([0,0,13]) cube([35,2,42]);
}
translate([0,-20,-1]) cube([200,20,42]);
}
}

module zuby() {
l = 4;
    for (i= [0:cos(45)*l*2-2*cos(45):50]) {
        translate([i,-cos(45)*l/2,-1]) rotate([0,0,45]){
            cube([l,1,42]);
            cube([1,l,42]);
        }
    }
}

module body() {
half();
mirror([0,1,0]) half();
}

module kolik() {
difference() {
body();
translate([.5,0,0]) zuby();
}
}

difference() {
    scale([1.3,1.5,1]) kolik();
    
    translate([40,31,20]) rotate([90,0,0])
   { 
       translate([0,0,9]) cylinder(d=12, h=6);
       translate([0,0,3])  cylinder(d=5, h=6);
       translate([-12,0,6])  cylinder(d=12, h=9);
       translate([-10,-2.5,3]) cube([10,5,8]);
       translate([-12,-6,9]) cube([12,12,6]);
       
       translate([140,0,-10]) rotate([0,12,0]) cylinder(d=5,h=20);
   }
    
}

