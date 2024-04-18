glass = 2.6;
thick = 1;
width = 210;
height = 318;
depth = 12;
cell = 10;
$fn=32;

module frame() {
	difference(){
		union() {
			difference(){
				translate([0,0,thick/2]) minkowski() {
					cube([width,height,depth],true);
					sphere(thick);
				}
				translate([0,0,thick+thick/2]) cube([width,height,depth+thick],true);
			};
			cube([width-2*thick-2*glass,height-2*thick-2*glass,depth],true);
		};
		union() {
			difference() {
				cube([width-4*thick-2*glass,height-4*thick-2*glass,depth+2*thick],true);
				translate([-width/2+glass+3*thick,-height/2+glass+3*thick,-depth/2+thick/2]) minkowski() {
					cylinder(d=10,h=depth+4*thick);
					sphere(thick);
				};
				translate([width/2-glass-3*thick,-height/2+glass+3*thick,-depth/2+thick/2]) minkowski() {
					cylinder(d=10,h=depth+4*thick);
					sphere(thick);
				}
			}
			translate([-width/2+glass+3*thick,-height/2+glass+3*thick,-depth/2+thick]) cylinder(d=10,h=depth+4*thick);
			translate([width/2-glass-3*thick,-height/2+glass+3*thick,-depth/2+thick]) cylinder(d=10,h=depth+4*thick);
		}
	}
}

module mesh() {
	for (i = [0:cell+thick:width/2-glass-thick]) {
		translate([i,height/2,-depth/2]) rotate([90,0,0])  cylinder(h=height,d=thick); //cube([thick,height,thick]);
	};
	for (i = [0:-cell-thick:-width/2+glass+thick]) {
		translate([i,height/2,-depth/2]) rotate([90,0,0])  cylinder(h=height,d=thick);
	};
	for (j = [-thick/2:-cell-thick:-height/2+glass+thick]) {
		translate([-width/2,j,-depth/2]) rotate([0,90,0])  cylinder(h=width,d=thick);
	};
}

difference() {
	union() {
		frame();
		mesh();
	};
	translate([0,height/2,0]) cube([width+500,height, depth+500],true);
};


translate([width+20,0,0]) difference() {
	union() {
		frame();
		mesh();
	};
	translate([0,height/2,0]) cube([width+500,height, depth+500],true);
	translate([0,-height,0]) cube([width+500,height, depth+500],true);
	
};