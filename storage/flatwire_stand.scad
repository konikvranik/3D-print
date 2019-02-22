wire=1.5;
connector=2.5;

height=200;

capacity = 20;

count=30;

distance = 7.5;

peggheight = 4;
    
wall = 2.5;

backside= height;
bottom=max(100,(capacity * connector));
$fn = 32;

module pegg() {
    diameter=connector+.2;
    cube([distance/2, capacity * connector, peggheight]);
    translate([distance/2-connector/2, capacity * connector, 0]) difference() {
        cylinder(d=diameter, h=10);
        translate([-diameter/2, -diameter/2, peggheight]) rotate([45,0,0]) cube([diameter+2,2*diameter+2, 20]);
    }
}

module array() {
    for(i = [0:count]) {
        translate([i * (wire+distance), 0, 0]) {
            if(i<count)    pegg();
            if(i>0) mirror([1,0,0]) pegg();
        }
    }
}

module sidewall() {
cube([wall, (capacity * connector), height+wall]);
}

module floor() {
    cube([(count)*(wire+distance)+2*wall,bottom,wall]);
}



translate([wall,0,height-peggheight+wall]) array();
sidewall();
translate([(count)*(wire+distance)+wall,0,0]) sidewall();
difference() {
    cube([(count)*(wire+distance)+2*wall,bottom,wall+5]);
    translate([wall,wall,wall]) cube([(count)*(wire+distance),bottom-2*wall,wall+5]);
}

translate([0,-wall,height+wall-backside]) {
    difference() {
        cube([(count)*(wire+distance)+wall*2,wall,backside]);
        translate([0,-wall/2,backside/4]) cube([(count)*(wire+distance)+wall*2,2*wall,backside/2]);
    }
}