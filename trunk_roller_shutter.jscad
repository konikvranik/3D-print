// source: trunk_roller_shutter.jscad



function rawShell(x,y,z,r1,r2) {
	return CSG.cube([x,y,z]).subtract([CSG.cube([r1,r1,z]), CSG.cube([r2,r2,z]).translate([0,y-r2,0])])
		.union([
			cylinder({r:r1, h:z}).translate([r1,r1,0]),
			CSG.cylinder({r:r2, h:z}).translate([r2,y-r2,0])]);
}

function shell(x,y,z,w) {
	var r1 = 20-w;
	var r2 = 10-w;
	var h1 = 30;

	return rawShell(x-2*w,y-2*w,z,r1,r2).subtract([
		CSG.cube([15,32,z]).translate([0,y-32-w,52-w]),
		CSG.cube([12,37-w-6,h1])
			.union(CSG.cylinder({r:6,h:h1}).translate([6,37-w-6,0]))
			.translate([30,0,0])
	]).expand(w,16)
		.subtract([ rawShell(x-2*w,y-2*w,z,r1,r2).translate([0,0,w]) ])
		.translate([w,w,0]);
}


// producer: OpenJSCAD 1.0.3
function main(){
	CSG.defaultResolution3D=10;
	return shell(97,68,68,2.5);
}
  
//only add this wrapper if not already present & we are not in command-line mode
if(typeof wrappedMain === 'undefined' && typeof getParameterDefinitionsCLI !== 'undefined'){
  const wrappedMain = main
  main = function(){
    var paramsDefinition = (typeof getParameterDefinitions !== 'undefined') ? getParameterDefinitions : undefined
    return wrappedMain(getParameterDefinitionsCLI(paramsDefinition, {}))
  }
}

  
