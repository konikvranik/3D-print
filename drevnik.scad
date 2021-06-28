x = 0;
y = 1;
z = 2;

w = 3000;
d = 800;
h = 2000-100;

hranol = [0, 45, 70];

// krajní podložky
translate([hranol[1], 0, 0])
    pricka(d);
translate([w - hranol[1] + hranol[1], 0, 0])
    pricka(d);

// prostřední podložky
for (i = [(w - hranol[1]) / 6:(w - hranol[1]) / 6:w - 4 * hranol[1]]) {
    translate([i + hranol[1], hranol[z], 0])
        pricka(d - 2 * hranol[z]);
}

// podlaha
translate([0, hranol[z], hranol[z]])
    for (i = [0:(d - hranol[y] - 2 * hranol[z]) / 3:d - hranol[y]]) {
        translate([0, i, 0])
            hranol(w);
    }

// sloupky
translate([0, 0, hranol[z]]) {

    sloupek(h + 100);
    translate([w - hranol[y], 0, 0]) sloupek(h + 100);

    translate([w - hranol[y], (d - hranol[y] - 2 * hranol[z]) / 3, 0]) sloupek(h + 70);
    translate([0, (d - hranol[y] - 2 * hranol[z]) / 3, 0]) sloupek(h + 70);

    translate([w - hranol[y], d - (d - hranol[y] - 2 * hranol[z]) / 3 - hranol[z], 0]) sloupek(h + 30);
    translate([0, d - (d - hranol[y] - 2 * hranol[z]) / 3 - hranol[z], 0]) sloupek(h + 30);

    translate([w - hranol[y], d - hranol[z], 0]) sloupek(h);
    translate([0, d - hranol[z], 0]) sloupek(h);

}

// střecha
translate([0, d + 50, h + hranol[z] - 30])
    rotate([- 8, 0, 0]) {
        rotate([0, 0, - 90])
            hranol(d + 150);
        translate([w - hranol[y], 0, 0])
            rotate([0, 0, - 90])
                hranol(d + 150);
        translate([hranol[y], - d - 150, 0])
            hranol(w - 2 * hranol[y]);
        translate([hranol[y], - hranol[y], 0])
            hranol(w - 2 * hranol[y]);
        translate([0, - d - 150, hranol[z]]) osb([w, d + 150]);

    }

module pricka(d) {
    rotate([0, 0, 90])
        hranol(d);
}

module sloupek(l) {
    rotate([- 90, - 90, 0])
        hranol(l);
}

module hranol(l) {
    cube(hranol + [l, 0, 0]);
    echo("hranol", l);
}

module osb(s) {
    cube([s[0], s[1], 8]);
    echo("osb", s);
}