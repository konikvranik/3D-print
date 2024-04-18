$fa=.1;
$fs=.2;

difference() {
    cylinder(h=40, d=47, $fn=6);

    cylinder(h=4, d=45-2.15*2, $fn=6);
    translate([0,0,3.3]) cylinder(h=7.7, d=45-1.15*2, $fn=6);
    translate([0,0,-1]) cylinder(h=42, d=45-2.45*2, $fn=6);
    for(i=[30:60:330]) rotate([0,0,i]) translate([-4.5,0,-1]) cube([9,50,i==90?25:12]);
    
    
}

translate([0,0,24]){
    for(i=[30:60:330]) rotate([0,0,i]) translate([19,0,0]) difference() {
        cylinder(h=16,d=8);
        translate([0,-10,-1]) cube(50);
    }
}

difference() {
    translate([-25,-9,25]) cube([78,18,15]);
    translate([-9,-9,24]) cube(18);
}