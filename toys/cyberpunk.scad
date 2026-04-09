$fs=.1;
$fa=1;
union() {
    rotate([90, 0, 0]) import("Phanteks_HDD_cover_cp2077-v2.stl");
    rotate([0, 180, 0]) linear_extrude(.5) text("In your Steam library", halign="center", valign="center");
}