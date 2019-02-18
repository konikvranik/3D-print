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

module male(h,w,d) {
    translate([h/2,0,-d/2]) difference() {
        translate([0,0,0]) rotate([-90,0,0]) cylinder(d=d,h=w);
        translate([-d/2,-1,-d]) cube([d,w+2,d]);
    }
}

module female(h,w,d) {
    difference() {
        cube([h,w,d/2-c]);
        translate([0,-1,d/2]) male(h+2,w+2,d+.2);
    }
}

module rack(size, w, h, d, c, c1) {
  for (x = [0:size[0]-1]) {
    for (y = [0:size[1]-1]) {
      translate([x*(w-c),0,y*(h-c)]) cell(w,d,h,c,c1);
    }
    translate([x*(w-c),0,c]) male(w,d,6);
    translate([x*(w-c),0,(size[1]*(h-c))+c]) female(w,d,6.2);
  }
  for (y = [0:size[1]-1]) {
    translate([c,0,h+y*(h-c)]) rotate([0,90,0]) male(h,d,6);
    translate([(size[0]*(w-c))+c,0,h+y*(h-c)]) rotate([0,90,0]) female(h,d,6.2);
  }
}

w = 49;
h = 49;
d = 49;
c = 1;
c1 = .5;
s = .2;

rack([4,3],w,h,d,c,c1);

translate([c+s,-h+c,0]) box(w-2*c-2*s,d-2*c-2*s,h-2*c-2*s,c,[1,10,h/3-2*c],6);
