// Ansible widget cases
//
// Mount: base mount for selectors
// -----------------------------------------------------------------------------

include <../params.scad>;

// -----------------------------------------------------------------------------

module selector_mount(type_label) {
	color(SELECTOR_MOUNT_COLOR) {
		// Cylinder base
		difference() {
			// Outside
			union() {
				// Base
				cylinder(MOUNT_HEIGHT, SELECTOR_MOUNT_RADIUS, SELECTOR_MOUNT_RADIUS, $fn=MOUNT_SEGMENTS);
				
				// Grip
				translate([
					0,
					0,
					MOUNT_HEIGHT - GRIP_HEIGHT
				])
					cylinder(
						GRIP_HEIGHT,
						SELECTOR_MOUNT_RADIUS + GRIP_THICKNESS,
						SELECTOR_MOUNT_RADIUS + GRIP_THICKNESS,
						$fn=MOUNT_SEGMENTS
					);

				// Type label
				translate([0, SELECTOR_LABEL_Y, MOUNT_HEIGHT])
				linear_extrude(LABEL_MOUNT_HEIGHT)
					text(
						type_label,
						font=LABEL_MOUNT_FONT,
						size=LABEL_MOUNT_FONT_SIZE,
						halign="center"
					);
			}
			
			// Cut out inside hole
			translate([
				0,
				0,
				-SELECTOR_HOLE_OFFSET
			])
					cylinder(
						MOUNT_HEIGHT,
						SELECTOR_HOLE_RADIUS,
						SELECTOR_HOLE_RADIUS,
						$fn=MOUNT_SEGMENTS
					);
		}
	}
}
