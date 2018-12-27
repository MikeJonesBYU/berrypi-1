// Ansible widget cases
//
// Mount: base mount for selectors
// -----------------------------------------------------------------------------

include <../params.scad>;

// -----------------------------------------------------------------------------

module selector_mount() {
	color(SELECTOR_MOUNT_COLOR) {
		// Cylinder base
		difference() {
			// Outside
			union() {
				// Base
				cylinder(MOUNT_HEIGHT, SELECTOR_MOUNT_RADIUS, SELECTOR_MOUNT_RADIUS);
				
				// Grip
				translate([
					0,
					0,
					MOUNT_HEIGHT - GRIP_HEIGHT
				])
					cylinder(
						GRIP_HEIGHT,
						SELECTOR_MOUNT_RADIUS + GRIP_THICKNESS,
						SELECTOR_MOUNT_RADIUS + GRIP_THICKNESS
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
						SELECTOR_HOLE_RADIUS
					);
		}
	}
}
