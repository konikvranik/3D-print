
$fn=64;


use <threads.scad>;

module usatko() {
    d_in = 5;
    d_out = 11.3;
    h_in = 11.5;
    h_out = 14.3;
    hole = 3.3;
    threads=6;
    thread_length=5;


    difference() {
        union() {
            translate([0,0,h_out-d_out+d_out/2]) sphere(d=d_out);
            scale([1,1,h_out/d_out]) translate([0,0,d_out/2]) sphere(d=d_out);
        }
        cylinder(d=d_in, h=h_in - thread_length+1);
        cylinder(d=hole, h=h_out+1);
    translate([0,0,h_in - thread_length])  metric_thread(diameter=d_in,pitch=thread_length/threads,length=thread_length+1,internal=true);
    }
}

module stetoskop() {
    dia_d=43.8;
    dia_h=4;
    difference() {
        cylinder(d=dia_d+2,h=dia_h+.2);
        translate([0,0,.2]) metric_thread(diameter=dia_d,length=dia_h+1,pitch=.8,internal=true);
    }
}

 usatko();

translate([50,0,0]) stetoskop();