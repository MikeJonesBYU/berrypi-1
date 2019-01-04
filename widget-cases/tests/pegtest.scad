// Test pegs

PEG_HEIGHT = 7;
PEG_RADIUS_BASE = 2.5 / 2;
PEG_RADIUS_TOP = 1.5 / 2;
PEG_OFFSET = 5;

BOARD_WIDTH = 18;
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
		}
}


// -----------------------------------------------------------------------------
// Peg hole tests 

test_peg_holes(1.5, 0, 0, 1);
test_peg_holes(1.75, 0, 13, 2);
test_peg_holes(2, 0, 26, 3);
test_peg_holes(2.25, 0, 39, 4);
test_peg_holes(2.5, 0, 52, 5);

// -----------------------------------------------------------------------------
// Peg tests 

test_pegs(1, 2.5, 6, 23, 0, 1, 1);
test_pegs(1.25, 2.5, 6, 23, 13, 2, 1);
test_pegs(1.5, 2.5, 6, 23, 26, 3, 1);
test_pegs(1.75, 2.5, 6, 23, 39, 4, 1);
test_pegs(2, 2.5, 6, 23, 52, 5, 1);

test_pegs(1, 2.5, 4, 46, 0, 1, 2);
test_pegs(1.25, 2.5, 4, 46, 13, 2, 2);
test_pegs(1.5, 2.5, 4, 46, 26, 3, 2);
test_pegs(1.75, 2.5, 4, 46, 39, 4, 2);
test_pegs(2, 2.5, 4, 46, 52, 5, 2);

test_pegs(1, 2, 6, 69, 0, 1, 3);
test_pegs(1.25, 2, 6, 69, 13, 2, 3);
test_pegs(1.5, 2, 6, 69, 26, 3, 3);
test_pegs(1.75, 2, 6, 69, 39, 4, 3);
test_pegs(2, 2, 6, 69, 52, 5, 3);
