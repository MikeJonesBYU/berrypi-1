// Ansible widget cases
//
// Magnet: LSM303 magnet selector w/ mount
// -----------------------------------------------------------------------------

include <../params.scad>;
use <_mount.scad>;

// -----------------------------------------------------------------------------

module magnet_selector(r, h, thickness) {
	color(SELECTOR_MOUNT_COLOR) {
		union() {        
			// Pegs
			translate([
				(SELECTOR_DOCK_RADIUS / 2) - MAGNET_PEG_OFFSET_X,
				(-SELECTOR_DOCK_RADIUS / 2) + MAGNET_PEG_OFFSET_Y,
				MOUNT_HEIGHT + MAGNET_PEG_OFFSET_Z
			])
				cylinder(MAGNET_PEG_HEIGHT, MAGNET_PEG_RADIUS_BASE, MAGNET_PEG_RADIUS_TOP);
		   
			translate([
				(-SELECTOR_DOCK_RADIUS / 2) + MAGNET_PEG_OFFSET_X,
				(-SELECTOR_DOCK_RADIUS / 2) + MAGNET_PEG_OFFSET_Y,
				MOUNT_HEIGHT + MAGNET_PEG_OFFSET_Z
			])
				cylinder(MAGNET_PEG_HEIGHT, MAGNET_PEG_RADIUS_BASE, MAGNET_PEG_RADIUS_TOP);
			
			// Cut out hole for wires
			difference() {
				// Mount
				selector_mount();
				
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
