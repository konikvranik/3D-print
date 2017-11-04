// source: trunk_roller_shutter.jscad

var EXPAND = true;

function expandIf(v, w) {
  var sc = [];
  var mv = [];
  var ax = [ 'x', 'y', 'z' ];
  for (var i = 0; i < ax.length; i++) {
    var s = v.getBounds()[1][ax[i]] - v.getBounds()[0][ax[i]];
    mv.push(((v.getBounds()[1][ax[i]] + v.getBounds()[0][ax[i]]) / s) * -w);
    sc.push((s + 2 * w) / s);
  }
  return EXPAND ? v.expand(w, CSG.defaultResolution3D) : v.scale(sc).translate(mv);
}

function roundCorners(obj, rs) {
  var cls = [];
  for (i = 0; i < rs.length; i++) {
    var r = rs[i];
    if (r) {
      var x = obj.getBounds()[0].x;
      var y = obj.getBounds()[0].y;
      var rx = r;
      var ry = r;
      var z = obj.getBounds()[1].z;
      switch (i) {
      case 2:
      case 3:
        y = obj.getBounds()[1].y;
        ry = -r;
        if (i == 3)
          break;
      case 1:
        x = obj.getBounds()[1].x;
        rx = -r;
      default:
      }
      obj = obj.subtract(cube({size : [ rx, ry, z ]}).translate([ x, y, 0 ]))
                .union(cylinder({r : r, h : z}).translate([ x + rx, y + ry, 0 ]));
    }
  }
  return obj;
}

function partHull(x, y, z, r1, r2) {
  var p = 50 - 2.5;
  var s = 7;  // posun středu kružnice
  var r = 44; // poloměr prostřední spodní kružnice
  var r3 = 30;
  return roundCorners(cube([ x, y, z ]), [ r1, 0, r2, r2 ])
      .subtract(cube([ 50, 35, z ]).translate([ x - 15, 0, 0 ]))
      .union(cylinder({r : r3, h : z}).translate([ x - r3 + 2, r3 + 8, 0 ]))
      .subtract(cube([ 100, y, z ]).translate([ x, 0, 0 ]))
      .subtract(cube([ x, 100, z ]).translate([ 0, y, 0 ]))

      .subtract(
          cube([ 100, 100, z ]).translate([ 0, -100, 0 ]).rotate([ p, 0, 0 ], [ 0, 0, 1 ], 20)) // zkosit jednu stěnu
      .subtract(cube([ 10, 20, z ]).translate([ p - s, 0, 0 ])) // hole for bottom midle rounded corner
      .union(cylinder({r : r, h : z})
                 .subtract(cube([ 2 * r, 2 * r, z ])
                               .translate([ -r, 10, 0 ])
                               .union(cube([ r, 2 * r, z ]).translate([ -r, -r, 0 ])))
                 .translate([ p - s, r, 0 ])) // bottom midle rounded corner - not too smooth
      ;
}

/**
 * škvíra z boku
 **/
function slot(x, y, z) {
  return cube([ x, y - x / 2, z ]).union(cylinder({r : x / 2, h : z}).translate([ x / 2, y - x / 2, 0 ]));
}

function slotWalls(x, y, z, w) {
  return slot(x, y - w, z)
      .subtract(cube([ x, y, z ]).translate([ 0, 3 * w, 9 - w ]))
      .subtract(slot(x - 2 * w, y - 2 * w, z).translate([ w, 0, 0 ]))
      .union(cube([ x, w, w ]).translate([ 0, 0, z ]))
}

function cornerCircle(d, w, z, s) {
  var v = cylinder({d : d - 2 * w, h : z - 2 * w});
  return expandIf(v, w)
      .subtract(cylinder({d : d - 2 * w, h : z}))
      .subtract(cube([ d / 2, s, z ]).translate([ 0, -d / 2 + w, 0 ]));
}

function rolletHole(b, t, z, w) {
  return polyhedron({
    points : [
      [ 0, 0, 0 ],
      [ -w, 0, 0 ],
      [ 0, -b, 0 ],
      [ -w, -b, 0 ],
      [ 0, -t, z ],
      [ -w, -t, z ],
      [ 0, 0, z ],
      [ -w, 0, z ]
    ],
    polygons : [ [ 0, 1, 3, 2 ], [ 0, 6, 7, 1 ], [ 0, 2, 4, 6 ], [ 7, 5, 3, 1 ], [ 7, 6, 4, 5 ], [ 2, 3, 5, 4 ] ]
  });
}

function expandedHull(x, y, z, w, r1, r2, rolletHoleFromTop, rolletHoleTop) {

  var rolletHoleBottom = 10;
  var v = partHull(x, y, z - 2 * w, r1, r2)
              .subtract(cube([ 15, 32, z ]).translate([ 0, y - 32 + w, 50 - 2 * w ])) // vyříznout výsek
              .subtract(slot(12 - (EXPAND ? 0 : 2 * w), 37 - (EXPAND ? w : 2 * w), 30)
                            .translate([ 25 + (EXPAND ? 0 : w), 0, 0 ])) // vyříznout škvíru
              .subtract(rolletHole(rolletHoleBottom + 2 * w, rolletHoleTop + 2 * w, z, w)
                            .translate([ x, y + 2 * w - rolletHoleFromTop, 2 * w ])) // škvíra na roletu
      ;
  return expandIf(v, w);
}

function shell(x, y, z, w) {

  var rolletHoleFromTop = 11;
  var rolletHoleTop = 20;

  var r1 = 20 - w;
  var r2 = 10 - w;

  var dc = 8.5;
  var rc = dc / 2;

  var cc = cornerCircle(dc, w, z, 2.5).mirroredY();

  return expandedHull(x, y, z, w, r1, r2, rolletHoleFromTop, rolletHoleTop)
      .subtract(partHull(x, y, z, r1, r2).translate([ 0, 0, 0 ])) // vydlábnout vnitřek
      .union(cc.translate([ 15, y - rc + w, 0 ]))
      .union(cc.mirroredX().rotateZ(-45).translate([ x - rc + w, y - rc + w - (rolletHoleFromTop - dc), 0 ]))
      .union(cc.rotateZ(-90).translate([ x - rc + w, y - rc + w - (rolletHoleFromTop + rolletHoleTop), 0 ]));
}

function buttonHole(w) {
  var r = 100;
  var cyl = cylinder({r : r, h : w});
  var sq = roundCorners(cube([ 21, 15, w ]).translate([ 0, 1, 0 ]), [ 2, 2, 2, 2 ]);
  var cc = cyl.intersect(cyl.translate([ 0, 2 * r - 17 ]))
               .translate([ 21 / 2, -r + 17, 0 ])
               .intersect(cube([ 17, 17, w ]).translate([ 2, 0, 0 ]));
  return cc.union(sq).rotateX(90);
}

function rhomboid(x, y, z, a) {
  var m0 = x * tan(a);
  var my = y + m0;
  var path = polygon([ [ 0, 0 ], [ x, m0 ], [ x, my ], [ 0, y ] ]);
  return linear_extrude({height : z}, path);
}

function part(x, y, z, w) {
  var cc = cornerCircle(8.5, w, z, 2.5).mirroredY();
  var p = 50 - 2.5;
  var prolis = cube([ 9, 1.25, 24 ]);
  var screwHole = cylinder({d : 10, h : 20});

  return shell(x - 2 * w, y - 2 * w, z, w)
      .union(slotWalls(12, 37, 30 - w, w).translate([ 25, 0, 0 ]))

      .union(rhomboid(12, 8, z - w, 20)
                 .subtract(rhomboid(8, 6, z - w, 20).translate([ 2, 0, 0 ]))
                 .translate([ 77 - w - 12, 4.3, 0 ]))
      .subtract(screwHole.rotateX(90).translate([ p + 23.2, 4, 60 - w ]).rotate([ p, 0, 0 ], [ 0, 0, 1 ], 20))

      .union(cube([ 7, 11.5, 43 - w ])
                 .subtract(cube([ 7, 10.5, z ]).translate([ 1, 0, 0 ]))
                 .translate([ 89 - w, 18.5 - w, 0 ]))

      .union(cube([ 1, 4, 43 - w ]).translate([ 77 - w - 1, 15, 0 ]))

      .union(cube([ 9, 10 - w, 20 - w ])
                 .union(cube([ 1.5, 4, 18 - w ]).translate([ 9 - 1.5, -4, 0 ]))
                 .subtract(cube([ 9 - 3, 10 - w - 1.5, 20 - w ]).translate([ 1.5, 1.5, 0 ]))
                 .translate([ 30 - w - 1.5, y - 10 - w, 0 ]))

      .union(cube([ 1, 4, 43 - w ]).translate([ 76 - w, y - w - 4, 0 ]))

      .union(cube([ 1, 11 - w, 54 - w ])
                 .subtract(cube([ 1, 11 - w, 54 - w ]).translate([ 0, 11 - w - 2, 54 - w - 12 ]))
                 .translate([ 16 - w, 0, 0 ]))

      .union(
          cylinder({d : 19, h : 7 - w})
              .union(cylinder({d : 8, h : 20 - w}).subtract(cylinder({d : 5, h : 20 - w}).translate([ 0, 0, 7 - w ])))
              .translate([ 74 - w, y - 27 - w, 0 ]))

      .union(cube([ 20, 23 - w, 17.5 - w ])
                 .union(cube([ 11, 31 - w, 8 - w ]).translate([ 3 - 1.5, -8, 0 ]))
                 .subtract(cube([ 11 - 3, 31 - w - 1.5, z ])
                               .translate([ 3, 1.5 - 8, 0 ])
                               .union(cube([ 20 - 1.5, 23 - w, 17.5 - w ]).translate([ 0, 1.5, 5 - w ]))
                               .union(cube([ 7 - 3, 23 - w - 1.5, z ]).translate([ 14.5, 1.5, 0 ]))
                               .union(cube([ 20, 23 - w, 17.5 - w ]).translate([ 0, -14 + w, 10 - w ]))
                               .union(cube([ 6, 23 - w, z ]).translate([ 0, 0, 8 - w ]))
                               .union(cube([ 10.5, 21.5 - w, z ]).translate([ 2, 1.5, 0 ])))
                 .translate([ 62 - 20 - w, y - 23 - w, 0 ]))

      .union(cube([ 6, 1.5, 10.5 - w ])
                 .union(cube([ 2, 3, 17.5 - w ]).translate([ 4, -1.5, 0 ]))
                 .translate([ 61 - 6 - w, y - 32 - w, 0 ]))

      .subtract(prolis.union(prolis.translate([ 21, 0, 0 ])).translate([ 23 - w, y - 2 * w, z - 24 - w ]))

      .subtract(buttonHole(w).translate([ 38.5 - w, y - w, 5.5 - w ]))

      .subtract(screwHole.rotateY(-90).translate([ 1.5 - w, 31 - w, 60 - w ]))

      .translate([ w, w, w ]); // zalícovat s osama
}

function getParameterDefinitions() {
  return [
    {name : 'resolution', type : 'int', initial : 8, caption : "Smoothiness of model:"},
    {name : 'expand', type : 'checkbox', checked : false, caption : "Smooth corners:"}
  ];
}

function main(params) {
  CSG.defaultResolution3D = params.resolution;
  CSG.defaultResolution2D = params.resolution;
  EXPAND = params.expand;
  //  return partHull(97, 68, 68, 20, 10);
  return part(97, 68, 68, 2.5)
      //.intersect(cube([200,200,1]).translate([-100,-100,3]))
      //.intersect(cube([50,200,200]).translate([85,-100,-100])).rotateY(90)
      ;
}

//only add this wrapper if not already present & we are not in command-line mode
if(typeof wrappedMain === 'undefined' && typeof getParameterDefinitionsCLI !== 'undefined'){
  const wrappedMain = main
  main = function(){
    var paramsDefinition = (typeof getParameterDefinitions !== 'undefined') ? getParameterDefinitions : undefined
    return wrappedMain(getParameterDefinitionsCLI(paramsDefinition, {}))
  }
}
