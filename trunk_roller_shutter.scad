
module roundCorner() {
}

module rawShell(x,y,z,r1,r2) {
    union() {
        difference() {
            cube([x,y,z]);
            cube([r1,r1,z]);
            translate([0,y-r2,0])
            cube([r2,r2,z]);
        };
        translate([r1,r1,0])
            cylinder(r=r1, h=z);
        translate([r2,y-r2,0])
            cylinder(r=r2, h=z);
    };
}

module shell(x,y,z,w) {
    r1 = 20-w;
    r2 = 10-w;
    h1 = 30;
    translate([w,w,0])
        difference() {
            minkowski() {
                difference() {
                    rawShell(x-2*w,y-2*w,z,r1,r2);
                    translate([0,y-32-w,52-w])
                        cube([15,32,z]);
                    translate([30,0,0]) {
                        cube([12,37-w-6,h1]);
                        translate([6,37-w-6,0])
                            cylinder(r=6,h=h1);
                    }
               }
                sphere(r=w);
            };
            translate([0,0,w])
                rawShell(x-2*w,y-2*w,z,r1,r2);
        }
}

render(convexity=4) {
        shell(97,68,68,2.5);
     
}