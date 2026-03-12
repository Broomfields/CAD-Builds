//variables (mm)
	idlerID = 25.5;
	idlerOD = 72.5;
	beltwidth= 5;
	$fn=560; //faceting

//these are the lips that hold the belt on
	lipheight = 10;
	lipthickness = -1;
	topangle = 60; //the angle the top lip overhang makes. You can increase this to lower the idler profile.

    diskHeight = lipthickness*2+beltwidth+lipheight*cos(topangle);
    bevelHeight = 3;

//construction
	difference(){
        union(){
            cylinder(
            r= (idlerOD / 2), 
            h= (lipthickness * 2 + beltwidth + lipheight * cos(topangle))
            );
            
//            translate([-15,0,(-bevelHeight) - 1]) cylinder(
//            r= ((idlerID/2) + 5), 
//            h= (diskHeight + bevelHeight)
//            );
            
//            translate([15,0,(-bevelHeight) - 1]) cylinder(
//            r= ((idlerID/2) + 5), 
//            h= (diskHeight + bevelHeight)
//            );
            
		}
        
    union() {
        translate([15,0,-1])
            cylinder(
            r= (idlerID / 2), 
            h= (diskHeight + 2)
            );
            
//        translate([15,0,(-diskHeight)])        
//            cylinder(
//            r= (idlerID / 3), 
//            h= (diskHeight + bevelHeight + 1)
//            );
        }
    union() {
        translate([-15,0,-1])
            cylinder(
            r= (idlerID / 2), 
            h= (diskHeight + 2)
            );
            
//        translate([-15,0,(-diskHeight)])        
//            cylinder(
//            r= (idlerID / 3), 
//            h= (diskHeight + bevelHeight + 1)
//            );
        }
        
        rotate([0, 0, 45]) translate( [(idlerOD/2 - 4.9), 0, bevelHeight + 1])
            linear_extrude(height = diskHeight + 2, center = true)
                difference() {
                    square([10,4], center = true);
                }
                
        rotate([0, 0, 135]) translate( [(idlerOD/2 - 4.9), 0, bevelHeight + 1])
            linear_extrude(height = diskHeight + 2, center = true)
                difference() {
                    square([10,4], center = true);
                }
                
        rotate([0, 0, -45]) translate( [(idlerOD/2 - 4.9), 0, bevelHeight + 1])
            linear_extrude(height = diskHeight + 2, center = true)
                difference() {
                    square([10,4], center = true);
                }
                
        rotate([0, 0, -135]) translate( [(idlerOD/2 - 4.9), 0, bevelHeight + 1])
            linear_extrude(height = diskHeight + 2, center = true)
                difference() {
                    square([10,4], center = true);
                }
}