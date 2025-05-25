d1 = 14.94;
d2 = 17.85;
d3 = 14.5;
d4 = 12.65;
d5 = 10;
s = 2.85;
di1 = 12.3;
di2 = 5.75;


h1 = 2.5;
h2 = 1.3;
h3 = 5.75 - h1 - h2;
h4 = 4.5;
ht = h1 + h2 + h3 + h4;
hi1 = 4.3;
hi2 = 3.7;

$fa = 1;
$fs = .1;


module body() {
    cylinder(h = h1, d = d1);
    translate([0, 0, h1]) {cylinder(h = h2, d = d2);
        translate([0, 0, h2]) {cylinder(h = h3, d1 = d3, d2 = d4);
            translate([0, 0, h3]) cylinder(h = h4, d = d5);
        }
    }

}

difference() {
    body();
    cylinder(d = s, h = ht + 1);
    translate([0, - s / 2, - 1]) cube([d2, s, ht + 2]);
    translate([0, 0, - 1]) cylinder(d = di1, h = hi1 + 1);
    translate([0, 0, ht - hi2]) cylinder(h = hi2 + 1, d = di2);
}