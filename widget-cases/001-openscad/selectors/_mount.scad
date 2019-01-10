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

			// Carve out notches
			translate([
				-SELECTOR_MOUNT_RADIUS - SELECTOR_MOUNT_THICKNESS,
				-SELECTOR_MOUNT_NOTCH_SIZE / 2,
				-2
			])
				cube([
					SELECTOR_MOUNT_RADIUS * 2 + 10,
					SELECTOR_MOUNT_NOTCH_SIZE,
					SELECTOR_MOUNT_NOTCH_HEIGHT + 2
				]);

			translate([
				SELECTOR_MOUNT_RADIUS - SELECTOR_MOUNT_THICKNESS - SELECTOR_MOUNT_NOTCH_SIZE / 2 + 0.5,
				-SELECTOR_MOUNT_RADIUS / 2 - SELECTOR_MOUNT_NOTCH_SIZE / 2 - 5,
				-2
			])
			rotate([0, 0, 90])
				cube([
					SELECTOR_MOUNT_RADIUS * 2 + 10,
					SELECTOR_MOUNT_NOTCH_SIZE,
					SELECTOR_MOUNT_NOTCH_HEIGHT + 2
				]);
		}
	}
}
