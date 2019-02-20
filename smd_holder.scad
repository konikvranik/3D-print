boxes=[["2K2",8,6,50,5],["10K",8,6,50,5],["200K",8,6,50,5],["49K9",8,6,50,5],["100K",8,6,50,5],["diode",8,6,50,5],["NFET",8,6,50,5],["10µF",8,6,50,5],["4K7",8,6,50,5],["NPN",8,6,50,5],["1117",12,6,50,5],["470µF",12,6,50,4],["150µF",12,6,50,4],["µUSB",16,6,50,5]];
border=1;
thickness=1.5;
wall=1;
textplace=15;
parthole=15;
dispenserradius=10;

module body(width, diameter) {
    difference() {
        cube([diameter+2*wall,diameter+2*wall,width+2*wall]);
        union() {
            translate([diameter/2+wall,diameter/2+wall,wall]) cylinder(d=diameter,h=width);
            translate([diameter/2+wall,diameter/2+wall,wall]) cylinder(d=diameter-5,h=width+2*wall);
            translate([diameter/2+wall,wall,wall]) cube([diameter/2+2*wall,diameter/2,width]);
        }
    }
}

module dispenser(text, width, height, diameter, textsize) {
    function inner() = width-2*border;
    union() {
        difference() {
            cube([height+wall,diameter+2*wall,width+2*wall]);
            translate([-1,0,0]) difference() {
                translate([0,0,wall])
                    cube([height+1,diameter+wall-textplace-parthole+4+inner(),width]);
                translate([0,diameter+wall-textplace-parthole+4+inner(),wall])
                    cylinder(r=height,h=width);
            }
            translate([-1,0,wall+border])
                cube([height+1,diameter+2*wall+.1,inner()]);
            translate([height-thickness,0,wall])
                cube([thickness,diameter+2*wall+.1,width]);
            translate([height-.1,diameter+wall-textplace,wall])
                cube([thickness+wall+.2,textplace,width]);
            translate([height-.1,diameter+wall-textplace-parthole,wall])
                cube([thickness+wall+.2,4,width]);
        }
        difference() {
            translate([-dispenserradius+height-thickness,0,wall])
                cube([dispenserradius,diameter+wall-textplace-parthole,width]);
            translate([-dispenserradius+height-thickness-wall,dispenserradius+wall,0])
                cylinder(r=dispenserradius, h=width+2*wall);
            translate([-dispenserradius+height-thickness-wall-1,dispenserradius+wall,0])
                cube([dispenserradius+1,diameter,width+2*wall]);
        }
        translate([height-thickness-wall,diameter+wall-textplace-parthole,wall]) rotate([0,0,-25])
            cube([wall,5.1,width]);
        translate([height+wall,(diameter+wall-textplace-parthole)/2,width/2+wall]) rotate([90,0,90])
            linear_extrude(1) text(text,valign="center", halign="center", size=textsize);
    }
}

module hull(text, width, height, diameter,textsize) {
    body(width,diameter);
    translate([diameter+2*wall,0,0]) dispenser(text, width, height, diameter, textsize);
}

function displace(i) = ( i > 0 ? boxes[i-1][1] + 2*wall + 1 + displace(i-1) : 0 );

rotate([-90,0,180]) {
    for (i=[0:len(boxes)-1]){
        box=boxes[i];
        width=box[1]+.5;
        diameter=box[3]-2*wall;
        translate([0,0,displace(i)]) hull(box[0], width, box[2], diameter, box[4]);
    }
}