// Ansible widget cases
//
// Magnet: LSM303 magnet selector w/ mount
// -----------------------------------------------------------------------------

include <../params.scad>;
use <_mount.scad>;

// -----------------------------------------------------------------------------

module magnet_selector() {
	color(SELECTOR_MOUNT_COLOR) {
		union() {        
			// Pegs
			translate([
				(SELECTOR_DOCK_RADIUS / 2) - MAGNET_PEG_OFFSET_X,
				(-SELECTOR_DOCK_RADIUS / 2) + MAGNET_PEG_OFFSET_Y,
				MOUNT_HEIGHT + MAGNET_PEG_OFFSET_Z
			])
				cylinder(MAGNET_PEG_HEIGHT, MAGNET_PEG_RADIUS_BASE, MAGNET_PEG_RADIUS_TOP, $fn=SEGMENTS);
		   
			translate([
				(-SELECTOR_DOCK_RADIUS / 2) + MAGNET_PEG_OFFSET_X,
				(-SELECTOR_DOCK_RADIUS / 2) + MAGNET_PEG_OFFSET_Y,
				MOUNT_HEIGHT + MAGNET_PEG_OFFSET_Z
			])
				cylinder(MAGNET_PEG_HEIGHT, MAGNET_PEG_RADIUS_BASE, MAGNET_PEG_RADIUS_TOP, $fn=SEGMENTS);
			
			// Cut out hole for wires
			difference() {
				// Mount
				selector_mount("M");
				
				// Hole
				translate([
					-MAGNET_HOLE_WIDTH/2,
					0,
					// Move it to the top, then arbitrarily go -5 so it cuts through
					MOUNT_HEIGHT - 5
				])
					cube([
						MAGNET_HOLE_WIDTH,
						MAGNET_HOLE_LENGTH,
						// Arbitrary, make sure it cuts through
						10
					]);
				
				// Board inset
				translate([
					-MAGNET_BOARD_INSET_WIDTH / 2,
					-MAGNET_BOARD_INSET_HEIGHT / 2,
					MOUNT_HEIGHT - MAGNET_BOARD_INSET_DEPTH
				])
					cube([
						MAGNET_BOARD_INSET_WIDTH,
						MAGNET_BOARD_INSET_HEIGHT,
						// Arbitrary, make sure it cuts through the top
						5
					]);
			}
		}
	}
}

// -----------------------------------------------------------------------------

module lsm303_board() {
	color([0.8, 0.3, 0.3]) {
		difference() {
			// Base LSM303
			cube([
				MAGNET_BOARD_WIDTH,
				MAGNET_BOARD_HEIGHT,
				1
			]);

			// Peg holes
			translate([
				MAGNET_PEG_HOLE_OFFSET_X,
				MAGNET_PEG_HOLE_OFFSET_Y,
				-5
			])
				cylinder(10, MAGNET_PEG_HOLE_RADIUS, MAGNET_PEG_HOLE_RADIUS, $fn=SEGMENTS);

			translate([
				MAGNET_BOARD_WIDTH - MAGNET_PEG_HOLE_OFFSET_X,
				MAGNET_PEG_HOLE_OFFSET_Y,
				-5
			])
				cylinder(10, MAGNET_PEG_HOLE_RADIUS, MAGNET_PEG_HOLE_RADIUS, $fn=SEGMENTS);
		}
	}
}
