// Ansible widget cases

module widget_mount(s, h, thickness) {
    // 1 mm off for spacing
    real_s = s - 1;
    inside_s = real_s - thickness;
    grip_height = 5;
    grip_thickness = 7;

    // Square base
    difference() {
        // Outside
        union() {
            // Base
            cube([real_s, real_s, h]);
            
            // Grip
            translate([-grip_thickness/2, -grip_thickness/2, h - grip_height])
                linear_extrude(height=grip_height)
                hull() {
                    translate([0, 0, 0])
                        circle(r=5/2);
                
                    translate([real_s + grip_thickness, 0, 0])
                        circle(r=5/2);
                
                    translate([0, real_s+grip_thickness, 0])
                        circle(r=5/2);
                
                    translate([real_s+grip_thickness, real_s+grip_thickness, 0])
                        circle(r=5/2);
                }
        }
        
        // Carve out inside
        translate([thickness, thickness, -thickness])
            cube([inside_s - thickness, inside_s - thickness, h]);
    }
}
