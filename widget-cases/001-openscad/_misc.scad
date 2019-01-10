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
			WALL_THICKNESS + BATTERY_DIAMETER / 2
		])
			rotate([-90, 0, 0])
			linear_extrude(BATTERY_LENGTH)
			hull() {
				translate([BATTERY_DIAMETER / 2, 0, 0])
					circle(BATTERY_DIAMETER / 2, $fn=SEGMENTS);

				translate([BATTERY_WIDTH - BATTERY_DIAMETER / 2, 0, 0])
					circle(BATTERY_DIAMETER / 2, $fn=SEGMENTS);
			}
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
			difference() {
				// Base Pi
				cube([
					PI_WIDTH,
					PI_LENGTH,
					PI_DEPTH
				]);

				// Peg holes
				translate([
					PI_HOLE_OFFSET_X,
					PI_HOLE_OFFSET_Y,
					-5
				])
					cylinder(10, PI_HOLE_RADIUS, PI_HOLE_RADIUS, $fn=SEGMENTS);

				translate([
					PI_WIDTH - PI_HOLE_OFFSET_X,
					PI_HOLE_OFFSET_Y,
					-5
				])
					cylinder(10, PI_HOLE_RADIUS, PI_HOLE_RADIUS, $fn=SEGMENTS);

				translate([
					PI_HOLE_OFFSET_X,
					PI_LENGTH - PI_HOLE_OFFSET_Y,
					-5
				])
					cylinder(10, PI_HOLE_RADIUS, PI_HOLE_RADIUS, $fn=SEGMENTS);

				translate([
					PI_WIDTH - PI_HOLE_OFFSET_X,
					PI_LENGTH - PI_HOLE_OFFSET_Y,
					-5
				])
					cylinder(10, PI_HOLE_RADIUS, PI_HOLE_RADIUS, $fn=SEGMENTS);
			}
    }
}

// -----------------------------------------------------------------------------

pack_and_pi();
