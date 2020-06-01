
boundary=[26.5,16.5,17.5];
space=[.2,.2,.1];
conn = [1.25,3,14,3];

wall = 1;

difference() {
	translate([-wall,-wall,-wall]) cube(boundary+[2*wall,2*wall,wall]);
	cube(boundary+[0,0,1]);
	translate([-wall-1,conn[0],conn[1]]) cube([1+wall+1,conn[2],conn[3]]);
}

translate([boundary[0]+2*wall+5,0,0]) difference() {
	translate([-2*wall,-2*wall,-wall]-space/2) cube(boundary + [4*wall,4*wall,2*wall] + space);
	translate([-wall,-wall,0]-space/2) cube(boundary + [2*wall,2*wall,wall+1] + space);
	translate([boundary[0]+2*wall-1,conn[0],boundary[2]-conn[1]-conn[3]]) cube([1+wall+1,conn[2],conn[3]]);
}