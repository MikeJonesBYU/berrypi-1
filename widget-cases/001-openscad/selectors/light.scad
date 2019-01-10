// Ansible widget cases
//
// Light: TSL2561 light selector w/ mount
// -----------------------------------------------------------------------------

include <../params.scad>;
use <_mount.scad>;

// -----------------------------------------------------------------------------

module light_selector() {
	color(SELECTOR_MOUNT_COLOR) {
		union() {        
			// Pegs
			translate([
				(SELECTOR_DOCK_RADIUS / 2) - LIGHT_PEG_OFFSET_X,
				(-SELECTOR_DOCK_RADIUS / 2) + LIGHT_PEG_OFFSET_Y,
				MOUNT_HEIGHT + LIGHT_PEG_OFFSET_Z
			])
				cylinder(LIGHT_PEG_HEIGHT, LIGHT_PEG_RADIUS_BASE, LIGHT_PEG_RADIUS_TOP, $fn=SEGMENTS);
		   
			translate([
				(-SELECTOR_DOCK_RADIUS / 2) + LIGHT_PEG_OFFSET_X,
				(-SELECTOR_DOCK_RADIUS / 2) + LIGHT_PEG_OFFSET_Y,
				MOUNT_HEIGHT + LIGHT_PEG_OFFSET_Z
			])
				cylinder(LIGHT_PEG_HEIGHT, LIGHT_PEG_RADIUS_BASE, LIGHT_PEG_RADIUS_TOP, $fn=SEGMENTS);
			
			// Cut out hole for wires
			difference() {
				// Mount
				selector_mount("L");
				
				// Hole
				translate([
					-LIGHT_HOLE_WIDTH/2,
					0,
					// Move it to the top, then arbitrarily go -5 so it cuts through
					MOUNT_HEIGHT - 5
				])
					cube([
						LIGHT_HOLE_WIDTH,
						LIGHT_HOLE_LENGTH,
						// Arbitrary, make sure it cuts through
						10
					]);
				
				// Board inset
				translate([
					-LIGHT_BOARD_INSET_WIDTH / 2,
					-LIGHT_BOARD_INSET_HEIGHT / 2,
					MOUNT_HEIGHT - LIGHT_BOARD_INSET_DEPTH
				])
					cube([
						LIGHT_BOARD_INSET_WIDTH,
						LIGHT_BOARD_INSET_HEIGHT,
						// Arbitrary, make sure it cuts through the top
						5
					]);
			}
		}
	}
}

// -----------------------------------------------------------------------------

module tsl2561_board() {
	color([0.8, 0.3, 0.3]) {
		difference() {
			// Base TSL2561
			cube([
				LIGHT_BOARD_WIDTH,
				LIGHT_BOARD_HEIGHT,
				1
			]);

			// Peg holes
			translate([
				LIGHT_PEG_HOLE_OFFSET_X,
				LIGHT_PEG_HOLE_OFFSET_Y,
				-5
			])
				cylinder(10, LIGHT_PEG_HOLE_RADIUS, LIGHT_PEG_HOLE_RADIUS, $fn=SEGMENTS);

			translate([
				LIGHT_BOARD_WIDTH - LIGHT_PEG_HOLE_OFFSET_X,
				LIGHT_PEG_HOLE_OFFSET_Y,
				-5
			])
				cylinder(10, LIGHT_PEG_HOLE_RADIUS, LIGHT_PEG_HOLE_RADIUS, $fn=SEGMENTS);
		}
	}
}

// -----------------------------------------------------------------------------

light_selector();
