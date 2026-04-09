d=28.5;
h=7;
di=15.5;

difference() {
union() {
    cylinder(d1=d,d2=d+3, h= 2);
    translate([0,0,2]) cylinder(d2=d,d1=d+3, h= 1);
    translate([0,0,3]) cylinder(d=d, h= h);
    translate([0,0,3+h]) cylinder(d1=d+2*4,d2=d+4, h= 10);
}
translate([0,0,-1])cylinder(d=di,h=h+3+10+2);
cube([.5,50,50]);
}