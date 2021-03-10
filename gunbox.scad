thick = 10;
plate = [342, 244, 5] - [thick, thick, 0];
h = 67 - 40 + 10 - plate[2];
box = [342, 244, h];
triangle = 7;

difference() {
    cube(box);
    translate([thick, thick, - 1]) cube(box - [2 * thick, 2 * thick, - 2]);

    translate([0, triangle, 0]) rotate([45 + 90, 0, 0]) cube([box[0], 10, h]);
    translate([triangle, 0, 0]) rotate([0, - 45 - 90, 0]) cube([h, box[1], h]);
    translate([0, box[1] - triangle, 0]) rotate([- 45, 0, 0]) cube([box[0], h, h]);
    translate([box[0] - triangle, 0, 0]) rotate([0, 45, 0]) cube([h, box[1], h]);
    translate(box / 2) cube([10, box[1], box[2]], center = true);

    translate([0, 0, box[2] / 2]) rotate([0, 0, 45]) cube([2 * triangle, box[1], box[2] + 1], center = true);
    translate([box[0], 0, box[2] / 2]) rotate([0, 0, - 45])  cube([2 * triangle, box[1], box[2] + 1], center = true);
    translate([box[0], box[1], box[2] / 2]) rotate([0, 0, 45])  cube([2 * triangle, box[1], box[2] + 1], center = true);
    translate([0, box[1], box[2] / 2]) rotate([0, 0, - 45])  cube([2 * triangle, box[1], box[2] + 1], center = true);
}

translate([box[0] + 20, 0, 0]) cube(plate);