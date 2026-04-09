d = 90;
h = 55;
t = 5;
bottom = 5;

$fs=.1;
$fa=1;

difference() {
    cylinder(h = h + bottom + t, d = d + 2 * t);
    translate([0, 0, bottom+t]) cylinder(h = h + bottom + t, d=d);
    translate([0, 0, -t]) cylinder(h=bottom+t, d=d);
}
