// -----------------------------------------------------------------------------
// Groove test

translate([0, 0, 0])
    difference() {
        cube([36, 30, 3]);
        
        translate([6, 6, 2])
            cylinder(4, 3, 3);
    }

translate([40, 0, 0])
    difference() {
        cube([35.5, 30, 3]);
        
        translate([6, 6, 2])
            cylinder(4, 3, 3);

        translate([14, 6, 2])
            cylinder(4, 3, 3);
    }

translate([75, 33, 0])
rotate([0, 0, 90])
    difference() {
        cube([35, 30, 3]);
        
        translate([6, 6, 2])
            cylinder(4, 3, 3);

        translate([14, 6, 2])
            cylinder(4, 3, 3);

        translate([22, 6, 2])
            cylinder(4, 3, 3);
    }

// Groove casing
translate([0, 66, 0])
rotate([90, 0, 0])
    difference() {
        cube([40, 25, 31]);

		// Back hole
		translate([3, 3, -6])
			cube([34, 27, 40]);

        // Groove
        translate([3, 3, 3])
            cube([34, 26, 25]);
      
        // Inside groove (3mm)
        translate([2, 2, 5])
            cube([36, 26, 3]);

        // Inside groove (3mm)
        translate([2, 2, 10])
            cube([36, 26, 3.5]);

        // Inside groove (4mm)
        translate([2, 2, 16])
            cube([36, 26, 4]);

        // Inside groove (4mm)
        translate([2, 2, 22])
            cube([36, 26, 4.5]);
       
        // View hole
        translate([3, 3, 3])
            cube([34, 19, 30]);
    }
