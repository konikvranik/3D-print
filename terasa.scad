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
    // Balkonové prkno: https://www.hornbach.cz/shop/Balkonove-prkno-profilovane-19-x-115-x-3000-mm-smrk/5195909/artikl.html
    cube([l,19,115]);
}

module man() {
    translate([100,-1200,1100]) rotate([50,0,0]) scale(v=[12,12,12]) import("/home/hpa/Stažené/gary.stl", convexity=5);

}

module terasa() {
    module podlaha() {
        translate([45,0,0]) hranol45x75();
        translate([1500,0,0]) hranol45x75();
        translate([3000-2*45,0,0]) hranol45x75();
        translate([0,0,75]){
            for(i=[75:150:3000-70]) {
            translate([0,i,0]) prkno27x143();
            }
        }
    }

    module zabradli() {
        down=900;
        translate([0,75,-down]) rotate([90,0,0])  {
            h=2200+down+70+27+115;
            hranol45x75(h);
            translate([1500-45,0,0]) hranol45x75(900+down);
            translate([3000-45,0,0]) hranol45x75(h);
        }

        translate([0,2000,0]) rotate([90,0,0])  {
            h=2200+70+27+115;
            hranol45x75(h);
            translate([3000-45,0,0]) hranol45x75(h);
        }


        translate([0,75,900+45]) rotate([0,90,-90]) hranol45x75();
        translate([0,75+24,300]) rotate([90,0,0]) prkno27x143();

        translate([45,0,300+143]) rotate([90,0,90]) prkno27x143(2000);
        translate([3000-45-27,0,300+143]) rotate([90,0,90]) prkno27x143(2000);


        translate([0,0,900]) rotate([-35,0,0]) hranol45x75(1600);
        translate([3000-45,0,900]) rotate([-35,0,0]) hranol45x75(1600);

    }

    module strecha() {
        translate([0,-900,70+27+2200]) {
            rotate([0,0,90]) prkno19x115();
            translate([3000+19,0,0]) rotate([0,0,90]) prkno19x115();
            for(i=[0:330:3000]){
                translate([0,i,0]) prkno19x115();
            }
        }
    }
    podlaha();
    zabradli();
    strecha();
    translate([1500,300,75+27]) man();

}

module teren() {
    s=800;

// výška schodů = 1200
// délka schodů = 1700
// schody ode zdi: 1500, 2700
// celkem = 7500


//500 3000
    //2300 
    translate([0,0,-1100]) {
        translate([-300,0,0]) cube([300,5200,5000]);
        translate([-10,1400,00])cube([7500,3800,1100]);
        difference() {
            translate([0,0,0])cube([7500,1400,1100]);
            translate([-1,0,0]) rotate([38,0,0])cube([7502,3500,7000]);
        }
        translate([0,1400+3500,0]) difference() {
            cube([4700,300,5000]);
            translate([500,-1,1100+1200]) cube([3000,302,2300]);
        }
    }
    translate([1500,1400+3500-1700,0]) {
        difference() {
            cube([2700-1500, 1700, 1200]);
            translate([-1,0,0]) rotate([40,0,0]) cube([2700-1500+2, 3700, 1200]);
        }
    }
}

translate([7500-3000-800,200,0]) terasa();

teren();