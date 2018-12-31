// Test pegs

PEG_HEIGHT = 7;
PEG_RADIUS_BASE = 2.5 / 2;
PEG_RADIUS_TOP = 1.5 / 2;
PEG_OFFSET = 5;

BOARD_WIDTH = 30;
BOARD_LENGTH = 10;
BOARD_THICKNESS = 3;

module peg(x, y, h, r1, r2) {
	translate([
		x,
		y,
		BOARD_THICKNESS
	])
		cylinder(h, r1 / 2, r2 / 2, $fn=60);
}

module peg_hole(x, y, r) {
	translate([
		x,
		y,
		-5
	])
		cylinder(10, r / 2, r / 2, $fn=60);
}

module board() {
	cube([
		BOARD_WIDTH,
		BOARD_LENGTH,
		BOARD_THICKNESS
	]);
}

// -----------------------------------------------------------------------------

module test_pegs(r2, r1, h, x, y, i, c) {
	translate([
		x,
		y,
		0
	])
		difference() {
            union() {
                board();
                
                peg(PEG_OFFSET, PEG_OFFSET, h, r1, r2);
                peg(BOARD_WIDTH - PEG_OFFSET, PEG_OFFSET, h, r1, r2);
            }
            
            for (x=[0:i-1])
                translate([6, 0 + (c*2), -3])
                    cube([i+1, 5, 4]);
        }
}

// -----------------------------------------------------------------------------

module test_peg_holes(r, x, y, i) {
	translate([
		x,
		y,
		0
	])
		difference() {
			board();

			peg_hole(PEG_OFFSET, PEG_OFFSET, r);
			peg_hole(BOARD_WIDTH - PEG_OFFSET, PEG_OFFSET, r);
            
            for (x=[0:i-1])
                translate([10, 2, -3])
                    cube([i+1, 6, 4]);
		}
}


// -----------------------------------------------------------------------------
// Peg hole tests 

test_peg_holes(1.5, 5, 0, 1);
test_peg_holes(1.75, 5, 20, 2);
test_peg_holes(2, 5, 40, 3);
test_peg_holes(2.25, 5, 60, 4);
test_peg_holes(2.5, 5, 80, 5);

// -----------------------------------------------------------------------------
// Peg tests 

test_pegs(1, 2.5, 6, 40, 0, 1, 1);
test_pegs(1.25, 2.5, 6, 40, 20, 2, 1);
test_pegs(1.5, 2.5, 6, 40, 40, 3, 1);
test_pegs(1.75, 2.5, 6, 40, 60, 4, 1);
test_pegs(2, 2.5, 6, 40, 80, 5, 1);

test_pegs(1, 2.5, 4, 75, 0, 1, 2);
test_pegs(1.25, 2.5, 4, 75, 20, 2, 2);
test_pegs(1.5, 2.5, 4, 75, 40, 3, 2);
test_pegs(1.75, 2.5, 4, 75, 60, 4, 2);
test_pegs(2, 2.5, 4, 75, 80, 5, 2);

test_pegs(1, 2, 6, 110, 0, 1, 3);
test_pegs(1.25, 2, 6, 110, 20, 2, 3);
test_pegs(1.5, 2, 6, 110, 40, 3, 3);
test_pegs(1.75, 2, 6, 110, 60, 4, 3);
test_pegs(2, 2, 6, 110, 80, 5, 3);
