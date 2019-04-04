thickness = 3;
width=58+7;
height=55;
pcb=1;
border=1;
hole=5;
strip=1.5;
$fn=64;

module bar() {
    translate([3.5,3.5,hole]) {
        sphere(d=2.75);
        translate([0,0,-thickness-hole]) {
            cylinder(d=7, h=thickness+hole);
        }
    }
    translate([0,-thickness,-thickness]) cube([7,3.5+thickness,thickness+hole]);
}

module bar2() {
    translate([0,thickness,thickness]) {
        bar();
        translate([0,height,0]) mirror([0,1,0]) bar();
    }
}

module cover() {
    difference() {
        bar2();
        translate([3.5,-1,0]) cube([3.5+1,height+2*thickness+2*border+2,thickness]);
    }
   // cube([7,height+2*thickness,thickness]);
    translate([0,thickness+border,-strip]) difference() {
        cube([3.5+border,height-2*border,thickness+strip]);
        translate([3.5, -1, strip]) cube([7,height-2*border+2,thickness]);
    }
    translate([0,0,hole+thickness+pcb]) difference() {
        cube([7,height+2*thickness,15-pcb]);
        translate([-1,thickness+border,-1]) {
            cube([7+2,height-2*border,15-pcb-thickness+1]);
        }
        translate([-1,-1,15-pcb-thickness]) cube([3.5+1,height+2*thickness+2,15-pcb+2]);
        
    }
}

module frame() {
    difference() {
        translate([0,0,hole]) cube([width,height+2*thickness,pcb+2*thickness]);
        translate([-border,thickness,thickness+hole]) {
            cube([width+2*border,height,pcb]);
            translate([7+border,-thickness-border-1,0]) cube([width-2*7,thickness+border+3,thickness+2]);
            translate([7+border,-thickness-1,-2]) cube([width-2*7,thickness+1,thickness+2]);
        }
        translate([-border,thickness+border,thickness-hole]) cube([width+2*border,height-2*border,hole+100]);
        
    }

    translate([7,0,0]) mirror([1,0,0]) cover();
    translate([58,0,0]) {
        cover();
    }

}

frame();