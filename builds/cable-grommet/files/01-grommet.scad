//variables (mm)
	idlerID = 70;
	idlerOD = 75;
    depth = 50;
    rimDepth = 10;
	beltwidth= 5;
	$fn=560; //faceting

//these are the lips that hold the belt on
	lipheight = 10;
	lipthickness = -1;
	topangle = 60; //the angle the top lip overhang makes. You can increase this to lower the idler profile.

    bevelHeight = 3;

//construction
difference()
{
    union()
    {
        disk();
        rim();
    }
    
    translate([0,0,-1])
    cylinder( r= (idlerID / 2), h= (depth + 2) ); 
 
    
 
    translate([0,0, ((depth - rimDepth) - 5)])
    cylinder( r= (idlerID / 2) + 2, h= (rimDepth + 5) );   
    
}    
    
module disk(x= 0, y= 0, z= 0)
{
    cylinder(
        r= (idlerOD / 2),
        h= depth
    );
}
    
    
module rim(x= 0, y= 0, z= 0)
{
    translate([0,0,depth - rimDepth])
    cylinder(
        r= (idlerOD / 2) + 10,
        h= (rimDepth)
    );
}