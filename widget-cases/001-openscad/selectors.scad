// Ansible widget cases
//
// Selectors: shows all the selectors
// -----------------------------------------------------------------------------

include <params.scad>;

use <selectors/_mount.scad>;
use <selectors/magnet.scad>;
use <selectors/light.scad>;
use <selectors/button.scad>;

// -----------------------------------------------------------------------------

X_TRANSLATION = SELECTOR_DOCK_RADIUS * 3;

// -----------------------------------------------------------------------------

// Blank mount
translate([
	0,
	0,
	0,
])
	selector_mount();

// -----------------------------------------------------------------------------

// Magnet selector
translate([
	1 * X_TRANSLATION,
	0,
	0,
])
	magnet_selector();

translate([
	1 * X_TRANSLATION - SELECTOR_DOCK_RADIUS / 2 - 2.5,
	-SELECTOR_DOCK_RADIUS / 2 - 1.5,
	MOUNT_HEIGHT + 1
])
	lsm303_board();

// -----------------------------------------------------------------------------

// Light selector
translate([
	2 * X_TRANSLATION,
	0,
	0,
])
	light_selector();

translate([
	2 * X_TRANSLATION - SELECTOR_DOCK_RADIUS / 2 - 0.5,
	-SELECTOR_DOCK_RADIUS / 2 + 1,
	MOUNT_HEIGHT + 1
])
	tsl2561_board();

// -----------------------------------------------------------------------------

// Button selector
translate([
	3 * X_TRANSLATION,
	0,
	0,
])
	button_selector();

// -----------------------------------------------------------------------------
