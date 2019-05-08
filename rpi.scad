thickness = 3;
width=58+7;
height=55+1;
pcb=2;
border=2;
hole=5;
strip=1.5;
space=25;
$fn=64;

module bar() {
    difference() {
        union() {
            translate([3.5,0,hole+2+1.5]) sphere(d=3);
            translate([3.5,3.5,0]) {
                translate([0,0,hole]) sphere(d=2.75);
                translate([0,0,0]) cylinder(d=7, h=hole);
                
            }
            translate([0,-thickness,0]) {
                cube([7,3.5+thickness,hole]);
                cube([7,thickness,space-thickness]);
            }
        }
        translate([0,-thickness-1,-2*thickness-1]) cube([9,8+thickness+1,2*thickness+1]);
    }
}

module bar2() {
    translate([0,thickness,thickness]) {
        bar();
        translate([0,height,0]) mirror([0,1,0]) bar();
    }
    translate([0,0,space]) cube([7,height+2*thickness,thickness]);
}

module cover() {
    bar2();
}

module joins() {
    translate([7,thickness/2,thickness/2]) {
            sphere(d=thickness/2);
            translate([0,height+thickness,0]) sphere(d=thickness/2);
        }
        translate([width-7,thickness/2,thickness/2]){
            sphere(d=thickness/2);
            translate([0,height+thickness,0]) sphere(d=thickness/2);
        }
}

module frame() {
    difference() {
        translate([7,0,0]) {
            cube([width-14,thickness,thickness+hole]);
            translate([0,height+thickness,0]) cube([width-14,thickness,2*thickness]);
        }
        joins();
    }
    
    translate([0,0,space+.2]) joins();
    
    translate([7,0,0]) mirror([1,0,0]) cover();
    translate([58,0,0]) cover();
}

difference() {
    frame();
}