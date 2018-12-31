// Ansible widget cases
//
// Case: walls and floor for case
// -----------------------------------------------------------------------------

include <params.scad>;

// -----------------------------------------------------------------------------

module case() {
	// Difference to cut out door slot
	difference() {
		// Union floor, side walls, ridge, shelf
		union() {
			// Floor
			cube([CASE_WIDTH, CASE_LENGTH, FLOOR_THICKNESS]);
			
			// Side and back walls
			_case_walls();
			
			// Pi shelf
			_pi_shelf();

			// Battery guides
			_battery_guides();
		   
			// Ridges
			_ridges();
		}
			
		// Cut out the door slot
		_door_slot();
	}
}

// -----------------------------------------------------------------------------

module _case_walls() {
	// Side wall (far side)
	translate([
		CASE_WIDTH - WALL_THICKNESS,
		0,
		0
	])
		cube([WALL_THICKNESS, CASE_LENGTH, CASE_HEIGHT]);
	
	// Side wall (near side)
	translate([
		0,
		0,
		0
	])
		cube([WALL_THICKNESS, CASE_LENGTH, CASE_HEIGHT]);

	// Back wall
	cube([CASE_WIDTH, WALL_THICKNESS, CASE_HEIGHT]);
}

// -----------------------------------------------------------------------------

module _ridges() {
	// Side ridge (far)
	translate([
		CASE_WIDTH - RIDGE_THICKNESS - WALL_THICKNESS,
		WALL_THICKNESS,
		CASE_HEIGHT - WALL_THICKNESS
	])
		cube([
			RIDGE_THICKNESS,
			CASE_LENGTH - WALL_THICKNESS,
			WALL_THICKNESS
		]);

	// Side ridge (near)
	translate([
		WALL_THICKNESS,
		WALL_THICKNESS,
		CASE_HEIGHT - WALL_THICKNESS
	])
		cube([
			RIDGE_THICKNESS,
			CASE_LENGTH - WALL_THICKNESS,
			WALL_THICKNESS
		]);

	// Back ridge
	translate([
		0,
		WALL_THICKNESS,
		CASE_HEIGHT - WALL_THICKNESS
	])
		cube([
			CASE_WIDTH,
			RIDGE_THICKNESS,
			WALL_THICKNESS
		]);

	// Ridge pegs
	_ridge_pegs();
}

// -----------------------------------------------------------------------------

module _ridge_pegs() {    
	translate([
		RIDGE_PEG_OFFSET,
		RIDGE_PEG_OFFSET,
		CASE_HEIGHT
	])
		cylinder(RIDGE_PEG_HEIGHT, RIDGE_PEG_RADIUS_BASE, RIDGE_PEG_RADIUS_TOP, $fn=SEGMENTS);

	translate([
		CASE_WIDTH - RIDGE_PEG_OFFSET,
		RIDGE_PEG_OFFSET,
		CASE_HEIGHT
	])
		cylinder(RIDGE_PEG_HEIGHT, RIDGE_PEG_RADIUS_BASE, RIDGE_PEG_RADIUS_TOP, $fn=SEGMENTS);

	translate([
		RIDGE_PEG_OFFSET,
		CASE_LENGTH - RIDGE_PEG_OFFSET,
		CASE_HEIGHT
	])
		cylinder(RIDGE_PEG_HEIGHT, RIDGE_PEG_RADIUS_BASE, RIDGE_PEG_RADIUS_TOP, $fn=SEGMENTS);

	translate([
		CASE_WIDTH - RIDGE_PEG_OFFSET,
		CASE_LENGTH - RIDGE_PEG_OFFSET,
		CASE_HEIGHT
	])
		cylinder(RIDGE_PEG_HEIGHT, RIDGE_PEG_RADIUS_BASE, RIDGE_PEG_RADIUS_TOP, $fn=SEGMENTS);
}

// -----------------------------------------------------------------------------

module _pi_shelf() {
	// Pi shelf
	translate([
		0,
		// Move it down to the right spot in the case
		SHELF_Y,
		// Move it up to the right height (with room for the battery)
		SHELF_HEIGHT
	])
		cube([CASE_WIDTH, SHELF_LENGTH, SHELF_THICKNESS]);

	// Pi pegs
	translate([
		// Center it
		(CASE_WIDTH / 2) - (PI_WIDTH / 2),
		// Move it down to the right spot on the shelf
		PI_Y,
		// Put it right on top of the shelf
		SHELF_HEIGHT + SHELF_THICKNESS
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

module _battery_guides() {
	// Battery guides
	translate([
		// Put it on the near side
		(CASE_WIDTH / 2 - BATTERY_WIDTH / 2) - (BATTERY_GUIDE_WIDTH*1.414) - BATTERY_GUIDE_OFFSET_X,
		// Move it down to the right spot in the case
		WALL_THICKNESS,
		// Move it up to the right height (at the floor)
		WALL_THICKNESS
	])
	rotate([0, 45, 0])
		cube([BATTERY_GUIDE_WIDTH, BATTERY_GUIDE_LENGTH, BATTERY_GUIDE_HEIGHT]);

	translate([
		// Put it on the far side
		(CASE_WIDTH / 2 + BATTERY_WIDTH / 2) + BATTERY_GUIDE_OFFSET_X,
		// Move it down to the right spot in the case
		WALL_THICKNESS,
		// Move it up to the right height (at the floor)
		WALL_THICKNESS
	])
	rotate([0, 45, 0])
		cube([BATTERY_GUIDE_WIDTH, BATTERY_GUIDE_LENGTH, BATTERY_GUIDE_HEIGHT]);
}

// -----------------------------------------------------------------------------

module _door_slot() {
	// Cut out the door slot
	translate([
		// Move in enough for the inset
		WALL_THICKNESS - FRONT_DOOR_INSET,
		// Put it at the end of the case, subtracting the wall and the
		// offset
		CASE_LENGTH - WALL_THICKNESS - FRONT_DOOR_OFFSET_Y,
		// Move in enough for the inset
		WALL_THICKNESS - FRONT_DOOR_INSET
	])
		cube([
			// Door slot should go full width so the one side is open
			CASE_WIDTH,
			// Door slot thickness
			FRONT_DOOR_THICKNESS + FRONT_DOOR_INSET,
			// Door slot height should carve out enough for the inset
			CASE_HEIGHT - WALL_THICKNESS - FRONT_DOOR_INSET
		]);
}

// -----------------------------------------------------------------------------

case();
