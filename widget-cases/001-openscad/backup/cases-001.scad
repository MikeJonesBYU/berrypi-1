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
    
    // Lid
    selection_y = length * 0.78;
    widget_y = length * 0.15;
    widget_w = 50;
    widget_l = 40;
    border_height = 9;
    border_thickness = 4;
    selection_dock_r = 16;
    
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
                        circle(r=5);
                
                    translate([widget_w + border_thickness / 2, -border_thickness / 2, 0])
                        circle(r=5);
                
                    translate([-border_thickness / 2, widget_l + border_thickness / 2, 0])
                        circle(r=5);
                
                    translate([widget_w + border_thickness / 2, widget_l + border_thickness / 2, 0])
                        circle(r=5);
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
            widget_offset = 18;
            widget_hole_w = widget_w - widget_offset;
            widget_hole_l = widget_l - widget_offset;
            translate([width / 2 - widget_hole_w / 2, widget_y + widget_offset / 2, -5])
                cube([widget_hole_w, widget_hole_l, 10]);
            
            // Selection dock
            translate([width / 2, selection_y, 2])
            linear_extrude(height=border_height + 1)
                circle(r=selection_dock_r);
            
            // Selection dock holes
            offset = selection_dock_r - 6;
            
            translate([width / 2, selection_y - offset, -5])
            cylinder(10, 2.5, 2.5);
            
            translate([width / 2, selection_y + offset, -5])
            cylinder(10, 2.5, 2.5);
            
            horiz_offset = 9;
            y_offset = 5;
            translate([width / 2 - horiz_offset, selection_y + y_offset, -5])
            cylinder(10, 2.5, 2.5);
                
            translate([width / 2 + horiz_offset, selection_y + y_offset, -5])
            cylinder(10, 2.5, 2.5);
                
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

shelf_height = 28;
wall_thickness = 3;

module default_case() {
    WIDTH = 84;
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
}

default_case();

module pack_and_pi() {
    CASE_WIDTH = 84;
    DIVIDER_Y = 65;
    
    // Battery pack
    color("red") {
        translate([CASE_WIDTH / 2 - 68.58 / 2, wall_thickness * 2, wall_thickness])
        cube([68.58, 96.52, 22.86]);
    }

    // Pi
    color("blue") {
        translate([CASE_WIDTH / 2 - PI_W / 2, DIVIDER_Y - 8, shelf_height + wall_thickness + 2])
            cube([PI_W, PI_L, PI_D]);
    }
}

pack_and_pi();