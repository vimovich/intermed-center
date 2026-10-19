import { sdfGeometry, heartFn } from '../src/js/sdf.js';
import { mergeVertices } from 'three/examples/jsm/utils/BufferGeometryUtils.js';
import { writeFileSync } from 'node:fs';
function pack(g0, file) {
  g0.deleteAttribute('normal');
  const g = mergeVertices(g0, 1e-4);
  const pos = g.getAttribute('position').array, idx = g.getIndex().array, vc = pos.length / 3;
  const q = new Int16Array(pos.length); for (let i = 0; i < pos.length; i++) q[i] = Math.round(pos[i] / 2.5 * 32767);
  const ind = vc < 65536 ? new Uint16Array(idx) : new Uint32Array(idx);
  const buf = Buffer.concat([Buffer.from(new Uint32Array([vc, idx.length]).buffer), Buffer.from(q.buffer), Buffer.from(ind.buffer)]);
  writeFileSync(new URL(`../public/assets/${file}`, import.meta.url), buf);
  console.log(file, 'verts', vc, 'tris', idx.length / 3, 'kb', (buf.length / 1024).toFixed(0));
}
pack(sdfGeometry(heartFn, { size: 1.75, res: 92, scaleField: 10 }), 'heart.bin');
