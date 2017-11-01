// source: trunk_roller_shutter.jscad

function roundCorners(obj, rs) {
	var cls = [];
	for (i=0; i<rs.length; i++) {
		var r = rs[i];
		if(r) {
			var x=obj.getBounds()[0].x;
			var y=obj.getBounds()[0].y;
			var rx = r;
			var ry = r;
			var z=obj.getBounds()[1].z;
			switch(i) {
				case 2:
				case 3:
					y = obj.getBounds()[1].y;
					ry=-r;
					if(i==3)
						break;
				case 1:
					x = obj.getBounds()[1].x;
					rx=-r;
				default:
			}
			obj = obj
				.subtract(cube({size:[rx,ry,z]}).translate([x,y,0]))
				.union(cylinder({r:r,h:z}).translate([x+rx,y+ry,0]));
		}
	}
	return obj;
}

function rawShell(x,y,z,r1,r2) {
	var p = 50-2.5;
	var s = 7;
	var r = 40;
	return roundCorners( cube([x,y,z]), [r1,0,r2,r2])
		.subtract(cube([100,100,z]).translate([0,-100,0]).rotate([p,0,0],[0,0,1],20)) // zkosit jednu stěnu
		.subtract(cube([10,20,z]).translate([p-s,0,0]))
		.union(cylinder({r:r,h:z}).subtract(cube([2*r,2*r,z]).translate([-r,10,0]).union(cube([r,2*r,z]).translate([-r,-r,0]))).translate([p-s,r,0]))
		;
}

function shell(x,y,z,w) {
	var r1 = 20-w;
	var r2 = 10-w;
	var h1 = 30;

	return rawShell(x-2*w,y-2*w,z,r1,r2)
		.subtract(cube([15,32,z]).translate([0,y-32-w,52-2*w])) // vyříznout výsek
		.subtract(cube([12,37-w-6,h1]).union(cylinder({r:6,h:h1}).translate([6,37-w-6,0])).translate([25,0,0]) // vyříznout škvíru
	).expand(w,CSG.defaultResolution3D)
		.subtract(rawShell(x-2*w,y-2*w,z,r1,r2).translate([0,0,w])) // vydlábnout vnitřek
		.translate([w,w,w]); // zalícovat s osama
}

function main(){
	CSG.defaultResolution3D=16;
	return shell(97,68,68,2.5);
}
