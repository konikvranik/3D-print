module cell(w,h,d,c,c1) {
  difference() {
    color([1,.9,.7,1])cube([w,h,d]);
    translate([c,c1,c]) cube([w-2*c,h-c-c1,d-2*c]);
    translate([c,-.1,c+c1]) cube([w-2*c,h-c-.1,d-2*c-c1]);
  }
}

module box(w,h,d,c,handle,ts) {
  color([.4,.1,.1,.9]) difference() {
    cube([w,h,d]);
    translate([c,c,c]) cube([w-2*c,h-2*c,d-c+.1]);
  }
  color([.4,.1,.1,.9]) translate([w/2,-handle[1],c+h/2]) {
    translate([0, 5,0]) minkowski() {
      cube(handle, center=true);
      sphere(c);
    };
    minkowski() {
      cube([handle[0]*2,handle[0],handle[2]], center=true);
      sphere(c);
    };
  }
}

module male(step,h,d) {
    union() {
        translate([step/2,0,-d/2]) difference() {
            translate([0,0,0]) rotate([-90,0,0]) cylinder(d=d,h=h,$fn=6);
            translate([-d/2,-1,-d]) cube([d,h+2,d]);
            translate([0,h-d,0]) sphere(d/4);
        }
    }
}

module female(step,h,d) {
    difference() {
        cube([step,h,d/2-c]);
        dist=.15;
        translate([0,-dist-1,d/2]) minkowski() {
            male(step,h+2,d+dist);
            sphere(dist);
        }
    }
}

module connectors(w,h,d,c,size) {
  difference(){
    union() {
      for (y = [0:30:h]) {
        translate([c,0,y+30]) rotate([0,90,0]) male(30,d,6);
        translate([w+c,0,y+30]) rotate([0,90,0]) female(30,d,6.2);
        }
    }
    translate([-d,-c,h+c]) cube([w+2*c+2*d,d+2*c,h+2*c]);
  }
  difference() {
      union(){
          for (x = [0:30:w]) {
            translate([x,0,c]) male(30,d,6);
            translate([x,0,h+c]) female(30,d,6.2);
          }
      }
      translate([w+2*c,-c,-d]) cube([w+2*c,d+2*c,h+2*c+2*d]);
  }
}

module rack(size, w, h, d, c, c1) {
  for (x = [0:size[0]-1]) {
    for (y = [0:size[1]-1]) {
      translate([x*(w-c),0,y*(h-c)]) cell(w,d,h,c,c1);
    }
  }
  connectors(size[0]*(w-c),size[1]*(h-c),d,c,size);
}

module bottom(w,d,c) {
    thick=6.2;
  difference() {
      translate([0,0,-thick/2+c-s]) union(){
          for (x = [0:30:w]) {
            translate([x,0,0]) female(30,d,thick);
          }
      }
      translate([w-2*c,-c,-d]) cube([w+2*c,d+2*c,h+2*c+2*d]);
  }
  translate([0,-d,-thick/2-s]) cube([w,2*d,c]);
}

w = 49;
h = 49;
d = 49;
c = 1;
c1 = .5;
s = .2;

//rack([4,3],w,h,d,c,c1);
translate([c+s,c+s,c+s]) box(w-2*c-2*s,d-2*c-2*s,h-2*c-2*s,c,[1,10,h/3-2*c],6);
//bottom((w)*4,d,c);