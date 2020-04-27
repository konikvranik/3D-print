piece=[19,19,4];
letter_thick = .4;
r=2;
$fn=64;
alphabet = [
["A","1",5],
["Á","2",2],
["B","3",2],
["C","2",3],
["Č","4",1],
["D","1",3],
["Ď","8",1],
["E","1",5],
["É","3",2],
["Ě","3",2],
["F","5",1],
["G","5",1],
["H","2",3],
["I","1",4],
["Í","2",3],
["J","2",2],
["K","1",3],
["L","1",3],
["M","2",3],
["N","1",5],
["Ň","6",1],
["O","1",6],
["Ó","7",1],
["P","1",3],
["R","1",3],
["Ř","4",2],
["S","1",4],
["Š","4",2],
["T","1",4],
["Ť","7",1],
["U","2",3],
["Ú","5",1],
["Ů","4",1],
["V","1",4],
["X","10",1],
["Y","2",2],
["Ý","4",2],
["Z","2",2],
["Ž","4",1],
["","",2]
];


board11=[
	["3W", "", "", "2L", ""],
	["", "2W", "","", ""],
	["", "", "2W", "", ""],
	["2L", "", "", "2W", ""],
	["", "", "", "", "2W" ]
];

board21=[
	["", "", "3W", "", ""],
	["3L", "", "","", "3L"],
	["", "2L", "", "2L", ""],
	["", "", "2L", "", ""],
	["", "", "", "", "" ]
];

board31=[
	["", "2L", "", "", "3W"],
	["", "", "","2W", ""],
	["", "", "2W", "", ""],
	["", "2W", "", "", "2L"],
	["2W", "", "", "", "" ]
];

board12=[
	["", "3L", "", "", ""],
	["", "", "2L","", ""],
	["3W", "", "", "2L", ""],
	["", "", "2L", "", ""],
	["", "3L", "", "", "" ]
];

board22=[
	["3L", "", "", "", "3L"],
	["", "2L", "","2L", ""],
	["", "", "*", "", ""],
	["", "2L", "", "2L", ""],
	["3L", "", "", "", "2L" ]
];

board32=[
	["", "", "", "3L", ""],
	["", "", "2L","", ""],
	["", "2L", "", "", "3W"],
	["", "", "2L", "", ""],
	["", "", "", "3L", "" ]
];


board13=[
	["", "", "", "", "2W" ],
	["2L", "", "", "2W", ""],
	["", "", "2W", "", ""],
	["", "2W", "","", ""],
	["3W", "", "", "2L", ""]
];

board23=[
	["", "", "", "", "" ],
	["", "", "2L", "", ""],
	["", "2L", "", "2L", ""],
	["3L", "", "","", "3L"],
	["", "", "3W", "", ""]
];

board33=[
	["2W", "", "", "", "" ],
	["", "2W", "", "", "2L"],
	["", "", "2W", "", ""],
	["", "", "","2W", ""],
	["", "2L", "", "", "3W"]
];

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
	translate([-1.5,0,0]) {
		translate([0,-1,0]) cube([5,2,piece[2]/2-1]);
		cylinder(r=2, h=piece[2]/2-.5);
	}
}

module pivothole() {
	translate([3,0,0]) cube([3,2+.4,piece[2]/2+1], center = true);
	translate([0,0,0]) cylinder(r=2+.2, h=piece[2]*4, center = true);
}


module plate(arr, pivots) {
	pl = (piece + [1,1,0]) * 5 ;
	difference() {
		cube([pl[0]+1, pl[1]+1, piece[2]/2]);
		translate([piece[0]/2+1,piece[0]/2+1,1]) for (i = [0:len(arr)-1]) {
			for (j = [0 : len(arr[i])-1]) {
				translate([j * (piece[0]+1), i * (piece[1]+1), piece[2]]) {
					
					rotate([0,0,180]) translate([0,0,-piece[2]]) linear_extrude(height=piece[2]) text(text=arr[i][j],halign="center",valign="center", size=9);
					cube(piece+[.5,.5,piece[2]-1], center=true);
				}
			}
		}
		if (pivots[0] == -1) {
			translate([3,piece[1]*1.5,0]) mirror([1,0,0]) pivothole();
			translate([3,piece[1]*3.5,0]) mirror([1,0,0]) pivothole();		
		}
		if (pivots[1] == -1) {
			translate([piece[1]*1.5,3,0]) rotate([0,0,-90]) pivothole();
			translate([piece[1]*3.5,3,0]) rotate([0,0,-90]) pivothole();		
		}
		if (pivots[2] == -1) {
			translate([pl[0]-3,piece[1]*1.5,0]) pivothole();
			translate([pl[0]-3,piece[1]*3.5,0]) pivothole();		
		}
		if (pivots[3] == -1) {
			translate([piece[1]*1.5,pl[1]-3,0]) rotate([0,0,90]) pivothole();
			translate([piece[1]*3.5,pl[1]-3,0]) rotate([0,0,90]) pivothole();		
		}

	}
	if (pivots[0] == 1) {
		translate([-3,piece[1]*1.5,0]) pivot();
		translate([-3,piece[1]*3.5,0]) pivot();		
	}
	if (pivots[1] == 1) {
		translate([piece[1]*1.5,-3,0]) rotate([0,0,90]) pivot();
			translate([piece[1]*3.5,-3,0]) rotate([0,0,90]) pivot();	
	}
	if (pivots[2] == 1) {
		translate([pl[0]+3,piece[1]*1.5,0]) mirror([1,0,0]) pivot();
			translate([pl[0]+3,piece[1]*3.5,0]) mirror([1,0,0]) pivot();
	}
	if (pivots[3] == 1) {
		translate([piece[1]*1.5,pl[1]+3,0]) rotate([0,0,-90]) pivot();
			translate([piece[1]*3.5,pl[1]+3,0]) rotate([0,0,-90]) pivot();		
	}
	
}

module board() {
	translate([200,0,0]) plate(board11,[0,0,1,1]);
	translate([301.5,0,0]) plate(board21,[-1,0,1,1]);
	translate([403,0,0]) plate(board31,[-1,0,0,1]);
	translate([200,101.5,0]) plate(board12,[0,-1,1,1]);
	translate([301.5,101.5,0]) plate(board22,[-1,-1,1,1]);
	translate([403,101.5,0]) plate(board32,[-1,-1,0,1]);
	translate([200,203,0]) plate(board13,[0,-1,1,0]);
	translate([301.5,203,0]) plate(board23,[-1,-1,1,0]);
	translate([403,203,0]) plate(board33,[-1,-1,0,0]);
}

pieces(0,0,0,0);

board();