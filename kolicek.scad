$fn=$preview ? 16 : 128;

w = 40;

module vyrez() {
    translate([20,-15,-1]) cylinder(h=w+2, d=56);
}

module halfbody() {
	difference() {
				cube([150,20,w]);
				translate([12,-15,-1]) rotate([0,0,57]) cube([20,50,w+2]);
				translate([35,0,0]) vyrez();
				translate([90,-18,-1]) rotate([0,0,13]) cube([200,20,w+2]);
	}
}

module half() {
    translate([0,-7,0]) rotate([0,0,4])  difference() {
		if ($preview) {
			halfbody();
		} else {
			minkowski() {
				halfbody();
				sphere($fn=16);
			}
		}
        translate([82,3,-1]) rotate([0,0,13]) cube([35,2,w+2]);
    }
}

module zuby() {
l = 4;
    for (i= [0:cos(45)*l*2-2*cos(45):50]) {
        translate([i,-cos(45)*l/2,-1]) rotate([0,0,45]){
            cube([l,1,w+2]);
            cube([1,l,w+2]);
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
translate([3.3,0,0]) zuby();
}
}




difference() {
    scale([1.3,1.5,1]) kolik();
    
    translate([40,29,w*1/2]) rotate([90,0,0])
   { 
       translate([0,0,9]) cylinder(d=12, h=6);
       translate([0,0,3])  cylinder(d=5, h=6);
       translate([-12,0,5])  cylinder(d=12, h=10);
       translate([-10,-2.5,3]) cube([10,5,8]);
       translate([-12,-6,9]) cube([12,12,6]);
       
       translate([140,0,-10]) rotate([0,12,0]) {
           cylinder(d=5,h=20);
           translate([0,0,8]) cylinder(d=12,h=20);
       }
   }
    
}

