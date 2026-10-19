import { BufferGeometry, BufferAttribute } from 'three';
import { MarchingCubes } from 'three/examples/jsm/objects/MarchingCubes.js';

export const clamp = (x, a, b) => Math.min(Math.max(x, a), b);
export function smin(a, b, k) { const h = clamp(0.5 + 0.5 * (b - a) / k, 0, 1); return b * (1 - h) + a * h - k * h * (1 - h); }
export function smax(a, b, k) { return -smin(-a, -b, k); }
export const sphere = (x, y, z, cx, cy, cz, r) => Math.hypot(x - cx, y - cy, z - cz) - r;
export function ellipsoid(x, y, z, rx, ry, rz) {
  const k0 = Math.hypot(x / rx, y / ry, z / rz), k1 = Math.hypot(x / (rx * rx), y / (ry * ry), z / (rz * rz));
  return k0 * (k0 - 1) / k1;
}
export function roundCone(px, py, pz, a, b, r1, r2) {
  const bax = b[0] - a[0], bay = b[1] - a[1], baz = b[2] - a[2];
  const l2 = bax * bax + bay * bay + baz * baz, rr = r1 - r2, a2 = l2 - rr * rr, il2 = 1 / l2;
  const pax = px - a[0], pay = py - a[1], paz = pz - a[2];
  const y = pax * bax + pay * bay + paz * baz, z = y - l2;
  const xx = pax * l2 - bax * y, xy = pay * l2 - bay * y, xz = paz * l2 - baz * y;
  const x2 = xx * xx + xy * xy + xz * xz, y2 = y * y * l2, z2 = z * z * l2;
  const k = Math.sign(rr) * rr * rr * x2;
  if (Math.sign(z) * a2 * z2 > k) return Math.sqrt(x2 + z2) * il2 - r2;
  if (Math.sign(y) * a2 * y2 < k) return Math.sqrt(x2 + y2) * il2 - r1;
  return (Math.sqrt(x2 * a2 * il2) + y * rr) * il2 - r1;
}

/** Polygonize an implicit function (negative inside) into a BufferGeometry. */
export function sdfGeometry(fn, { size = 2, res = 80, scaleField = 10, maxPoly = 140000 } = {}) {
  const mc = new MarchingCubes(res, { flatShading: false }, false, false, maxPoly);
  mc.isolation = 0;
  const n = mc.size, f = mc.field;
  for (let k = 0; k < n; k++) {
    const z = ((k - mc.halfsize) / mc.halfsize) * size;
    for (let j = 0; j < n; j++) {
      const y = ((j - mc.halfsize) / mc.halfsize) * size;
      for (let i = 0; i < n; i++) {
        const x = ((i - mc.halfsize) / mc.halfsize) * size;
        f[i + j * n + k * n * n] = -fn(x, y, z) * scaleField;
      }
    }
  }
  mc.update();
  const c = mc.count;
  const pos = mc.geometry.getAttribute('position').array.slice(0, c * 3);
  const nor = mc.geometry.getAttribute('normal').array.slice(0, c * 3);
  for (let i = 0; i < pos.length; i++) pos[i] *= size;
  const g = new BufferGeometry();
  g.setAttribute('position', new BufferAttribute(pos, 3));
  g.setAttribute('normal', new BufferAttribute(nor, 3));
  g.computeBoundingSphere();
  mc.geometry.dispose();
  return g;
}

/* ---------- shapes ---------- */
// Taubin heart (y up), tilted slightly like an anatomical heart icon
function taubin(x, y, z) {
  const a = x * x + 2.25 * z * z + y * y - 1;
  return a * a * a - x * x * y * y * y - 0.1125 * z * z * y * y * y;
}
export function heartFn(x, y, z) {
  const zz = z * 1.35;
  let d = ellipsoid(x - 0.5, y - 0.42, zz, 0.72, 0.68, 0.66);
  d = smin(d, ellipsoid(x + 0.5, y - 0.42, zz, 0.72, 0.68, 0.66), 0.2);
  d = smin(d, roundCone(x, y, zz, [0.42, 0.2, 0], [0, -1.25, 0], 0.66, 0.05), 0.35);
  d = smin(d, roundCone(x, y, zz, [-0.42, 0.2, 0], [0, -1.25, 0], 0.66, 0.05), 0.35);
  d = smax(d, -sphere(x, y, zz, 0, 1.22, 0, 0.34), 0.22);
  return d;
}

export function kidneyFn(x, y, z) {
  // bean: union of spheres along an arc, minus hilum notch
  let d = 1e9;
  for (let i = 0; i <= 10; i++) {
    const t = -1.05 + (i / 10) * 2.1;
    const cx = Math.sin(t) * 0.55 - 0.35, cy = Math.cos(t) * 0.0 + t * 0.78;
    d = smin(d, ellipsoid(x - (Math.cos(t) * 0.6 - 0.25), y - t * 0.72, z, 0.62, 0.55, 0.42), 0.25);
    void cx; void cy;
  }
  d = smax(d, -ellipsoid(x - 0.78, y, z, 0.42, 0.5, 0.6), 0.3);
  return d;
}

export function neuronFn(x, y, z) {
  let d = sphere(x, y, z, 0, 0, 0, 0.55);
  const dirs = [[1, 0.35, 0.2], [-0.9, 0.5, -0.3], [0.2, -1, 0.35], [-0.35, 0.95, 0.4], [0.5, 0.25, -1], [-0.6, -0.6, 0.6], [0.9, -0.55, -0.4]];
  for (const [a, b, c] of dirs) {
    const l = Math.hypot(a, b, c), ux = a / l, uy = b / l, uz = c / l;
    const tip = [ux * 1.55, uy * 1.55, uz * 1.55];
    d = smin(d, roundCone(x, y, z, [ux * 0.35, uy * 0.35, uz * 0.35], tip, 0.2, 0.05), 0.18);
    d = smin(d, sphere(x, y, z, tip[0], tip[1], tip[2], 0.1), 0.08);
  }
  return d;
}
