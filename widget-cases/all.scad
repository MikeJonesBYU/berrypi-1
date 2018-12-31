// Ansible widget cases
//
// All: shows all in one
// -----------------------------------------------------------------------------

include <params.scad>;

use <case.scad>;
use <front.scad>;
use <lid.scad>;
use <_misc.scad>;

use <widgets/_mount.scad>;
use <selectors/magnet.scad>;

// -----------------------------------------------------------------------------

// Set these to change how close things are to the case
FRONT_OFFSET_Y = 30;
LID_OFFSET_Z = 30;
MOUNT_OFFSET_Z = 30;

// -----------------------------------------------------------------------------

// Case
case();

/*
 *
// Front
translate([
	0,
	// Add the potential offset (to explode the view)
	CASE_LENGTH + FRONT_OFFSET_Y,
	// How high up it should be
	WALL_THICKNESS - FRONT_DOOR_INSET
])
	front();

// Lid
translate([
	0,
	0,
	// Add the potential offset (to explode the view)
	CASE_HEIGHT + LID_OFFSET_Z
])
	lid();

// Magnet selector
translate([
	// Center it
	CASE_WIDTH / 2,
	// How far down the lid it should be
	SELECTOR_DOCK_Y,
	// Add the potential offsets (to explode the view)
	CASE_HEIGHT + LID_OFFSET_Z + MOUNT_OFFSET_Z
])
	magnet_selector();

// Widget mount
translate([
	// Center it
	(CASE_WIDTH / 2) - (WIDGET_DOCK_SIZE / 2),
	// How far down the lid it should be
	WIDGET_DOCK_Y,
	// Add the potential offsets (to explode the view)
	CASE_HEIGHT + LID_OFFSET_Z + MOUNT_OFFSET_Z
])
	widget_mount();
*/

// Battery pack and Raspberry Pi
pack_and_pi();
