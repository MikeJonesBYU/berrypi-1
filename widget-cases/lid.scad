// Ansible widget cases
//
// Lid: lid with selector/widget docks in it
// -----------------------------------------------------------------------------

include <params.scad>;

// -----------------------------------------------------------------------------

module lid() {
	// Cut out the inset and the connection holes
	difference() {
		// Union the lid and the borders
		union() {
			// Base lid
			cube([
				CASE_WIDTH,
				CASE_LENGTH,
				LID_THICKNESS
			]);
			
			// Widget/selector dock borders
			_widget_dock_border();
			_selector_dock_border();
		}
	   
		// Cut out the widget/selector dock inset and hole
		_widget_dock();
		_selector_dock();

		// Cut out the ridge peg holes
		_ridge_peg_holes();
	}
}

// -----------------------------------------------------------------------------

// Border for the widget dock
module _widget_dock_border() {
	translate([
		// Center it
		(CASE_WIDTH / 2) - (WIDGET_DOCK_SIZE / 2),
		// How far down the lid to put the dock
		WIDGET_DOCK_Y,
		0
	])
	linear_extrude(height=DOCK_BORDER_HEIGHT)
		hull() {
			translate([
				-DOCK_BORDER_THICKNESS / 2,
				-DOCK_BORDER_THICKNESS / 2,
				0
			])
				circle(r=WIDGET_BORDER_RADIUS, $fn=SEGMENTS);
		
			translate([
				WIDGET_DOCK_SIZE + DOCK_BORDER_THICKNESS / 2,
				-DOCK_BORDER_THICKNESS / 2,
				0
			])
				circle(r=WIDGET_BORDER_RADIUS, $fn=SEGMENTS);
		
			translate([
				-DOCK_BORDER_THICKNESS / 2,
				WIDGET_DOCK_SIZE + DOCK_BORDER_THICKNESS / 2,
				0
			])
				circle(r=WIDGET_BORDER_RADIUS, $fn=SEGMENTS);
		
			translate([
				WIDGET_DOCK_SIZE + DOCK_BORDER_THICKNESS / 2,
				WIDGET_DOCK_SIZE + DOCK_BORDER_THICKNESS / 2,
				0
			])
				circle(r=WIDGET_BORDER_RADIUS, $fn=SEGMENTS);
		}
}

// -----------------------------------------------------------------------------

// Border for the selector dock
module _selector_dock_border() {
	translate([
		// Center it
		CASE_WIDTH / 2,
		// How far down the lid to put the dock
		SELECTOR_DOCK_Y,
		0
	])
		cylinder(
			DOCK_BORDER_HEIGHT,
			SELECTOR_DOCK_BORDER_RADIUS,
			SELECTOR_DOCK_BORDER_RADIUS,
			$fn=MOUNT_SEGMENTS
		);
}

// -----------------------------------------------------------------------------

// Widget dock inset and hole
module _widget_dock() {
	// Cut out the widget dock inset
	translate([
		// Center it
		(CASE_WIDTH / 2) - (WIDGET_DOCK_SIZE / 2),
		// How far down the lid to put the inset
		WIDGET_DOCK_Y,
		// Leave some behind
		DOCK_INSET
	])
		cube([
			// Size of the dock
			WIDGET_DOCK_SIZE,
			WIDGET_DOCK_SIZE,
			// Add one so it cuts all the way through the top
			DOCK_BORDER_HEIGHT + 1
		]);
	
	// Cut out the widget dock connection hole
	translate([
		// Center it
		(CASE_WIDTH / 2) - (WIDGET_HOLE_SIZE / 2),
		// Center it within the dock
		WIDGET_DOCK_Y + (WIDGET_HOLE_OFFSET / 2),
		// Arbitrary, to make sure it cuts all the way through
		-5
	])
		cube([
			// Size of the hole
			WIDGET_HOLE_SIZE,
			WIDGET_HOLE_SIZE,
			// Arbitrary, to make sure it cuts all the way through
			10
		]);
}

// -----------------------------------------------------------------------------

// Selector dock inset and hole
module _selector_dock() {
	// Selection dock
	translate([
		// Center it
		CASE_WIDTH / 2,
		// How far down the lid to put the inset
		SELECTOR_DOCK_Y,
		// Leave some behind
		DOCK_INSET
	])
		cylinder(
			// Add one so it cuts all the way through the top
			DOCK_BORDER_HEIGHT + 1,
			// Size of the dock
			SELECTOR_DOCK_RADIUS,
			SELECTOR_DOCK_RADIUS,
			$fn=MOUNT_SEGMENTS
		);
	
	// Selection dock hole
	translate([
		// Center it
		CASE_WIDTH / 2,
		// How far down the lid to put the hole
		SELECTOR_DOCK_Y,
		// Arbitrary, to make sure it cuts all the way through
		-5
	])
		cylinder(
			// Arbitrary, to make sure it cuts all the way through
			10,
			// Size of the hole
			SELECTOR_HOLE_SIZE,
			SELECTOR_HOLE_SIZE,
			$fn=MOUNT_SEGMENTS
		);
}

// -----------------------------------------------------------------------------

// Ridge peg holes
module _ridge_peg_holes() {
	translate([
		RIDGE_PEG_OFFSET,
		RIDGE_PEG_OFFSET,
		// Add 10 to make sure it goes through
		-10
	])
		cylinder(20, RIDGE_PEG_RADIUS_HOLE, RIDGE_PEG_RADIUS_HOLE, $fn=SEGMENTS);

	translate([
		CASE_WIDTH - RIDGE_PEG_OFFSET,
		RIDGE_PEG_OFFSET,
		-10
	])
		cylinder(20, RIDGE_PEG_RADIUS_HOLE, RIDGE_PEG_RADIUS_HOLE, $fn=SEGMENTS);

	translate([
		RIDGE_PEG_OFFSET,
		CASE_LENGTH - RIDGE_PEG_OFFSET,
		-10
	])
		cylinder(20, RIDGE_PEG_RADIUS_HOLE, RIDGE_PEG_RADIUS_HOLE, $fn=SEGMENTS);

	translate([
		CASE_WIDTH - RIDGE_PEG_OFFSET,
		CASE_LENGTH - RIDGE_PEG_OFFSET,
		-10
	])
		cylinder(20, RIDGE_PEG_RADIUS_HOLE, RIDGE_PEG_RADIUS_HOLE, $fn=SEGMENTS);
}

// -----------------------------------------------------------------------------

lid();
