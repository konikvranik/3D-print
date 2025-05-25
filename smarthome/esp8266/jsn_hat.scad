angle = 75;
diameter = 21.5;
outer_diameter = 23.25;
depth = 17.5;
upper_dia = 6.35;
upper_height = 2;
cable = 3;
ring = [24.15 + .5, 1];
height = 18.5 + 10;
displacement = 6;
total_height = 60;
total_diameter = 30;
offs = 10;

dive = 30;
$fs = .2;
$fa = 1;
module sensor() {
    cylinder(h = offs + height, d = (diameter + outer_diameter) / 2);
    cylinder(h = offs + ring[1], d = ring[0]);
    translate([displacement, 0, offs + height]) {
        cylinder(h = upper_height, d = upper_dia);
    }
}

module inner() {
    sensor();
    translate([- total_height / 2, - total_height / 2, - total_height])cube([total_height, total_height,
        total_height]);
    translate([displacement, 0, offs + height + upper_height]) rotate([0, - 15, 0]) cylinder(d = cable, h =
    total_height);
    translate([0, - (cable - 1) / 2, 0]) cube([total_height, cable * .65, 2 * total_height]);
}

module complete() {
    difference() {
        translate([0, 0, (total_height - dive) / 2]) scale([total_diameter / (total_height + dive), total_diameter / (
            total_height + dive)
            , 1]) sphere(d = total_height + dive);
        inner();
    }
}

complete();