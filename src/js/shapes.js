import * as THREE from 'three';
import { RoundedBoxGeometry } from 'three/examples/jsm/geometries/RoundedBoxGeometry.js';
import { mergeGeometries } from 'three/examples/jsm/utils/BufferGeometryUtils.js';

export const PALETTE = {
  teal: 0x0fb3a6,
  tealDeep: 0x0a7d7a,
  aqua: 0x6fe0d4,
  ice: 0xeaf7f7,
  lilac: 0x9b8cff,
  coral: 0xff5d55,
  rose: 0xf47fae,
  ink: 0x0b1a2a,
};

/** Pearlescent "candy glass" — glossy, iridescent, no transmission (works on transparent canvases). */
export function pearl(color, env, o = {}) {
  return new THREE.MeshPhysicalMaterial({
    color: new THREE.Color(color),
    roughness: o.roughness ?? 0.16,
    metalness: o.metalness ?? 0.05,
    clearcoat: 1,
    clearcoatRoughness: 0.06,
    iridescence: o.iridescence ?? 0.9,
    iridescenceIOR: 1.35,
    iridescenceThicknessRange: [180, 620],
    sheen: 0.4,
    sheenColor: new THREE.Color(0xffffff),
    envMap: env,
    envMapIntensity: o.envI ?? 1.25,
    transparent: !!o.opacity,
    opacity: o.opacity ?? 1,
    vertexColors: !!o.vertexColors,
    side: o.side ?? THREE.FrontSide,
  });
}

/* ---------- DNA double helix ---------- */
export function dna(env, { pairs = 22, radius = 0.9, height = 6, twist = 3.2 } = {}) {
  const g = new THREE.Group();
  const strandMatA = pearl(PALETTE.teal, env, { iridescence: 1 });
  const strandMatB = pearl(PALETTE.lilac, env, { iridescence: 1 });
  const nodeMat = pearl(0xffffff, env, { iridescence: 1, roughness: 0.08 });
  const rungMats = [pearl(PALETTE.aqua, env), pearl(0xffffff, env), pearl(PALETTE.lilac, env), pearl(PALETTE.teal, env)];
  const ptsA = [], ptsB = [];
  const N = 120;
  for (let i = 0; i <= N; i++) {
    const t = i / N, a = t * Math.PI * 2 * twist, y = (t - 0.5) * height;
    ptsA.push(new THREE.Vector3(Math.cos(a) * radius, y, Math.sin(a) * radius));
    ptsB.push(new THREE.Vector3(Math.cos(a + Math.PI) * radius, y, Math.sin(a + Math.PI) * radius));
  }
  const tubeA = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(ptsA), 400, 0.085, 20), strandMatA);
  const tubeB = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(ptsB), 400, 0.085, 20), strandMatB);
  g.add(tubeA, tubeB);
  const sGeo = new THREE.SphereGeometry(0.15, 32, 24);
  const rGeo = new THREE.CylinderGeometry(0.045, 0.045, 1, 16);
  for (let i = 0; i < pairs; i++) {
    const t = (i + 0.5) / pairs, a = t * Math.PI * 2 * twist, y = (t - 0.5) * height;
    const pa = new THREE.Vector3(Math.cos(a) * radius, y, Math.sin(a) * radius);
    const pb = new THREE.Vector3(Math.cos(a + Math.PI) * radius, y, Math.sin(a + Math.PI) * radius);
    const na = new THREE.Mesh(sGeo, nodeMat); na.position.copy(pa);
    const nb = new THREE.Mesh(sGeo, nodeMat); nb.position.copy(pb);
    // two half rungs with different colours (base pairs)
    const mid = pa.clone().add(pb).multiplyScalar(0.5);
    for (const [from, mat] of [[pa, rungMats[i % 4]], [pb, rungMats[(i + 2) % 4]]]) {
      const r = new THREE.Mesh(rGeo, mat);
      const dir = mid.clone().sub(from);
      r.scale.y = dir.length();
      r.position.copy(from).add(dir.clone().multiplyScalar(0.5));
      r.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir.normalize());
      g.add(r);
    }
    g.add(na, nb);
  }
  return g;
}

/* ---------- two-tone capsule ---------- */
export function capsule(env, colorA = PALETTE.teal, colorB = 0xffffff, r = 0.32, len = 0.75) {
  const geo = new THREE.CapsuleGeometry(r, len, 16, 48);
  const col = [], pos = geo.getAttribute('position');
  const ca = new THREE.Color(colorA), cb = new THREE.Color(colorB);
  for (let i = 0; i < pos.count; i++) { const c = pos.getY(i) > 0.004 ? ca : cb; col.push(c.r, c.g, c.b); }
  geo.setAttribute('color', new THREE.Float32BufferAttribute(col, 3));
  const m = new THREE.Mesh(geo, pearl(0xffffff, env, { vertexColors: true, iridescence: 0.6 }));
  // seam ring
  const ring = new THREE.Mesh(new THREE.TorusGeometry(r * 1.005, 0.012, 8, 64), pearl(0xd8e6e6, env));
  ring.rotation.x = Math.PI / 2;
  const gg = new THREE.Group(); gg.add(m, ring);
  return gg;
}

/* ---------- molecule ---------- */
export function molecule(env, scale = 1) {
  const g = new THREE.Group();
  const atoms = [
    [0, 0, 0, 0.5, PALETTE.teal], [1.05, 0.55, 0.2, 0.34, 0xffffff], [-1.0, 0.6, -0.25, 0.34, 0xffffff],
    [0.15, -1.1, 0.3, 0.38, PALETTE.lilac], [-0.2, 0.25, 1.1, 0.3, PALETTE.aqua], [0.9, -1.75, 0.6, 0.24, 0xffffff],
    [-0.75, -1.8, 0.1, 0.24, 0xffffff],
  ];
  const bonds = [[0, 1], [0, 2], [0, 3], [0, 4], [3, 5], [3, 6]];
  const bGeo = new THREE.CylinderGeometry(0.08, 0.08, 1, 16);
  const bMat = pearl(0xe6f1f2, env);
  for (const [a, b] of bonds) {
    const pa = new THREE.Vector3(...atoms[a].slice(0, 3)), pb = new THREE.Vector3(...atoms[b].slice(0, 3));
    const d = pb.clone().sub(pa), m = new THREE.Mesh(bGeo, bMat);
    m.scale.y = d.length(); m.position.copy(pa).add(d.clone().multiplyScalar(0.5));
    m.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), d.normalize());
    g.add(m);
  }
  for (const [x, y, z, r, c] of atoms) {
    const s = new THREE.Mesh(new THREE.SphereGeometry(r, 48, 32), pearl(c, env, { iridescence: 1 }));
    s.position.set(x, y, z); g.add(s);
  }
  g.position.y = 0.55;
  g.scale.setScalar(scale);
  const w = new THREE.Group(); w.add(g); return w;
}

/* ---------- Venus symbol (gynecology) ---------- */
export function venus(env) {
  const mat = pearl(PALETTE.rose, env, { iridescence: 1 });
  const g = new THREE.Group();
  const ring = new THREE.Mesh(new THREE.TorusGeometry(0.75, 0.2, 40, 120), mat);
  ring.position.y = 0.45;
  const stem = new THREE.Mesh(new THREE.CapsuleGeometry(0.2, 1.0, 12, 32), mat);
  stem.position.y = -0.95;
  const bar = new THREE.Mesh(new THREE.CapsuleGeometry(0.2, 0.75, 12, 32), mat);
  bar.rotation.z = Math.PI / 2; bar.position.y = -0.9;
  g.add(ring, stem, bar);
  g.position.y = 0.2;
  return g;
}

/* ---------- medical cross ---------- */
export function cross(env, color = PALETTE.teal) {
  const a = new RoundedBoxGeometry(0.72, 2.1, 0.62, 6, 0.24);
  const b = new RoundedBoxGeometry(2.1, 0.72, 0.62, 6, 0.24);
  const geo = mergeGeometries([a.toNonIndexed(), b.toNonIndexed()]);
  geo.computeVertexNormals();
  return new THREE.Mesh(geo, pearl(color, env, { iridescence: 1 }));
}

/* ---------- test tube with liquid ---------- */
export function tube(env) {
  const g = new THREE.Group();
  const prof = [];
  const R = 0.42, H = 2.2;
  for (let i = 0; i <= 16; i++) { const a = (i / 16) * (Math.PI / 2); prof.push(new THREE.Vector2(Math.sin(a) * R, -H / 2 + R - Math.cos(a) * R)); }
  prof.push(new THREE.Vector2(R, H / 2), new THREE.Vector2(R + 0.07, H / 2 + 0.04), new THREE.Vector2(R + 0.07, H / 2 + 0.12));
  const glass = new THREE.Mesh(new THREE.LatheGeometry(prof, 64), pearl(0xf2fbff, env, { opacity: 0.32, roughness: 0.02, iridescence: 1, side: THREE.DoubleSide, envI: 1.6 }));
  const liq = [];
  const r2 = R * 0.86;
  for (let i = 0; i <= 16; i++) { const a = (i / 16) * (Math.PI / 2); liq.push(new THREE.Vector2(Math.sin(a) * r2, -H / 2 + R - Math.cos(a) * r2 + 0.02)); }
  liq.push(new THREE.Vector2(r2, 0.15), new THREE.Vector2(0, 0.15));
  const liquid = new THREE.Mesh(new THREE.LatheGeometry(liq, 64), pearl(PALETTE.teal, env, { iridescence: 0.4 }));
  const cap = new THREE.Mesh(new THREE.CylinderGeometry(R + 0.12, R + 0.12, 0.42, 48), pearl(PALETTE.lilac, env));
  cap.position.y = H / 2 + 0.3;
  g.add(liquid, glass, cap);
  g.rotation.z = -0.35;
  return g;
}

/* ---------- drop ---------- */
export function drop(env, color = PALETTE.aqua) {
  const pts = [];
  for (let i = 0; i <= 64; i++) {
    const t = i / 64, a = t * Math.PI;
    const r = Math.sin(a) * (1 - Math.cos(a) * 0.0) * Math.pow(Math.sin(a / 2), 1.4) * 1.05;
    pts.push(new THREE.Vector2(Math.max(r, 0.0001), 1.25 - t * 2.4));
  }
  const geo = new THREE.LatheGeometry(pts, 96);
  geo.computeVertexNormals();
  return new THREE.Mesh(geo, pearl(color, env, { iridescence: 1, roughness: 0.05 }));
}

export { mergeGeometries };
