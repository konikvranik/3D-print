width = 8;
height=6;
border=1;
thickness=1.5;
box_size=50;
//text=["2K2","10K","200K","49.9K","100K","diode","uni-T","10µF","4K7","NPN"];
text=["NPN"];
textsize=5;
wall=1;

diameter = box_size-2*wall;
space=.2;
textplace=15;
parthole=15;
dispenserradius=10;

function width() = width+2*space;
function inner() = width()-2*border;

module body() {
difference() {
    cube([diameter+2*wall,diameter+2*wall,width()+2*wall]);
    union() {
        translate([diameter/2+wall,diameter/2+wall,wall]) cylinder(d=diameter,h=width());
        translate([diameter/2+wall,diameter/2+wall,wall]) cylinder(d=diameter-5,h=width()+2*wall);
        translate([diameter/2+wall,wall,wall]) cube([diameter/2+2*wall,diameter/2,width()]);
    }
}
}

module dispenser(text) {
    union() {
        difference() {
            cube([height+wall,diameter+2*wall,width()+2*wall]);
            translate([-1,0,0]) difference() {
                translate([0,0,wall])
                    cube([height+1,diameter+wall-textplace-parthole+4+inner(),width()]);
                translate([0,diameter+wall-textplace-parthole+4+inner(),wall])
                    cylinder(r=height,h=width());
            }
            translate([-1,0,wall+border])
                cube([height+1,diameter+2*wall+.1,inner()]);
            translate([height-thickness,0,wall])
                cube([thickness,diameter+2*wall+.1,width()]);
            translate([height-.1,diameter+wall-textplace,wall])
                cube([thickness+wall+.2,textplace,width()]);
            translate([height-.1,diameter+wall-textplace-parthole,wall])
                cube([thickness+wall+.2,4,width()]);
        }
        difference() {
            translate([-dispenserradius+height-thickness,0,wall])
                cube([dispenserradius,diameter+wall-textplace-parthole,width()]);
            translate([-dispenserradius+height-thickness-wall,dispenserradius+wall,0])
                cylinder(r=dispenserradius, h=width()+2*wall);
            translate([-dispenserradius+height-thickness-wall-1,dispenserradius+wall,0])
                cube([dispenserradius+1,diameter,width()+2*wall]);
        }
        translate([height-thickness-wall,diameter+wall-textplace-parthole,wall]) rotate([0,0,-25])
            cube([wall,5.1,width()]);
        translate([height+wall,(diameter+wall-textplace-parthole)/2,width()/2+wall]) rotate([90,0,90])
            linear_extrude(1) text(text,valign="center", halign="center", size=textsize);
    }
}

module hull(text) {
    body();
    translate([diameter+2*wall,0,0]) dispenser(text);
}

rotate([-90,0,180]) {
    for (i=[0:len(text)-1]){
        translate([0,0,i*(width() + 2*wall + 1)]) hull(text[i]);
    }
}