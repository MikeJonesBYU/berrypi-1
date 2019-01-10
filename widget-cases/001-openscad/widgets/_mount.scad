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
							circle(r=WIDGET_BORDER_RADIUS, $fn=SEGMENTS);
					
						translate([
							WIDGET_MOUNT_SIZE + GRIP_THICKNESS,
							0,
							0
						])
							circle(r=WIDGET_BORDER_RADIUS, $fn=SEGMENTS);
					
						translate([
							0,
							WIDGET_MOUNT_SIZE + GRIP_THICKNESS,
							0,
						])
							circle(r=WIDGET_BORDER_RADIUS, $fn=SEGMENTS);
					
						translate([
							WIDGET_MOUNT_SIZE + GRIP_THICKNESS,
							WIDGET_MOUNT_SIZE + GRIP_THICKNESS,
							0,
						])
							circle(r=WIDGET_BORDER_RADIUS, $fn=SEGMENTS);
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

			// Carve out notches
			translate([
				-WIDGET_MOUNT_THICKNESS - 5,
				(WIDGET_MOUNT_SIZE / 2) - (WIDGET_MOUNT_NOTCH_SIZE / 2),
				-2
			])
				cube([
					WIDGET_MOUNT_SIZE + WIDGET_MOUNT_THICKNESS + 10,
					WIDGET_MOUNT_NOTCH_SIZE,
					WIDGET_MOUNT_NOTCH_HEIGHT + 2
				]);

			translate([
				WIDGET_MOUNT_SIZE / 2 + WIDGET_MOUNT_NOTCH_SIZE / 2,
				-WIDGET_MOUNT_SIZE / 2 + WIDGET_MOUNT_THICKNESS + 10,
				-2
			])
			rotate([0, 0, 90])
				cube([
					WIDGET_MOUNT_SIZE + WIDGET_MOUNT_THICKNESS + 10,
					WIDGET_MOUNT_NOTCH_SIZE,
					WIDGET_MOUNT_NOTCH_HEIGHT + 2
				]);
		}
	}
}
