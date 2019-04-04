
tablet_width=263;
height=178;
thick=11;
width=100;
distance=50;



translate([0,height+distance,0]) {
    difference() {
        cube([width,5,50]);
        translate([15,0,25]) rotate([-90,0,0]) cylinder(d=4,h=10,center=true);
        translate([width/2,0,37]) rotate([-90,0,0]) cylinder(d=4,h=10,center=true);
        translate([width-15,0,25]) rotate([-90,0,0]) cylinder(d=4,h=10,center=true);
   }
}
difference() {
    translate([0,-5,-5]) cube([width,height+10+distance, thick+10]);
    translate([-(tablet_width-width)/2,5,0]) cube([tablet_width,height-10, thick+10]);
    union(){
        translate([-1,0,0])cube([width+2,height,thick]);
        translate([(width-27)/2, -23, 1]) cube([27,24,8]);
    }
}