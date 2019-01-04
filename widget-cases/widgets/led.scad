// Ansible widget cases
//
// LED widget w/ mount
// -----------------------------------------------------------------------------

include <../params.scad>;
use <_mount.scad>;

// -----------------------------------------------------------------------------

module led_widget() {
    union() {        
		// Shelf
		_led_shelf();

        // Cut out hole for wires
        difference() {
            // Mount
            widget_mount();
            
            // Lead holes
			_lead_holes();
        }
    }
}

// -----------------------------------------------------------------------------

module _lead_holes() {
	// Lead holes
	translate([
		WIDGET_MOUNT_SIZE / 2 - LED_LEAD_DISTANCE / 2,
		WIDGET_MOUNT_SIZE / 2,
		MOUNT_HEIGHT - 5
	])
		cylinder(10, LED_HOLE_RADIUS, LED_HOLE_RADIUS, $fn=SEGMENTS);

	translate([
		WIDGET_MOUNT_SIZE / 2 + LED_LEAD_DISTANCE / 2,
		WIDGET_MOUNT_SIZE / 2,
		MOUNT_HEIGHT - 5
	])
		cylinder(10, LED_HOLE_RADIUS, LED_HOLE_RADIUS, $fn=SEGMENTS);
}

// -----------------------------------------------------------------------------

module _led_shelf() {
	// Shelf for wiring
	translate([
		LED_SHELF_X,
		LED_SHELF_Y,
		LED_SHELF_Z,
	])
		cube([LED_SHELF_WIDTH, LED_SHELF_HEIGHT, LED_SHELF_DEPTH]);

	// Shelf for wiring
	translate([
		LED_SHELF2_X,
		LED_SHELF2_Y,
		LED_SHELF2_Z,
	])
		cube([LED_SHELF_WIDTH, LED_SHELF_HEIGHT, LED_SHELF_DEPTH]);
}

// -----------------------------------------------------------------------------

led_widget();
