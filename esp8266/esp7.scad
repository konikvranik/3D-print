boundary=[56,44];
conn= [8.3,7.8,43];
postrot=[23,17]; // pozice středu otvoru

thick=2;
bottom=[thick,48];

spodek=30;

wire = 3;

magic = 0;

difference() {
	union() {
		difference() {
			translate([-thick,-thick,-bottom[0]]) cube([boundary[0]+2*thick, boundary[1]+2*thick, bottom[0]+bottom[1]]);
			cube([boundary[0],boundary[1],bottom[1]+1]);
		}
		translate([postrot[0]-conn[0]/2-1-wire,postrot[1]-conn[1]/2-1,-bottom[0]]) cube([conn[0]+2+wire,conn[1]+2,conn[2]]);
	}
	translate([postrot[0]-conn[0]/2,postrot[1]-conn[1]/2,-bottom[0]-1]) cube([conn[0],conn[1],bottom[0]+bottom[1]]);
	translate([postrot[0]-conn[0]/2-wire,postrot[1]-conn[1]/2,-bottom[0]+thick]) cube([conn[0]+wire,conn[1],bottom[0]+bottom[1]]);
}


translate([boundary[0] + 2 * thick, -2 * thick, -thick]) difference() {
	cube([boundary[0] + 4 * thick + magic, boundary[1] + 4 * thick + magic, 30]);
	translate([thick,thick,thick]) cube([boundary[0] + 2 * thick + magic, boundary[1] + 2 * thick + magic, 30]);
	
}