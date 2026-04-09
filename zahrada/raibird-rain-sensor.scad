lower_d = 30;
lower_h = 25;
hrdlo_d = 15.4;
hrdlo_h=5;
inner = 11;
diameter = 140;
$fn = 64;

module trychtyr() {
difference() {
    cylinder(d1 = lower_d,d2=diameter, h=100);
    translate([0,0,-1]) cylinder(d=lower_d, h=lower_h+1);
    translate([0,0,lower_h-1]) cylinder(d=hrdlo_d, h=hrdlo_h+1);
    translate([0,0,lower_h+hrdlo_h-1]) cylinder(d=inner, h=hrdlo_h+1);
    translate([0,0,lower_h+hrdlo_h+1])  cylinder(d1 = inner, d2=diameter-2, h=100-lower_h-hrdlo_h+2);
}
}

module korekce() {
    difference() {
        cylinder(d1=inner+2, d2=20.8,h=10);
        translate([0,0,-.1]) cylinder(d1=inner, d2=19,h=12);
    }
}

//trychtyr();
korekce();