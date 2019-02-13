const COL = 3;
const ROW = 3;
const R = 21;
const D = 3.5;
const W = 1;
const H = W;
const PH = 20;
const CURVATURE = 16; // affects time of rendering

function inner() {
  return sphere({
    r: R,
    center: [true, true, true],
    fn: CURVATURE
  });
}

function outer() {
  return sphere({
    r: R + W,
    center: [true, true, true],
    fn: CURVATURE
  });
}

function row(x,c=0) {
  var r = x();
  for (var i = 1; i < Math.round(ROW +.3 - (c%2)*.6) ; i++) {
    r = r.union(x().translate([0, i * (2 * R + D), 0]));
  }
  return r;
}

function plato(x) {
  var r = row(x);
  for (var i = 1; i < COL; i++) {
    r = r.union(row(x,i).translate([i * Math.sin(60*Math.PI/180)*(2 * R +D), (i % 2) * (R + D / 2), 0]));
  }
  return r;
}

function vrch(x) {
  var b = plato(outer).getBounds();
  var w = b[1].x - b[0].x;
  var h = b[1].y - b[0].y;
  return cube({
    size: [w - 2 * R - D / 2 + 2 * W, h - 2 * R - 2 * W - D / 2, x],
    center: [false, false, false]
  }).translate([-W / 2, W, 0]);
}

function pricka(x, y, a, d = Math.floor(Math.max(COL, ROW)) - 1) {
  return cube({
    size: [W, d * (2 * R + D), PH],
    center: [true, false, false]
  })
    .rotateZ(a)
    .translate([x * Math.sin(60*Math.PI/180)*(2 * R +D), y * (2 * R + D), 0]);
}

function pricky() {
  var r = pricka(0, 0, -60);
  for (var i = 1; i < Math.floor(ROW); i++) {
    r = r.union(pricka(0, i, -60));
  }
  for (var i = 2; i < COL - 1; i += 2) {
    r = r.union(pricka(i, 0, -60));
  }
  for (var i = 0; i < COL; i++) {
    r = r.union(pricka(i, (i % 2) * 0.5, 0, Math.round(ROW +.3 - (i%2)*.6) - 1));
  }
  for (var i = 1; i < ROW; i++) {
    r = r.union(pricka(0, i, 240));
  }
  for (var i = 1; i < COL - 1; i += 2) {
    r = r.union(pricka(i, Math.floor(ROW) - 0.5, 240));
  }
  return r.intersect(vrch(PH));
}

function main() {
  return union(plato(outer), pricky(), vrch(H)).subtract(
    plato(inner).union(
      cube({
        size: [1000, 1000, 1000],
        center: [true, true, true]
      }).translate([0, 0, -500])
    )
  );
}
