// Ansible widget cases
//
// Button: button selector w/ mount
// -----------------------------------------------------------------------------

include <../params.scad>;
use <_mount.scad>;

// -----------------------------------------------------------------------------

module button_selector() {
	color(SELECTOR_MOUNT_COLOR) {
		union() {        
			// Cut out hole for wires
			difference() {
				// Mount
				selector_mount("B");
			}
		}
	}
}
