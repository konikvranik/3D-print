diameter = 40;
wall=1;
text=["2K2","3K3"];
border=1;
inner=6.2;
width = 2*border+inner;

module body() {
difference() {
    cube([diameter+2*wall,diameter+2*wall,width+2*wall]);
    union() {
        translate([diameter/2+wall,diameter/2+wall,wall]) cylinder(d=diameter,h=width);
        translate([diameter/2+wall,diameter/2+wall,wall]) cylinder(d=diameter-5,h=width+2*wall);
        translate([diameter/2+wall,wall,wall]) cube([diameter/2+2*wall,diameter/2,width]);
    }
}
}

module dispenser(text) {
    union() {
        difference() {
            cube([inner+wall,diameter+2*wall,width+2*wall]);
            translate([-1,0,0]) difference() {
                translate([0,0,wall]) cube([inner+1,diameter/2+wall,width]);
                translate([0,diameter/2+wall,wall]) cylinder(r=inner,h=width);
            }
            translate([-1,0,wall+border]) cube([inner+1,diameter+2*wall+.1,inner]);
            translate([inner-border,0,wall]) cube([border,diameter+2*wall+.1,width]);
            translate([inner-.1,diameter+wall-20,wall]) cube([border+wall+.2,20,width]);
            translate([inner-.1,diameter+wall-20-15,wall]) cube([border+wall+.2,4,width]);
        }
        difference() {
            translate([0,0,wall]) cube([inner-border,diameter+wall-20-15,width]);
            translate([0,inner-border-1+wall,wall]) cylinder(r=inner-border-1, h=width+2*wall);
            translate([-1,inner-border-1+wall,wall]) cube([inner-border,diameter/2-5,width]);
        }
        translate([inner-border-wall,diameter+wall-20-15,wall]) rotate([0,0,-25]) cube([wall,5.1,width]);
        translate([inner+wall,(diameter+wall-20-15)/2,width/2+wall]) rotate([90,-90,90]) linear_extrude(1) text(text,valign="center", halign="center", size=4);
    }
}

module hull(text) {
body();

translate([diameter+2*wall,0,0]) dispenser(text);
}

rotate([-90,0,0]) {
    for (i=[0:len(text)-1]){
        translate([0,0,i*(width + 2*wall + 1)]) hull(text[i]);
    }
}