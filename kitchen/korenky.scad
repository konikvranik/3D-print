module cell(w,h,d,c,c1) {
  difference() {
    cube([w,h,d]);
    translate([c,c1,c]) cube([w-2*c,h-c-c1,d-2*c]);
    translate([c,-.1,c+c1]) cube([w-2*c,h-c-.1,d-2*c-c1]);
  }
}

module box(t,w,h,d,c,handle,ts) {
  difference() {
    cube([w,h,d]);
    translate([c,c,c]) cube([w-2*c,h-2*c,d-c+.1]);
  }
  translate([w/2,-handle[1],30]) {
    translate([0,0,handle[2]/2+c]) rotate([90,0,0]) { linear_extrude(3) text(t,halign="center", valign="top", language="cs", script="utf8", size=ts); };
    translate([0, 10,0]) minkowski() {
      cube(handle, center=true);
      sphere(c);
    };
  }
}

module rack(size, w, h, c, c1) {
  for (x = [0:size[0]-1]) {
    for (y = [0:size[1]-1]) {
      translate([x*(w-c),0,y*(h-c),]) cell(w,h,d,c,c1);
    }
  }
}

w = 49;
h = 49;
d = 49;
c = 1;
c1 = .5;
s = .2;

rack([4,3],w,h,c,c1);

koreni = ["pepř", "bobkový list"];
i=0;
for (i = [0: len(koreni)-1]) {
  translate([c+s+w*i,-h+c,0]) box(koreni[i], w-2*c-2*s,w-2*c-2*s,w-2*c-2*s,c,[40,20,4],6);
};
