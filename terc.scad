inner=145;
outer=160;
terc=[138, 148];

difference() {
	cube([outer, outer, 1], center=true);
	cube([terc[0]-7*2, terc[1]-7*2, 10], center=true);
}
