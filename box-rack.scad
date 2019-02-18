module cell(w,h,d,c,c1) {
  difference() {
    color([1,.9,.7,1])cube([w,h,d]);
    translate([c,c1,c]) cube([w-2*c,h-c-c1,d-2*c]);
    translate([c,-.1,c+c1]) cube([w-2*c,h-c-.1,d-2*c-c1]);
  }
}

module box(t,w,h,d,c,handle,ts) {
  color([.4,.1,.1,.9]) difference() {
    cube([w,h,d]);
    translate([c,c,c]) cube([w-2*c,h-2*c,d-c+.1]);
  }
  color([.4,.1,.1,.9]) translate([w/2,-handle[1],30]) {
    translate([0,0,handle[2]/2+c]) rotate([90,0,0]) { linear_extrude(3) text(t,halign="center", valign="top", language="cs", script="utf8", size=ts); };
    translate([0, 10,-5]) minkowski() {
      cube(handle, center=true);
      sphere(c);
    };
    translate([0, 0,-5]) minkowski() {
      cube([handle[0]*2,handle[1]/10,handle[2]], center=true);
      sphere(c);
    };
  }
}

module male(h,d) {
    translate([h/2,0,-d/2]) difference() {
        translate([0,0,0]) rotate([-90,0,0]) cylinder(d=d,h=h);
        translate([-d/2,-1,-d]) cube([d,h+2,d]);
    }
}

module female(h,d) {
    difference() {
        cube([h,h,d/2-c]);
        translate([0,-1,d/2]) male(h+2,d+.2);
    }
}

module rack(size, w, h, c, c1) {
  for (x = [0:size[0]-1]) {
    for (y = [0:size[1]-1]) {
      translate([x*(w-c),0,y*(h-c)]) cell(w,h,d,c,c1);
    }
    translate([x*(w-c),0,c]) male(w,6);
    translate([x*(w-c),0,(size[1]*(h-c))+c]) female(w,6.2);
  }
  for (y = [0:size[1]-1]) {
    translate([c,0,h+y*(h-c)]) rotate([0,90,0]) male(h,6);
    translate([(size[0]*(w-c))+c,0,h+y*(h-c)]) rotate([0,90,0]) female(h,6.2);
  }
}

w = 49;
h = 49;
d = 49;
c = 1;
c1 = .5;
s = .2;

rack([4,3],w,h,c,c1);

koreni = [""];
i=0;
for (i = [0: len(koreni)-1]) {
  translate([c+s+w*i,-h+c,0]) box(koreni[i], w-2*c-2*s,w-2*c-2*s,w-2*c-2*s,c,[4,20,40],6);
};
