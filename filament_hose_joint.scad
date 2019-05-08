hose=6.5;
printer=8.3;
thickness=1;
hose_length=10;
printer_length=10;
string=4;

$fn=64;

module drill(height) {
    translate([0,0,-1]) cylinder(d=hose,h=height+1);
    translate([0,0,height]) cylinder(d1=hose,d2=string,h=thickness);
    cylinder(d=string,h=height+thickness+1);
}

difference() {
    cylinder(d=printer+2*thickness,h=printer_length+hose_length);
    translate([0,0,hose_length+thickness]) cylinder(d=printer,h=printer_length+1);
    drill(hose_length);
}

translate ([printer+hose,0,0]) difference() {
    cylinder(d=hose+2*thickness,h=2*hose_length+thickness);
    translate([0,0,hose_length+thickness]) cylinder(d=hose,h=hose_length+1);
    drill(hose_length);
}


