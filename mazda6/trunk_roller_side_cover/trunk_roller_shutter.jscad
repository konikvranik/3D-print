// source: trunk_roller_shutter.jscad

var EXPAND = true;
var SMOOTH = 0;

function expandIf(v, w) {
  var sc = [];
  var mv = [];
  var ax = [ 'x', 'y', 'z' ];
  for (var i = 0; i < ax.length; i++) {
    var s = v.getBounds()[1][ax[i]] - v.getBounds()[0][ax[i]];
    mv.push(((v.getBounds()[1][ax[i]] + v.getBounds()[0][ax[i]]) / s) * -w);
    sc.push((s + 2 * w) / s);
  }
  return EXPAND ? v.expand(w, fn(w)) : v.scale(sc).translate(mv);
}

function fn(r) { return SMOOTH * 2 * sqrt(r / 5); }

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
                .union(cylinder({r : r, h : z, fn : fn(r)}).translate([ x + rx, y + ry, 0 ]));
    }
  }
  return obj;
}

function rtCorner(x, y, z, w) {

  var c1 = cylinder({r : 4 - w, h : z, fn : fn(4 - w)});
  var c2 = cylinder({r : 16 - w, h : z, fn : fn(16 - w)});

  return c2.subtract(cube([ 16, 2 * 16, z ]).translate([ 9, -16, 0 ]))
      .subtract(cube([ 2 * 16, 9, z ]))
      .union(c1.translate([ 8, 9, 0 ]))
      .translate([ 0, -9, 0 ]);
}

function partHull(x, y, z, r1, r2, w) {
  var p = 50 - w;
  var r = 30; // poloměr prostřední spodní kružnice
  var r3 = 20;
  var s = 5.3;

  return roundCorners(cube([ x, y, z ]), [ r1, 0, 0, r2 ])

      .subtract(cube([ 50, 32.5 - w, z ]).translate([ 83.8 - w, 0, 0 ]))
      .union(cylinder({r : r3, h : z, fn : fn(r3)})
                 //.subtract(cube([ 2 * r3, r3, z ]).translate([ -r3, 0, 0 ]))
                 .translate([ x - r3, 32.5 - w, 0 ]))

      .subtract(cube([ 16, 16, z ]).translate([ 85 - w, y - 7 + w, 0 ]))
      .union(rtCorner(x, y, z, w).translate([ 85 - w, y - 7 + w, 0 ]))

      .subtract(
          cube([ 100, 100, z ]).translate([ 0, -100, 0 ]).rotate([ p, 0, 0 ], [ 0, 0, 1 ], 20)) // zkosit jednu stěnu
      .subtract(cube([ 10, 20, z ]).translate([ p - s, 0, 0 ])) // hole for bottom midle rounded corner
      .union(cylinder({r : r, h : z, fn : fn(r)})
                 .translate([ p - s, r, 0 ])) // bottom midle rounded corner - not too smooth
      ;
}

/**
 * škvíra z boku
 **/
function slot(x, y, z) {
  return cube([ x, y - x / 2, z ])
      .union(cylinder({r : x / 2, h : z, fn : fn(x / 2)}).translate([ x / 2, y - x / 2, 0 ]));
}

function slotWalls(x, y, z, w) {
  return slot(x, y - w, z)
      .subtract(cube([ x, y, z ]).translate([ 0, 3 * w, 9 - w ]))
      .subtract(slot(x - 2 * w, y - 2 * w, z).translate([ w, 0, 0 ]))
      .union(cube([ x, w, w ]).translate([ 0, 0, z ]))
}

function cornerCircle(d, w, z, s) {
  var v = cylinder({d : d - 2 * w, h : z, fn : fn(d / 2)});
  return expandIf(v, w)
      .subtract(cylinder({d : d - 2 * w, h : z + w, fn : fn(d / 2 - w)}))
      .subtract(cube([ d / 2, s, z + w ]).translate([ 0, -d / 2 + w, 0 ]));
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
  var v = partHull(x, y, z - 2 * w, r1, r2, w)
              .subtract(cube([ 16.5, 32, z ]).translate([ 0, y - 32 + w, 50 - 2 * w ])) // vyříznout výsek
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

  var r1 = 18 - w;
  var r2 = 14 - w;

  var dc = 8;
  var rc = dc / 2;

  var cc = cornerCircle(dc, 2, z - 2 * w, 2.5).mirroredY();

  return expandedHull(x, y, z, w, r1, r2, rolletHoleFromTop, rolletHoleTop)
      .subtract(partHull(x, y, z, r1, r2, w).translate([ 0, 0, 0 ])) // vydlábnout vnitřek
      .union(cc.translate([ 16.5, y - rc + w, 0 ]))
      .union(cc.mirroredX().rotateZ(-32).translate([ x - rc + w, y - rc + w - (rolletHoleFromTop - dc), 0 ]))
      .union(cc.rotateZ(-90).translate([ x - rc + w, y - rc + w - (rolletHoleFromTop + rolletHoleTop), 0 ]));
}

function buttonHole(w) {
  var r = 40;
  var cyl = cylinder({r : r, h : w, fn : fn(r)});
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
  var p = 50 - 2.5;
  var prolis = cube([ 9, 1.25, 24 ]);
  var screwHole = cylinder({d : 10, h : 20, fn : fn(5)});

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

      .union(cylinder({d : 19, h : 7 - w, fn : fn(19 / 2)})
                 .union(cylinder({d : 8, h : 20 - w, fn : fn(8 / 2)})
                            .subtract(cylinder({d : 5, h : 20 - w, fn : fn(5 / 2)}).translate([ 0, 0, 7 - w ])))
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
    {
      name : 'smooth',
      type : 'int',
      initial : 0,
      caption : "Smoothiness (if set to 0, general smoothiness is set to 2 and no corner expanding is done):",
      min : 0,
      max : 8,
      step : 1
    },
    {name : 'cuts', type : 'checkbox', checked : false, caption : "Produce sectioncuts:"}
  ];
}

function main(params) {

  EXPAND = params.smooth > 0;
  SMOOTH = EXPAND ? params.smooth : 14;

  var p = part(97, 68, 68, 2.5);

  if (params.cuts) {
    var cuts = [ 16, 33, 46, 57, 74, 76, 96.9 ];
    var result = [];
    var offset = 0;

    result.push(p.sectionCut(new CSG.OrthoNormalBasis(CSG.Plane.fromNormalAndPoint([ 0, 0, 1 ], [ 0, 0, 3 ]))));

    result.push(p.sectionCut(new CSG.OrthoNormalBasis(CSG.Plane.fromNormalAndPoint([ 0, 0, 1 ], [ 0, 0, 50 ])))
                    .translate([ 0, -100 - 100 * (offset++) ]));

    result.push(p.rotateX(-90)
                    .sectionCut(new CSG.OrthoNormalBasis(CSG.Plane.fromNormalAndPoint([ 0, 0, 1 ], [ 0, 0, -67 ])))
                    .translate([ 0, -100 - 100 * (offset++) ]));

    result.push(p.rotateX(-90)
                    .sectionCut(new CSG.OrthoNormalBasis(CSG.Plane.fromNormalAndPoint([ 0, 0, 1 ], [ 0, 0, -66 ])))
                    .translate([ 0, -100 - 100 * (offset++) ]));

    result.push(p.rotateX(-90)
                    .sectionCut(new CSG.OrthoNormalBasis(CSG.Plane.fromNormalAndPoint([ 0, 0, 1 ], [ 0, 0, -64 ])))
                    .translate([ 0, -100 - 100 * (offset++) ]));

    for (var i = 0; i < cuts.length; i++) {
      var o = [];
      vector_text(0, 0, "@" + cuts[i] + "mm")
          .forEach(function(pl) { o.push(rectangular_extrude(pl, {w : 1, h : 200}).translate([ -200, 0, -100 ])); });
      result.push(
          p.rotateY(90)
              .union(o)
              .sectionCut(new CSG.OrthoNormalBasis(CSG.Plane.fromNormalAndPoint([ 0, 0, 1 ], [ 0, 0, -cuts[i] ])))
              .translate([ 0, -100 - 100 * (i + offset) ]));
    }
    return result;
  } else {
    return p;
  }
}
