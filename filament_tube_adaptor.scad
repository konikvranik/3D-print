dis = 2.5;
dos = 4;
dil = 2.5;
dol = 4;
d = 7;
h = 5;

$fa=.1;
$fs = .05;
difference() {
    cylinder(d=d, h=h);
    translate([0,0,-1]) cylinder(d=dos+.1, h/2+1);
    translate([0,0,h/2+1.5]) cylinder(d=dol+.1, h/2+1);
    cylinder(d=dis+.8, h);
}