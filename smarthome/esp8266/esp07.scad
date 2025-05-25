inner_width=47;
inner_height=40;
inner_depth=40;
thick=1.5;
wavgat_x = 41.5;
wavgat_y = 28.5;
wavgat_z = 11.5;
wavgat_d = 1.2;
esp_x = 35;
esp_y = 40-18.5;


module inner(d=0) {
    translate([-d,inner_height - esp_y-d,0]) cube([esp_x +2*d, esp_y+2*d, inner_depth +2*thick+1]);
    translate([inner_width - wavgat_x-d,wavgat_y-1-d,0]) cube([esp_x-inner_width + wavgat_x+2*d , inner_height -wavgat_y+2*d, inner_depth +2*thick+1]);
    translate([inner_width - wavgat_x+.5-d,.5-d,0]) cube([wavgat_x-1+2*d , wavgat_y-1+2*d, wavgat_z]);
    translate([inner_width - wavgat_x-d,-d,wavgat_z-wavgat_d]) cube([wavgat_x+2*d , wavgat_y+2*d, inner_depth +2*thick+1]);
}

module shell() {
difference() {
    cube([inner_width + 2*thick, inner_height + 2* thick, inner_depth +2*thick]);
    translate([thick,thick,thick]) inner(.15);
}
}

module cover() {
translate([inner_width + 2*thick + 5,0,0]) {
    difference() {
        union() {
            translate([0,0,inner_height+thick]) cube([inner_width+2*thick,inner_height+2*thick,thick]);
        inner();
        }
        translate([-1,-1,-1]) cube([inner_width+2, inner_height+2, wavgat_z+1]);
        translate([-1,-1,inner_height+2*thick]) cube([inner_width+2, inner_height+2, inner_height]);
        
        translate([inner_width - wavgat_x+thick,thick,0]) cube([wavgat_x-2*thick , wavgat_y-2*thick, inner_depth]);
       
        translate([-1,wavgat_y,0]) cube([esp_x+2 , inner_height -wavgat_y+1, inner_depth ]);
        translate([inner_width - wavgat_x+thick,wavgat_y-2,0]) cube([esp_x-inner_width + wavgat_x -2*thick, inner_height -wavgat_y-2*thick, inner_depth ]);
        
        translate([inner_width - wavgat_x + 20 + thick-4, 15+thick-4,0]) cube([8,8,inner_depth+2*thick +2], centered=true);
    }
    
}
}

//cover();
shell();