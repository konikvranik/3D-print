
boundary=[37,25.4,20]+[.3,.2,0];
space=[.2,.2,.1];
conn = [0,3,21.5,5];
reset = [9.5,3,6,4];
wall = 1;

difference() {
	translate([-wall,-wall,-wall]) cube(boundary+[2*wall,2*wall,wall]);
	cube(boundary+[0,0,1]);
	translate([conn[0],-wall-1,conn[1]]) cube([conn[2],1+wall+1,conn[3]]);
	translate([boundary[0]-1,reset[0],reset[1]]) cube([1+wall+1,reset[2],reset[3]]);
}

translate([boundary[0]+2*wall+5,0,0]) difference() {
	translate([-2*wall,-2*wall,-wall]-space/2) cube(boundary + [4*wall,4*wall,2*wall] + space);
	translate([-wall,-wall,0]-space/2) cube(boundary + [2*wall,2*wall,wall+1] + space);
	translate([0,boundary[1],boundary[2]-conn[1]-conn[3]]) cube([conn[2],1+wall+1,conn[1]+conn[3]+wall+1]);
	translate([boundary[0],reset[0],boundary[2]-reset[1]-reset[3]]) cube([1+wall+1,reset[2],reset[3]]);
}