width = 50;
maxdiameter = 200;
thickness = 5;
wirethickness = 5/sin(45);

length=sqrt(2*(maxdiameter/2*maxdiameter/2));

rotate([45]) {
  difference() {
    cube([width + 2*thickness, maxdiameter/2, maxdiameter/2]);
    translate([thickness,thickness,thickness]) cube([width, maxdiameter/2, maxdiameter/2]);
    translate([thickness,-1,thickness]) cube([width, thickness+2, wirethickness]);
  }
}

translate([0,-length/2,0]) difference() {
  cube([width+2*thickness,length,2*thickness]);
  translate([thickness,thickness,thickness]) cube([width,length-2*thickness,thickness+1]);
}

cube([thickness,length/2,length/2]);
translate([width+thickness,0,0]) cube([thickness,length/2,length/2]);

translate([thickness,-3*wirethickness,thickness]) difference() {
  rotate([-180-45]) cube([width,thickness,thickness/2]);
  translate([0,-thickness-thickness/2,0]) cube([width,thickness,thickness]);
}