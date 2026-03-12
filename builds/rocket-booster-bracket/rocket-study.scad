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
        difference()
        {
            disk();
            boosterSlot();
//            boosterSlot(x= 15);
//            boosterSlot(x= -15);
            finSlit(45);
            finSlit(-45);       
            finSlit(135);        
            finSlit(-135);
        }
        
module disk(x= 0, y= 0, z= 0)
{
    union()
    {
        cylinder(
        r= (idlerOD / 2), 
        h= (lipthickness * 2 + beltwidth + lipheight * cos(topangle))
        );
    }
}

module boosterSlot(x=0, y=0)
{    
    translate([x, y,(-bevelHeight) - 1]) cylinder(
    r= ((idlerID/2) + 5), 
    h= (diskHeight + bevelHeight)
    );

    difference()
    {
        union()
        {
            translate([x, y, -1])
                cylinder(
                r= (idlerID / 2), 
                h= (diskHeight + 2)
                );
                
            translate([x, y, (-diskHeight)])        
                cylinder(
                r= (idlerID / 3), 
                h= (diskHeight + bevelHeight + 1)
                );
            }
    }
}

module finSlit(rotation = 45)
{
    rotate([0, 0, rotation]) translate( [(idlerOD/2 - 4.9), 0, bevelHeight + 1])
            linear_extrude(height = diskHeight + 2, center = true)
                difference() {
                    square([10,4], center = true);
                }
}