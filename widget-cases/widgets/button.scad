// Ansible widget cases

// Budget widget
module button_widget() {
    peg_r1 = 2.5;
    peg_r2 = 1.5;
    peg_h = 7;
    base_height = 2;
    
    widget_w = 23;
    widget_h = 21;
    
    union() {        
        // Pegs
        translate([1 + r/2, -r/2, h])
            cylinder(peg_h, peg_r1, peg_r2);
       
        translate([-r/2 - 1, -r/2, h])
            cylinder(peg_h, peg_r1, peg_r2);
        
        // Cut out hole for wires
        difference() {
            // Mount
            selector_mount(r, h, thickness);
            
            // Hole
            hole_x = widget_w - 5;
            hole_l = 10;
            translate([-hole_x/2, 0, h - 5])
                cube([hole_x, hole_l, 10]);
            
            // Board inset
            inset_w = widget_w + 1;
            inset_h = widget_h + 1;
            translate([-inset_w/2, -inset_h/2, h - 1])
                cube([inset_w, inset_h, 5]);
        }
    }
}
