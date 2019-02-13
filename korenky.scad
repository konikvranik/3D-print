module cell(w,h,d,c,c1) {
  difference() {
    cube([w,h,d]);
    translate([c,c1,c]) cube([w-2*c,h-c-c1,d-2*c]);
    translate([c,-.1,c+c1]) cube([w-2*c,h-c-.1,d-2*c-c1]);
  }
}

module box(w,h,d,c) {
  difference() {
    cube([w,h,d]);
    translate([c,c,c]) cube([w-2*c,h-2*c,d-c+.1]);
  }
}

w = 49;
h = 49;
d = 49;
c = 1;
c1 = .5;
s = .2;

cell(w,h,d,c,c1);

translate([c+s,-h+c,0]) box(w-2*c-2*s,w-2*c-2*s,w-2*c-2*s,c);