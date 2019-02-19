diameter = 50;
wall=1;
text="2K2";
border=1;
inner=6;
width = 2*border+inner;

module body() {
difference() {
    cube([diameter+2*wall,diameter+2*wall,width+2*wall]);
    union() {
        translate([diameter/2+wall,diameter/2+wall,wall]) cylinder(d=diameter,h=width+2*wall);
        translate([diameter/2+wall,wall,wall]) cube([diameter/2+2*wall,diameter/2,width]);
    }
}
difference() {
    translate([diameter/2+2*wall,diameter/2+2*wall,0]) cylinder(d=diameter,h=width+2*wall);
    translate([diameter/2+wall,diameter/2+wall,wall]) cylinder(d=diameter,h=width+2*wall);
}
}

module dispenser() {
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
            translate([0,0,wall]) cube([inner-border,diameter/2-5,width]);
            translate([0,inner-border-1+wall,wall]) cylinder(r=inner-border-1, h=width+2*wall);
            translate([-1,inner-border-1+wall,wall]) cube([inner-border,diameter/2-5,width]);
        }
        translate([inner+wall,(diameter+wall-20-15)/2,width/2+wall]) rotate([90,0,90]) linear_extrude(2) text(text,valign="center", halign="center", size=6);
    }
}

body();

translate([diameter+2*wall,0,0]) dispenser();