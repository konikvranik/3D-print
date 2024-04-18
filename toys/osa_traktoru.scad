$fn=64;
cylinder(d=7,h=30);
translate([0,0,30])cylinder(d1=7,d2=4,h=10);
for (i=[20:1:30]){
    translate([0,0,i])cylinder(d=8.5,h=.4);
}
difference(){
sphere(d=12);
    translate([-20,-20,0])cube([40,40,50]);
}