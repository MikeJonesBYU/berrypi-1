// Ansible widget cases
//
// Misc: Battery pack and Raspberry Pi (not printed)
// -----------------------------------------------------------------------------

include <params.scad>;

// -----------------------------------------------------------------------------

module pack_and_pi() {
	battery_pack();
	raspberry_pi();
}

// -----------------------------------------------------------------------------

module battery_pack() {
    color(BATTERY_COLOR) {
        translate([
			// Center it
			(CASE_WIDTH / 2) - (BATTERY_WIDTH / 2),
			// Move it in a little bit
			WALL_THICKNESS * 2,
			// Sit it directly on the floor
			WALL_THICKNESS
		])
			cube([
				BATTERY_WIDTH,
				BATTERY_HEIGHT,
				BATTERY_DEPTH
			]);
    }
}

// -----------------------------------------------------------------------------

module raspberry_pi() {
    color(PI_COLOR) {
        translate([
			// Center it
			(CASE_WIDTH / 2) - (PI_WIDTH / 2),
			// How far down the case it should go
			PI_Y,
			// Put it on the shelf (with the shelf thickness taken into
			// account) and a little extra since it won't sit flush
			SHELF_HEIGHT + SHELF_THICKNESS + 2
		])
            cube([
				PI_WIDTH,
				PI_LENGTH,
				PI_DEPTH
			]);
    }
}

// -----------------------------------------------------------------------------

pack_and_pi();
