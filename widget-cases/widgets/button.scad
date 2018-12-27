// Ansible widget cases

PI_W = 66.04;
PI_L = 30.48;
PI_D = 1.5;

LID_GROOVE_WIDTH = 2;

module pi_connectors() {    
    x_offset = 3.5;
    y_offset = 3;

    h = 8;
    r1 = 2.5;
    r2 = 1.5;

    translate([x_offset, y_offset, 0])
        cylinder(h, r1, r2);
    translate([PI_W - x_offset, y_offset, 0])
        cylinder(h, r1, r2);
    translate([x_offset, PI_L - y_offset, 0])
        cylinder(h, r1, r2);
    translate([PI_W - x_offset, PI_L - y_offset, 0])
        cylinder(h, r1, r2);
}

module case(width, length, wall_thickness, shelf_y, shelf_length, shelf_height, divider_y, case_height, widget_dock_height, pi_y, groove_width, ridge_thickness) {
    
    difference() {
    union() {
        // Floor
        difference() {
            cube([width, length, wall_thickness]);
        }
        
        // Pi shelf
        translate([0, shelf_y, shelf_height])
            cube([width, shelf_length, wall_thickness]);
        translate([width / 2 - PI_W / 2, pi_y, shelf_height + wall_thickness])
            pi_connectors();
        
        // Side walls
        difference() {
            // Wall
            translate([width - wall_thickness, 0, 0])
                cube([wall_thickness, length, case_height]);
        }
        
        difference() {
            // Wall
            translate([0, 0, 0])
                cube([wall_thickness, length, case_height]);
        }
       
        // Ridges
        // Back ridge
        translate([0, wall_thickness, case_height - wall_thickness])
            cube([width, ridge_thickness,wall_thickness]);
        // Side ridges
        translate([wall_thickness, wall_thickness, case_height - wall_thickness])
            cube([ridge_thickness, length - wall_thickness, wall_thickness]);
        translate([width - ridge_thickness - wall_thickness, wall_thickness, case_height - wall_thickness])
            cube([ridge_thickness, length - wall_thickness, wall_thickness]);

        // Ridge connectors
        h = 6;
        r1 = 2.5;
        r2 = 1.5;
        ridge_offset = 5;
        translate([ridge_offset, ridge_offset, case_height])
            cylinder(h, r1, r2);
        translate([width - ridge_offset, ridge_offset, case_height])
            cylinder(h, r1, r2);
        translate([ridge_offset, length - ridge_offset, case_height])
            cylinder(h, r1, r2);
        translate([width - ridge_offset, length - ridge_offset, case_height])
            cylinder(h, r1, r2);

        // Back wall
        cube([width, wall_thickness, case_height]);
    }
        
    // Door slot
    translate([-1, length - wall_thickness - 5, wall_thickness - 1])
        cube([width, 4, case_height - wall_thickness - 1]);
    }
    
    // Door (length - 7)
    translate([0, length + 30, wall_thickness - 1])
    union() {
        difference() {
            cube([width, 3, case_height - wall_thickness * 2 + 2]);
            
            translate([width / 2, 0, case_height / 2])
            sphere(10);
        }
    }
}

// Lid
module lid(width, length, case_height, wall_thickness, widget_dock_size, selection_dock_r) {
    selection_y = length * 0.78;
    widget_y = length * 0.15;
    widget_w = widget_dock_size;
    widget_l = widget_dock_size;
    border_height = 9;
    border_thickness = 4;

    
//    translate([width + 10, 0, case_height])
    translate([0, 0, case_height + 30])
        difference() {
            union() {
                // Lid
                cube([width, length, wall_thickness]);
                
                // Widget dock border
                translate([width / 2 - widget_w / 2, widget_y, 0])
                linear_extrude(height=border_height)
                hull() {
                    translate([-border_thickness / 2, -border_thickness / 2, 0])
                        circle(r=5/2);
                
                    translate([widget_w + border_thickness / 2, -border_thickness / 2, 0])
                        circle(r=5/2);
                
                    translate([-border_thickness / 2, widget_l + border_thickness / 2, 0])
                        circle(r=5/2);
                
                    translate([widget_w + border_thickness / 2, widget_l + border_thickness / 2, 0])
                        circle(r=5/2);
                }
            
                // Selection dock border
                translate([width / 2, selection_y, 0])
                    linear_extrude(height=border_height)
                    circle(r=selection_dock_r + border_thickness);
            }
           
            // Widget dock
            translate([width / 2 - widget_w / 2, widget_y, 2])
                cube([widget_w, widget_l, border_height + 1]);
            
            // Widget dock hole
            widget_offset = border_thickness * 2;
            widget_hole_w = widget_w - widget_offset;
            widget_hole_l = widget_l - widget_offset;
            translate([width / 2 - widget_hole_w / 2, widget_y + widget_offset / 2, -5])
                cube([widget_hole_w, widget_hole_l, 10]);
            
            // Selection dock
            translate([width / 2, selection_y, 2])
            linear_extrude(height=border_height + 1)
                circle(r=selection_dock_r);
            
            // Selection dock hole
            s_hole_r = selection_dock_r - border_thickness;
            translate([width / 2, selection_y, -5])
                cylinder(10, s_hole_r, s_hole_r);
                            
            // Ridge connectors
            h = 10;
            r = 2;
            ridge_offset = 5;
            translate([ridge_offset, ridge_offset, -5])
                cylinder(h, r, r);
            translate([width - ridge_offset, ridge_offset, -5])
                cylinder(h, r, r);
            translate([ridge_offset, length - ridge_offset, -5])
                cylinder(h, r, r);
            translate([width - ridge_offset, length - ridge_offset, -5])
                cylinder(h, r, r);
        }
}

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

module selector_mount(r, h, thickness) {
    // 1 mm off for spacing
    real_r = r - 0.5;
    inside_r = real_r - thickness;
    grip_height = 5;
    grip_thickness = 7;

    // Cylinder base
    difference() {
        // Outside
        union() {
            // Base
            cylinder(h, real_r, real_r);
            
            // Grip
            translate([0, 0, h - grip_height])
            cylinder(grip_height, real_r + grip_thickness, real_r + grip_thickness);
        }
        
        // Carve out inside
        translate([0, 0, -thickness])
            cylinder(h, inside_r, inside_r);
    }
}

// LSM303 magnet selector mount
module magnet_selector(r, h, thickness) {
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

shelf_height = 28;
wall_thickness = 3;

module default_case() {
    WIDTH = 90;
    LENGTH = 140;
    SHELF_Y = 52;
    SHELF_LENGTH = 40;
    SHELF_HEIGHT = 28;
    WALL_THICKNESS = 3;
    DIVIDER_Y = 65;
    CASE_HEIGHT = 55;
    WIDGET_DOCK_HEIGHT = CASE_HEIGHT;
    PI_Y = DIVIDER_Y - 8;
    GROOVE_WIDTH = LID_GROOVE_WIDTH + 1;
    RIDGE_THICKNESS = 6;

    case(
        width=WIDTH,
        length=LENGTH,
        shelf_y=SHELF_Y,
        shelf_length=SHELF_LENGTH,
        shelf_height=SHELF_HEIGHT,  
        wall_thickness=WALL_THICKNESS,
        divider_y=DIVIDER_Y,
        case_height=CASE_HEIGHT,
        widget_dock_height=WIDGET_DOCK_HEIGHT,
        pi_y=PI_Y,
        groove_width=GROOVE_WIDTH,
        ridge_thickness=RIDGE_THICKNESS
    );

    SELECTION_DOCK_R = 16;
    WIDGET_DOCK_SIZE = 32;
    
    lid(
        width=WIDTH,
        length=LENGTH,
        case_height=CASE_HEIGHT,
        wall_thickness=WALL_THICKNESS,
        selection_dock_r=SELECTION_DOCK_R,
        widget_dock_size=WIDGET_DOCK_SIZE
    );
    
    MOUNT_HEIGHT = 15;
    MOUNT_THICKNESS = 3;
    
    translate([WIDTH/2, LENGTH*.78, CASE_HEIGHT + 30 + 30])
    magnet_selector(
        r=SELECTION_DOCK_R,
        h=MOUNT_HEIGHT,
        thickness=MOUNT_THICKNESS
    );

    translate([WIDTH/2 - WIDGET_DOCK_SIZE/2, LENGTH*.15, CASE_HEIGHT + 30 + 30])
    widget_mount(
        s=WIDGET_DOCK_SIZE,
        h=MOUNT_HEIGHT,
        thickness=MOUNT_THICKNESS
    );
}

default_case();




module pack_and_pi() {
    CASE_WIDTH = 90;
    DIVIDER_Y = 65;
    
    // Battery pack
    color([0.2, 0.2, 0.2]) {
        translate([CASE_WIDTH / 2 - 68.58 / 2, wall_thickness * 2, wall_thickness])
        cube([68.58, 96.52, 22.86]);
    }

    // Pi
    color([0.3, 0.4, 0.3]) {
        translate([CASE_WIDTH / 2 - PI_W / 2, DIVIDER_Y - 8, shelf_height + wall_thickness + 2])
            cube([PI_W, PI_L, PI_D]);
    }
}

pack_and_pi();