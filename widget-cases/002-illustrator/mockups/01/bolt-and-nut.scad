include <params.scad>;

// -----------------------------------------------------------------------------

module pack_and_pi() {
	battery_pack();
	raspberry_pi();
}

// -----------------------------------------------------------------------------

module battery_pack() {
    color(BATTERY_COLOR) {
        translate([
			// Center it
			(CASE_WIDTH / 2) - (BATTERY_WIDTH / 2),
			// Move it in a little bit
			BATTERY_Y,
			// Sit it directly on the floor
			3 + BATTERY_DIAMETER / 2
		])
			rotate([-90, 0, 0])
			linear_extrude(BATTERY_LENGTH)
			hull() {
				translate([BATTERY_DIAMETER / 2, 0, 0])
					circle(BATTERY_DIAMETER / 2, $fn=SEGMENTS);

				translate([BATTERY_WIDTH - BATTERY_DIAMETER / 2, 0, 0])
					circle(BATTERY_DIAMETER / 2, $fn=SEGMENTS);
			}
    }
}

// -----------------------------------------------------------------------------

module raspberry_pi() {
    color(PI_COLOR) {
        translate([
			// Center it
			(CASE_WIDTH / 2) - (PI_WIDTH / 2),
			// How far down the case it should go
			PI_Y,
			// Put it on the shelf (with the shelf thickness taken into
			// account) and a little extra since it won't sit flush
			35
		])
			difference() {
				// Base Pi
				cube([
					PI_WIDTH,
					PI_LENGTH,
					PI_DEPTH
				]);

				// Peg holes
				translate([
					PI_HOLE_OFFSET_X,
					PI_HOLE_OFFSET_Y,
					-5
				])
					cylinder(10, PI_HOLE_RADIUS, PI_HOLE_RADIUS, $fn=SEGMENTS);

				translate([
					PI_WIDTH - PI_HOLE_OFFSET_X,
					PI_HOLE_OFFSET_Y,
					-5
				])
					cylinder(10, PI_HOLE_RADIUS, PI_HOLE_RADIUS, $fn=SEGMENTS);

				translate([
					PI_HOLE_OFFSET_X,
					PI_LENGTH - PI_HOLE_OFFSET_Y,
					-5
				])
					cylinder(10, PI_HOLE_RADIUS, PI_HOLE_RADIUS, $fn=SEGMENTS);

				translate([
					PI_WIDTH - PI_HOLE_OFFSET_X,
					PI_LENGTH - PI_HOLE_OFFSET_Y,
					-5
				])
					cylinder(10, PI_HOLE_RADIUS, PI_HOLE_RADIUS, $fn=SEGMENTS);
			}
    }
}

// -----------------------------------------------------------------------------

module floor_peg(x, y) {
	color("red") {
	translate([x, y, -3])
		cylinder(43, 1, 1, $fn=60);
		}
}

// -----------------------------------------------------------------------------

module tall_floor_peg(x, y) {
	color([0.6, 0.7, 0.9]) {
	translate([x, y, -3])
		cylinder(66, 1, 1, $fn=60);
		}
}

// -----------------------------------------------------------------------------

module floor() {
	union() {
		cube([90, 140, 3]);

		floor_peg(9, 55);	
		floor_peg(9, 80);	

		floor_peg(81, 55);	
		floor_peg(81, 80);	

		tall_floor_peg(20, 130);
		tall_floor_peg(70, 130);

		tall_floor_peg(5, 5);
		tall_floor_peg(85, 5);
	}
}

// -----------------------------------------------------------------------------

module pi_shelf() {
	color([0.7, 0.8, 0.4]) {
		translate([5, 51, 31])
			cube([80, 35, 3]);
	}
}

// -----------------------------------------------------------------------------

module lid() {
	translate([0, 0, 55])
		union() {
			difference() {
				cube([90, 140, 3]);

				translate([90/2 - 30/2, 20, -5])
					cube([30, 30, 10]);

				translate([90/2 - 50/2, 90, -5])
					cube([50, 30, 10]);
			}

			// Selector
			lid_peg(90/2 - 30/2 - 3, 18);
			lid_peg(90/2 + 30/2 + 3, 18);

			lid_peg(90/2 - 30/2 - 3, 52);
			lid_peg(90/2 + 30/2 + 3, 52);

			// Widget
			lid_peg(90/2 - 50/2 - 3, 88);
			lid_peg(90/2 + 50/2 + 3, 88);

			lid_peg(90/2 - 50/2 - 3, 122);
			lid_peg(90/2 + 50/2 + 3, 122);
		}
}

// -----------------------------------------------------------------------------

module lid_peg(x, y) {
	color("red") {
		translate([x, y, -3])
			cylinder(25, 1, 1, $fn=60);
	}
}

// -----------------------------------------------------------------------------

module selector() {
	color([0.8, 0.9, 0.6]) {
		translate([90/2 - 42/2, 14, 70])
			cube([42, 42, 3]);
	}
}

// -----------------------------------------------------------------------------

module widget() {
	color([0.9, 0.6, 0.8]) {
		translate([90/2 - 62/2, 84, 70])
			cube([62, 42, 3]);
	}
}

// -----------------------------------------------------------------------------

floor();
lid();
selector();
widget();
pi_shelf();
pack_and_pi();
