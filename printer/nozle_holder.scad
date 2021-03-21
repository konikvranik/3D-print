dia = 5.8;
depth = 6;
thick=1;
count = 3;
sizes = ["0,2", "0,25","0,3","0,4","0,5","0,6","0,8","1"];
cell=10;
textspace = 15;
$fn=64;

difference() {
cube([cell*count + textspace, len(sizes)*cell , depth + thick]);
    for(y=[1:cell:len(sizes)*cell]){
        translate([textspace+1,y+(cell-dia)/2,depth+thick-2]) linear_extrude(3) text(sizes[y/cell],size=dia, halign="right");
        for(x=[1:cell:count*cell]){
            translate([textspace+x+cell/2,y+cell/2,thick]) cylinder(d=dia,h=depth+1);
        }
    }    
}