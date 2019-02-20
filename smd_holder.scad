wall=1;
diameter = 50-2*wall;
//text=["2K2","10K","200K","49.9K","100K","diode","uni-T","10µF","4K7","NPN"];
text=["NPN"];
textsize=5;
border=1.5;
inner=6;
width = 2*border+inner;
textplace=15;
parthole=15;
dispenserradius=10;

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
                translate([0,0,wall]) cube([inner+1,diameter+wall-textplace-parthole+4+inner,width]);
                translate([0,diameter+wall-textplace-parthole+4+inner,wall]) cylinder(r=inner,h=width);
            }
            translate([-1,0,wall+border]) cube([inner+1,diameter+2*wall+.1,inner]);
            translate([inner-border,0,wall]) cube([border,diameter+2*wall+.1,width]);
            translate([inner-.1,diameter+wall-textplace,wall]) cube([border+wall+.2,textplace,width]);
            translate([inner-.1,diameter+wall-textplace-parthole,wall]) cube([border+wall+.2,4,width]);
        }
        difference() {
            translate([-dispenserradius,0,wall])
                cube([dispenserradius+inner-border,diameter+wall-textplace-parthole,width]);
            translate([-dispenserradius+inner-border-wall,dispenserradius+wall,0])
                cylinder(r=dispenserradius, h=width+2*wall);
            translate([-dispenserradius+inner-border-wall-1,dispenserradius+wall,0])
                cube([dispenserradius+1,diameter,width+2*wall]);
        }
        translate([inner-border-wall,diameter+wall-textplace-parthole,wall]) rotate([0,0,-25])
            cube([wall,5.1,width]);
        translate([inner+wall,(diameter+wall-textplace-parthole)/2,width/2+wall]) rotate([90,0,90])
            linear_extrude(1) text(text,valign="center", halign="center", size=textsize);
    }
}

module hull(text) {
body();

translate([diameter+2*wall,0,0]) dispenser(text);
}

rotate([-90,0,180]) {
    for (i=[0:len(text)-1]){
        translate([0,0,i*(width + 2*wall + 1)]) hull(text[i]);
    }
}