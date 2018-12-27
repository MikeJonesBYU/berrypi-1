// Ansible widget cases
//
// Mount: base mount for widgets
// -----------------------------------------------------------------------------

include <../params.scad>;

// -----------------------------------------------------------------------------

module widget_mount() {
	color(WIDGET_MOUNT_COLOR) {
		// Square base
		difference() {
			// Outside
			union() {
				// Base
				cube([WIDGET_MOUNT_SIZE, WIDGET_MOUNT_SIZE, MOUNT_HEIGHT]);
				
				// Grip
				translate([
					-GRIP_THICKNESS / 2,
					-GRIP_THICKNESS / 2,
					MOUNT_HEIGHT - GRIP_HEIGHT
				])
					linear_extrude(height=GRIP_HEIGHT)
					hull() {
						translate([
							0,
							0,
							0
						])
							circle(r=WIDGET_BORDER_RADIUS);
					
						translate([
							WIDGET_MOUNT_SIZE + GRIP_THICKNESS,
							0,
							0
						])
							circle(r=WIDGET_BORDER_RADIUS);
					
						translate([
							0,
							WIDGET_MOUNT_SIZE + GRIP_THICKNESS,
							0,
						])
							circle(r=WIDGET_BORDER_RADIUS);
					
						translate([
							WIDGET_MOUNT_SIZE + GRIP_THICKNESS,
							WIDGET_MOUNT_SIZE + GRIP_THICKNESS,
							0,
						])
							circle(r=WIDGET_BORDER_RADIUS);
					}
			}
			
			// Carve out inside
			translate([
				WIDGET_MOUNT_THICKNESS,
				WIDGET_MOUNT_THICKNESS,
				-WIDGET_MOUNT_THICKNESS
			])
				cube([
					WIDGET_MOUNT_SIZE - WIDGET_MOUNT_THICKNESS * 2,
					WIDGET_MOUNT_SIZE - WIDGET_MOUNT_THICKNESS * 2,
					MOUNT_HEIGHT
				]);
		}
	}
}
