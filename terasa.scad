strecha = 2200;

module hranol45x75(l=3000) {
    // hranol hoblovaný: https://www.hornbach.cz/shop/Hranol-hoblovany-45-x-75-x-3000-mm-smrk/5052074/artikl.html
cube([45,l,75]);
    }

module prkno27x143(l=3000){
    // modřín sibiřský: https://www.hornbach.cz/shop/Terasove-prkno-27-x-143-mm-modrin-sibirsky-3000-mm/6281498/artikl.html
    difference() {
    cube([l,143,27]);
        for(i=[0:7:140]) {
            translate([0,i,-1]) cube([l,3,4]);
            translate([0,i,24]) cube([l,3,4]);
        }
    }
}

module prkno19x115(l=3000){
    cube([l,19,115]);
}

translate([45,0,0]) hranol45x75();
translate([1500,0,0]) hranol45x75();
translate([3000-2*45,0,0]) hranol45x75();
translate([0,0,75]){
    for(i=[75:150:3000-70]) {
    translate([0,i,0]) prkno27x143();
    }
}

translate([0,75,-700]) rotate([90,0,0])  {
    h=2200+700+70+27+115;
    hranol45x75(h);
    translate([1500-45,0,0]) hranol45x75(900+700);
    translate([3000-45,0,0]) hranol45x75(h);
}

translate([0,2000,0]) rotate([90,0,0])  {
    h=2200+70+27+115;
    hranol45x75(h);
    translate([3000-45,0,0]) hranol45x75(h);
}


translate([0,75,900+45]) rotate([0,90,-90]) hranol45x75();
translate([0,75+24,300]) rotate([90,0,0]) prkno27x143();

translate([0,0,900]) rotate([-35,0,0]) hranol45x75(1600);
translate([3000-45,0,900]) rotate([-35,0,0]) hranol45x75(1600);

translate([0,-900,70+27+2200]) {
    rotate([0,0,90]) prkno19x115();
    translate([3000+19,0,0]) rotate([0,0,90]) prkno19x115();
    for(i=[0:250:3000]){
        translate([0,i,0]) prkno19x115();
    }
}