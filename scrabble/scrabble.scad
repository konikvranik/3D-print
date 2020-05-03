
// width, height and depth of single piece
piece=[19,19,4]; // [19:19:4]

// Thickeness of letter
letter_thick=.4; 

// Corner rounding radius
r=2;

// Array of alphabet
alphabet = [
["A", "1",5],
["Á", "2",2],
["B", "3",2],
["C", "2",3],
["Č", "4",1],
["D", "1",3],
["Ď", "8",1],
["E", "1",5],
["É", "3",2],
["Ě", "3",2],
["F", "5",1],
["G", "5",1],
["H", "2",3],
["I", "1",4],
["Í", "2",3],
["J", "2",2],
["K", "1",3],
["L", "1",3],
["M", "2",3],
["N", "1",5],
["Ň", "6",1],
["O", "1",6],
["Ó", "7",1],
["P", "1",3],
["R", "1",3],
["Ř", "4",2],
["S", "1",4],
["Š", "4",2],
["T", "1",4],
["Ť", "7",1],
["U", "2",3],
["Ú", "5",1],
["Ů", "4",1],
["V", "1",4],
["X","10",1],
["Y", "2",2],
["Ý", "4",2],
["Z", "2",2],
["Ž", "4",1],
[ "",  "",2]
];


boards = [
	[
		[
			["3W",   "",   "", "2L",   ""],
			[  "", "2W",   "",   "",   ""],
			[  "",   "", "2W",   "",   ""],
			["2L",   "",   "", "2W",   ""],
			[  "",   "",   "",   "", "2W"]
		], [
			[  "",   "", "3W",   "",   ""],
			["3L",   "",   "",   "", "3L"],
			[  "", "2L",   "", "2L",   ""],
			[  "",   "", "2L",   "",   ""],
			[  "",   "",   "",   "",   ""]
		], [
			[  "", "2L",   "",   "", "3W"],
			[  "",   "",   "", "2W",   ""],
			[  "",   "", "2W",   "",   ""],
			[  "", "2W",   "",   "", "2L"],
			["2W",   "",   "",   "",   ""]
		]
	], [
		[
			[  "", "3L",   "",   "",   ""],
			[  "",   "", "2L",   "",   ""],
			["3W",   "",   "", "2L",   ""],
			[  "",   "", "2L",   "",   ""],
			[  "", "3L",   "",   "",   ""]
		], [
			["3L",   "",   "",   "", "3L"],
			[  "", "2L",   "", "2L",   ""],
			[  "",   "",  "*",   "",   ""],
			[  "", "2L",   "", "2L",   ""],
			["3L",   "",   "",   "", "2L"]
		], [
			[  "",   "",   "", "3L",   ""],
			[  "",   "", "2L",   "",   ""],
			[  "", "2L",   "",   "", "3W"],
			[  "",   "", "2L",   "",   ""],
			[  "",   "",   "", "3L",   ""]
		]
	], [
		[
			[  "",   "",   "",   "", "2W"],
			["2L",   "",   "", "2W",   ""],
			[  "",   "", "2W",   "",   ""],
			[  "", "2W",   "",   "",   ""],
			["3W",   "",   "", "2L",   ""]
		], [
			[  "",   "",   "",   "",   ""],
			[  "",   "", "2L",   "",   ""],
			[  "", "2L",   "", "2L",   ""],
			["3L",   "",   "",   "", "3L"],
			[  "",   "", "3W",   "",   ""]
		], [
			["2W",   "",   "",   "",   ""],
			[  "", "2W",   "",   "", "2L"],
			[  "",   "", "2W",   "",   ""],
			[  "",   "",   "", "2W",   ""],
			[  "", "2L",   "",   "", "3W"]
		]
	]
];

$fs=.25;

module letter(l, p) {

	linear_extrude (height=piece[2]-letter_thick) {
		translate([-piece[0]/2+r,-piece[1]/2+r,0]) circle(r=r);
		translate([-piece[0]/2+r,piece[1]/2-r,0]) circle(r=r);
		translate([piece[0]/2-r,-piece[1]/2+r,0]) circle(r=r);
		translate([piece[0]/2-r,piece[1]/2-r,0]) circle(r=r);
		square([piece[0],piece[1] - 2*r], center=true);
		square([piece[0] - 2*r,piece[1]], center=true);
	}
	translate([0,0,piece[2]-letter_thick]) linear_extrude(height=letter_thick) {
		text(text=l, halign="center", valign="center");
		translate([piece[0]/2-r,-piece[1]/2+r]) text(text=p, halign="right", valign="bottom", size=3);
	}
}

module pieces(x,y,i,j) {
	if (i<len(alphabet)) {
		translate([x,y,0]) letter(alphabet[i][0],alphabet[i][1]);
		pieces(x + piece[0] + 1 < 200 ? x + piece[0] + 1 : 0, x + piece[0] + 1 < 200 ? y : y + piece[1] + 1,
		j < alphabet[i][2]-1 ? i : i+1, j < alphabet[i][2]-1 ? j+1 : 0);
	}
}


module pivot() {
		translate([1,0,(2-.4)/2]) cube([3,2,2-.4], center=true);
		translate([3.5,0,(2-.4)/2]) cylinder(r=2, h=2-.4, center=true);
}

module pivothole() {
	translate([0,0,1]) cube([4,2+.4,2], center=true);
	translate([-3,0,1]) cylinder(r=2+.2, h=2, center=true);
}


module plate(arr, pivots) {
	pl = (piece + [1,1,-piece[2]]) * 5 + [.5,.5,2.5];
	pos=[ for (i = [1:4]) [ [pl[0], (piece[0]+1)*i+.25, 0, (piece[0]+1)*i+.25], [(piece[1]+1)*i+.25, 0, (piece[1]+1)*i+.25, pl[1]] ] ];

	difference() {
		
		cube(pl);
		
		translate([(piece[0]+1)/2+.25, (piece[0]+1)/2+.25, 2]) for (i = [0:len(arr)-1]) {
			for (j = [0 : len(arr[i])-1]) {
				translate([j * (piece[0]+1 ),  i * (piece[1]+1), 0]) {
					translate([0,0,-letter_thick]) linear_extrude(height=piece[2]) text(text=arr[i][j], halign="center", valign="center", size=9);
					translate([0,0,2]) cube(piece+[.5,.5,-piece[2]+4], center=true);
				}
			}
		}
		
		for (i = [0:3]) {
			if (pivots[i] == -1) {
				for (j = [0:len(pos)-1]) {
					translate([pos[j][0][i], pos[j][1][i], 0]) rotate([0,0,i*-90]) pivothole();
				}
			}
		}
	}
	for (i = [0:3]) {
		if (pivots[i] == 1) {
			for (j = [0:len(pos)-1]) {
				translate([pos[j][0][i],pos[j][1][i],0]) rotate([0,0,i*-90]) pivot();
			}
		}
	}
}

module board() {
	for (i=[0:len(boards)-1]) {
		for (j=[0:len(boards[i])-1]) {
			translate([200 + i*101, j*101, 0]) plate(boards[j][i], [i < 2 ? 1 : 0, j > 0 ? -1 : 0, i > 0 ? -1 : 0, j < 2 ? 1 : 0]);
		};
	};
}

module stand() {
	difference() {
		rotate([60,0,0]) {
			difference() {
				translate([-2,-10,-50]) cube([(piece[0]+.5)*7.5+2*2, piece[1]+1+10, piece[2]+2+2+49]);
				cube([(piece[0]+.5)*7.5, piece[1]+1, piece[2]+2]);
				translate([0,2,0]) cube([(piece[0]+.5)*7.5, piece[1]+1, piece[2]+2+3]);
				translate([0,-12,-51]) cube([(piece[0]+.5)*7.5, 11, 60]);
				translate([0,-10,-51]) cube([(piece[0]+.5)*7.5, 50, 50]);
				translate([-10,-10,piece[2]+2+6]) rotate([-22,0,0]) cube([(piece[0]+.5)*7.5+20, 50, 50]);
			}
		}
		rotate([30,0,0]) translate([-10,18,-50]) cube([200,100,100]);
		translate([-10,-20,-50]) cube([200,150,50]);
	}
}

module smooth(r=1, size=1e12) {
		if($preview || r==0) children();
		else  if( r>0 ) minkowski() {
			 children();
			 sphere(r);
		} else {
			 size2 = size*[1,1,1];
			 size1 = size2*0.99;
			 difference() {
				 cube(size1, center=true);
				 minkowski(){
					 difference(){
						 cube(size2, center=true);
						 children();
					 }
					 sphere(-r);
				 }
			 }
		 }
	
}

pieces(0,0,0,0);
board();
translate([0,-40,0]) stand();
