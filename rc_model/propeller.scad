
$fn=64;
difference() {
union() {
cylinder(d=6,h=5.4);
translate([-4.3,-7.1,0]) scale(v=[.17,.17,.24]) import("/home/hpa/Stažené/Prop.STL");
}
translate([0,0,-.1])cylinder(d=2.5,h=6);
}
