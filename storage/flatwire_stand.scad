wire=1.7;
connector=2.5;

height=200;

capacity = 20;

count=30;

distance = 5;

peggheight = 4;
    
wall = 2.5;

backside= height*4/6+wall;
backhole=backside/2;
bottom=max(100,(capacity * connector));
$fn = 16;

module pegg() {
    diameter=connector+.9;
    cube([distance/2, capacity * connector, peggheight]);
    translate([distance/2-connector/2, capacity * connector, 0]) difference() {
        cylinder(d=diameter, h=10);
        translate([-diameter/2, -diameter/2, peggheight]) rotate([45,0,0]) cube([diameter+2,2*diameter+2, 20]);
    }
}

module array(count) {
    for(i = [0:count]) {
        translate([i * (wire+distance), 0, 0]) {
            if(i<count) pegg();
            if(i>0) mirror([1,0,0]) pegg();
        }
    }
}

module sidewall() {
translate([0, -wall, 0]) cube([wall, (capacity * connector)+wall, height+wall]);
}

module floor() {
    cube([(count)*(wire+distance)+2*wall,bottom,wall]);
}

module stand() {
    translate([wall,0,height-peggheight+wall]) array(count);
    sidewall();
    translate([(count)*(wire+distance)+wall,0,0]) sidewall();
    translate([0,-wall,0]) difference() {
        cube([(count)*(wire+distance)+2*wall,bottom,wall+5]);
        translate([wall,wall,wall]) cube([(count)*(wire+distance),bottom-2*wall,wall+5]);
    }

    translate([0,-wall,height+wall-backside]) {
        difference() {
            cube([(count)*(wire+distance)+wall*2,wall,backside]);
            translate([0,-wall/2,backside/4]) cube([(count)*(wire+distance)+wall*2,2*wall,backhole]);
        }
    }
}

module shelve() {
    sh = (backside-backhole)/2;
    height = height+wall-backside + sh;
    s=.15;
    translate([wall,s/2,height+wall]) {
        translate([0,0,-peggheight]) array(10);
        translate([0,-2*wall-s,-sh-wall]) difference() {
            cube([10*(wire+distance),3*wall+s,sh+wall]);
            translate([-1,wall,-wall]) cube([10*(wire+distance)+2,wall+s,sh+wall]);
        }
    }
}

//stand();

shelve();