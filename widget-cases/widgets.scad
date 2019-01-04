// Ansible widget cases
//
// Widgets: shows all the widgets
// -----------------------------------------------------------------------------

include <params.scad>;

use <widgets/_mount.scad>;
use <widgets/led.scad>;

// -----------------------------------------------------------------------------

X_TRANSLATION = WIDGET_DOCK_SIZE * 1.5;

// -----------------------------------------------------------------------------

// Blank mount
translate([
	0,
	0,
	0,
])
	widget_mount();

// -----------------------------------------------------------------------------

// LED
translate([
	1 * X_TRANSLATION,
	0,
	0,
])
	led_widget();
