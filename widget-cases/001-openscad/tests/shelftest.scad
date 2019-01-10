// Ansible widget cases
//
// Case: walls and floor for case
// -----------------------------------------------------------------------------

include <../params.scad>;

// -----------------------------------------------------------------------------

module _pi_shelf() {
	difference() {
		cube([CASE_WIDTH, SHELF_LENGTH, SHELF_THICKNESS]);

		// Shelf hole
		translate([
			// Center it
			(CASE_WIDTH / 2) - (SHELF_HOLE_WIDTH / 2),
			// Move it down just a bit
			SHELF_HOLE_OFFSET_Y,
			// Cut through all the way
			-2
		])
			cube([SHELF_HOLE_WIDTH, SHELF_HOLE_LENGTH, SHELF_THICKNESS + 10]);
	}

	// Pi pegs
	translate([
		// Center it
		(CASE_WIDTH / 2) - (PI_WIDTH / 2),
		// Move it down to the right spot on the shelf
		3,
		// Put it right on top of the shelf
		SHELF_THICKNESS
	])
		_pi_pegs();
}

// -----------------------------------------------------------------------------

module _pi_pegs() {    
    translate([
		SHELF_PEG_OFFSET_X,
		SHELF_PEG_OFFSET_Y,
		0
	])
        cylinder(SHELF_PEG_HEIGHT, SHELF_PEG_RADIUS_BASE, SHELF_PEG_RADIUS_TOP, $fn=SEGMENTS);

    translate([
		// Offset from end of Pi
		PI_WIDTH - SHELF_PEG_OFFSET_X,
		SHELF_PEG_OFFSET_Y,
		0
	])
        cylinder(SHELF_PEG_HEIGHT, SHELF_PEG_RADIUS_BASE, SHELF_PEG_RADIUS_TOP, $fn=SEGMENTS);

    translate([
		SHELF_PEG_OFFSET_X,
		// Offset from end of Pi
		PI_LENGTH - SHELF_PEG_OFFSET_Y,
		0
	])
        cylinder(SHELF_PEG_HEIGHT, SHELF_PEG_RADIUS_BASE, SHELF_PEG_RADIUS_TOP, $fn=SEGMENTS);

    translate([
		// Offset from end of Pi
		PI_WIDTH - SHELF_PEG_OFFSET_X,
		// Offset from end of Pi
		PI_LENGTH - SHELF_PEG_OFFSET_Y,
		0
	])
        cylinder(SHELF_PEG_HEIGHT, SHELF_PEG_RADIUS_BASE, SHELF_PEG_RADIUS_TOP, $fn=SEGMENTS);
}

// -----------------------------------------------------------------------------

_pi_shelf();
