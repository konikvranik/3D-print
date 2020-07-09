charging_base=[75, 75, 12];
phone=[72, 153, 8.6]+[1, 1, 1];
wall=3;
grab=5;

difference() {
	translate([-wall, -wall, -wall-charging_base[2]]) {
		cube(phone+[2*wall, wall-20, 2*wall]+[0, 0, charging_base[2]]);
		translate([wall+10, 0, 0]) cube(phone+[-20, 2*wall+phone[1]*3/8, 2*wall]+[0, 0, charging_base[2]]);
	}
	cube(phone);
	translate([-2*wall, phone[1]/4], 0) cube(phone+[4*wall, phone[0]/4, 4*wall]);
	translate([grab, grab, 0]) cube(phone-[2*grab, 2*grab, -wall-1]);
	translate((phone-charging_base)/2-[0, 0, phone[2]/2+charging_base[2]/2]) cube(charging_base+[0, 0, 0]);
	translate((phone-charging_base)/2-[0, -5, phone[2]/2+charging_base[2]/2]) cube(charging_base+[0, -5, 3]);
	translate([phone[0]/2-25/2, phone[1]/2, -charging_base[2]]) cube([25, phone[1]/2, charging_base[2]-1]);
	translate([phone[0]/2-10/2, phone[1], -10]) cube([10, phone[1]*2, 5]);
	translate([phone[0]/2-10/2, phone[1]*1.5-20-wall, -charging_base[2]-2*wall]) cube([10, 20, charging_base[2]+3*wall]);
	translate(phone/2-[10, 0, 0]) rotate([-90, 0, 0]) cylinder(d=4, h=2*phone[1]);
	translate(phone/2+[10, 0, 0]) rotate([-90, 0, 0]) cylinder(d=4, h=2*phone[1]);
}
