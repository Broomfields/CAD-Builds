//variables (mm)
	idlerID = 70;
	idlerOD = 75;
    lidIR = 35;
    lidOR = 37;
    depth = 50;
    rimDepth = 10;
    lidDepth = 5;
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
    translate([0,0,depth - 15])
    disk();
    
    translate([0,0,-1])
    cylinder( r= (idlerID / 2), h= (depth + 2) ); 
}
difference()
{
    top();
    
    translate([25,0,depth - lidDepth - 1])
    cylinder(
        r= lidIR / 2,
        h= lidDepth + 2
    );
}
    
module disk(x= 0, y= 0, z= 0)
{
    cylinder(
        r= lidOR,
        h= 15
    );
}
    
    
module top(x= 0, y= 0, z= 0)
{
    translate([0,0,depth - lidDepth])
    cylinder(
        r= lidOR,
        h= (lidDepth)
    );
}