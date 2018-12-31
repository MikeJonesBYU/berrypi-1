// Ansible widget cases
//
// Front: front door with finger hole in it
// -----------------------------------------------------------------------------

include <params.scad>;

// -----------------------------------------------------------------------------

module front() {    
    union() {
        difference() {
			// Front door
            cube([
				// Account for the far wall which we don't go through
				FRONT_DOOR_WIDTH,
				// How thick the door is
				FRONT_DOOR_THICKNESS,
				// How tall the door is (ignore top/bottom walls, do account
				// for the gap)
				FRONT_DOOR_HEIGHT
			]);
            
			// Lazily use a sphere instead of rotating a circle, and put it
			// smack in the middle
            translate([
				// Center it
				FRONT_DOOR_WIDTH / 2,
				0,
				// Center it
				FRONT_DOOR_HEIGHT / 2
			])
				sphere(10, $fn=SEGMENTS);
        }
    }
}

// -----------------------------------------------------------------------------

front();
