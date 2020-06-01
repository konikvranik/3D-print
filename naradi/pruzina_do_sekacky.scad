
h = 30;
di = 9;
do = 14;
n=8;
$fn=64;
th=3;
tw=400;


module spring(h=h) {
	linear_extrude(height = h, center = false, twist = tw)
	translate([(di + (do-di)/2)/2, 0])
	//square([(do-di)/2,th], center=true);
	circle(d=(do-di)/2);
}

module tail() {
	difference() {
		cylinder(d=do,center=true);
		cylinder(d=di,center=true);
	}
}

for (i = [0:360/n:360]) {
	rotate ([0,0,i]) spring();
}

tail();
translate([0,0,h]) tail();;