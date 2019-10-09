

connector = [15,9,11];
pcb=[23.5,24.8,1.3+11+3];
esp=[24.6,14.9,3];

module case() {
    module interior() {
        translate([10,2,5]) cube(connector);
        translate([2,3+9-1.5,5+11]) cube(esp);
        translate([0,0,5-1.3]) cube(pcb);
        translate([1.5,4,0]) cube([20,19,5-1.3]);
        difference() {
            translate([-15,0,0]) cube([15,25.3,5+11+3]);
            translate([-5,3+9.5,-1]) cube([5,10,5+11+5]);
        }
    }

    difference() {
        cube([ 15+23.5+5, 25.3+2 ,5+11+4]);
        translate([16,1,1]) interior();
        translate([16,1,10]) interior();
        translate([15+20,3+4.5,11+7-2.5-1.5]) rotate([0,90,0]) cylinder(d=9.5,h=30);
        translate([-1,(25.3+2)/2,5+11+3-2.5+1]) {
            rotate([0,90,0]) cylinder(d=5,h=5);
            translate([0,-2.5,0]) cube([5,5,2.5]);
        }
    }
}

translate([50,-(25.3+2.5)/2,-(5+11+3.5)/2]) case();

difference() {
    sphere(d=60);
    translate([-21,-(25.3+2.5)/2,-(5+11+4.4)+7/2]) cube([ 15+23.5+50, 25.3+2.5 ,5+11+4.4]);
    translate([-40,-15/2,-7/2]) cube([ 15+23.5+50, 15 ,7]);
     
}

translate([-60,0,0]) difference() {
    sphere(d=40);
    translate([0,0,-3.1/2]) intersection() {
        cube([42,12,3], center=true);
        translate([-21,0,-50+3/2]) rotate([0,90,0]) cylinder(r=50,h=42);
    }
     
}

