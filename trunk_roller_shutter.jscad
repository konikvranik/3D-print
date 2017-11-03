// source: trunk_roller_shutter.jscad

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
      obj = obj
                .subtract(cube({size : [ rx, ry, z ]}).translate([ x, y, 0 ]))
                .union(cylinder({r : r, h : z}).translate([ x + rx, y + ry, 0 ]));
    }
  }
  return obj;
}

function partHull(x, y, z, r1, r2) {
  var p = 50 - 2.5;
  var s = 7;  // posun středu kružnice
  var r = 40; // poloměr prostřední spodní kružnice
  return roundCorners(cube([ x, y, z ]), [ r1, 0, r2, r2 ])
      .subtract(cube([ 100, 100, z ]).translate([ 0, -100, 0 ]).rotate([ p, 0, 0 ], [ 0, 0, 1 ], 20))                                                                                // zkosit jednu stěnu
      .subtract(cube([ 10, 20, z ]).translate([ p - s, 0, 0 ]))                                                                                                                      // hole for bottom midle rounded corner
      .union(cylinder({r : r, h : z}).subtract(cube([ 2 * r, 2 * r, z ]).translate([ -r, 10, 0 ]).union(cube([ r, 2 * r, z ]).translate([ -r, -r, 0 ]))).translate([ p - s, r, 0 ])) // bottom midle rounded corner - not too smooth
      ;
}

/**
 * škvíra z boku
 **/
function slot(x, y, z) {
  return cube([ x, y - x / 2, z ]).union(cylinder({r : x / 2, h : z}).translate([ x / 2, y - x / 2, 0 ]));
}

function slotWalls(x, y, z, w) {
  return slot(x, y - w, z).subtract(cube([ x, y, z ]).translate([ 0, 3 * w, w ])).subtract(slot(x - 2 * w, y - 2 * w, z).translate([ w, 0, 0 ])).union(cube([ x, w, w ]).translate([ 0, 0, z ]))
}

function cornerCircle(d, w, z, s) {
  return cylinder({d : d - 2 * w, h : z - 2 * w}).expand(w, CSG.defaultResolution3D).subtract(cylinder({d : d - 2 * w, h : z})).subtract(cube([ d / 2, s, z ]).translate([ 0, -d / 2 + w, 0 ]));
}

function rolletHole(b, t, z, w) {
  return cube([ w, b, z ]).translate([ -w, -b, 0 ]);
}

function shell(x, y, z, w) {

  var r1 = 20 - w;
  var r2 = 10 - w;

  var rolletHoleFromTop = 11;
  var rolletHoleBottom = 10;
  var rolletHoleTop = 20;

  return partHull(x, y, z - 2 * w, r1, r2)
      .subtract(cube([ 15, 32, z ]).translate([ 0, y - 32 + w, 52 - 2 * w ]))                                         // vyříznout výsek
      .subtract(slot(12, 37 - w, 30).translate([ 25, 0, 0 ]))                                                         // vyříznout škvíru
      .subtract(rolletHole(rolletHoleBottom, rolletHoleTop, z, w).translate([ x, y + w - rolletHoleFromTop, 2 * w ])) // škvíra na roletu
      .expand(w, CSG.defaultResolution3D)
      .subtract(partHull(x, y, z, r1, r2).translate([ 0, 0, 0 ])) // vydlábnout vnitřek
      ;
}

function part(x, y, z, w) {
  var cc = cornerCircle(8, w, z, 2.5).mirroredY();

  return shell(x - 2 * w, y - 2 * w, z, w)
      .union(slotWalls(12, 37, 30 - w, w).translate([ 25, 0, 0 ]))
      .union(cc.translate([ 15, y - 4 - w, 0 ]))
      .union(cc.mirroredX().translate([ x - 4 - w, y - 4 - w, 0 ]))
      .translate([ w, w, w ]); // zalícovat s osama
}

function main() {
  CSG.defaultResolution3D = 8;
  return part(97, 68, 68, 2.5);
}
