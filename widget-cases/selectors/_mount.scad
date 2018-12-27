// Ansible widget cases
//
// Mount: base mount for selectors
// -----------------------------------------------------------------------------

include <../params.scad>;

// -----------------------------------------------------------------------------

module selector_mount() {
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
				MOUNT_HEIGHT - SELECTOR_GRIP_HEIGHT
			])
				cylinder(
					SELECTOR_GRIP_HEIGHT,
					SELECTOR_MOUNT_RADIUS + SELECTOR_GRIP_THICKNESS,
					SELECTOR_MOUNT_RADIUS + SELECTOR_GRIP_THICKNESS
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
