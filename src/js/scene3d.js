import * as THREE from 'three';
import { RoomEnvironment } from 'three/examples/jsm/environments/RoomEnvironment.js';
import { dna, capsule, molecule, pearl, PALETTE } from './shapes.js';

const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
const isMobile = matchMedia('(max-width: 760px)').matches;

function baseRenderer(el, exposure = 1) {
  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' });
  renderer.setPixelRatio(Math.min(devicePixelRatio || 1, isMobile ? 1.5 : 1.75));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = exposure;
  renderer.localClippingEnabled = true;
  renderer.setClearColor(0, 0);
  renderer.domElement.setAttribute('aria-hidden', 'true');
  el.appendChild(renderer.domElement);
  const env = new THREE.PMREMGenerator(renderer).fromScene(new RoomEnvironment(), 0.04).texture;
  return { renderer, env };
}

function lifecycle(el, renderer, camera, frame, baseZ) {
  const resize = () => {
    const w = el.clientWidth || 1, h = el.clientHeight || 1;
    renderer.setSize(w, h, false);
    renderer.domElement.style.cssText = 'width:100%;height:100%;display:block';
    camera.aspect = w / h;
    camera.position.z = baseZ * Math.max(1, 0.9 / camera.aspect);
    camera.updateProjectionMatrix();
  };
  resize();
  new ResizeObserver(resize).observe(el);
  const ptr = { x: 0, y: 0, tx: 0, ty: 0 };
  addEventListener('pointermove', (e) => { ptr.tx = e.clientX / innerWidth - 0.5; ptr.ty = e.clientY / innerHeight - 0.5; }, { passive: true });
  let visible = true, raf = 0;
  const t0 = performance.now();
  const loop = () => {
    raf = 0;
    if (!visible || document.hidden) return;
    ptr.x += (ptr.tx - ptr.x) * 0.05; ptr.y += (ptr.ty - ptr.y) * 0.05;
    frame((performance.now() - t0) / 1000, ptr);
    renderer.render(frame.scene, camera);
    if (!reduce) raf = requestAnimationFrame(loop);
  };
  new IntersectionObserver(([e]) => { visible = e.isIntersecting; if (visible && !raf) loop(); }, { rootMargin: '120px' }).observe(el);
  document.addEventListener('visibilitychange', () => { if (!document.hidden && !raf) loop(); });
  loop();
  requestAnimationFrame(() => el.classList.add('is-ready'));
}

function lights(scene, tint = 0x9fe8ff) {
  const key = new THREE.DirectionalLight(0xffffff, 2.2); key.position.set(3, 5, 4);
  const rim = new THREE.DirectionalLight(tint, 2.2); rim.position.set(-5, 1, -3);
  const fill = new THREE.DirectionalLight(0xc7b8ff, 0.9); fill.position.set(-3, -3, 4);
  scene.add(key, rim, fill, new THREE.AmbientLight(0xffffff, 0.25));
}

/* ================= HERO: DNA + floating capsules & molecules ================= */
export function mountHero(el) {
  const { renderer, env } = baseRenderer(el, 0.95);
  const scene = new THREE.Scene();
  lights(scene);
  const camera = new THREE.PerspectiveCamera(30, 1, 0.1, 100);
  camera.position.set(0, 0, 12);

  const helix = dna(env, { pairs: isMobile ? 18 : 24, height: 7.2, twist: 2.6, radius: 1.0 });
  const hg = new THREE.Group(); hg.add(helix); hg.rotation.z = -0.42;
  scene.add(hg);

  const floaters = [];
  const add = (o, x, y, z, s, spin) => { o.position.set(x, y, z); o.scale.setScalar(s); o.userData = { base: o.position.clone(), spin, ph: Math.random() * 6 }; scene.add(o); floaters.push(o); };
  add(capsule(env, PALETTE.teal), 2.25, 1.55, 0.6, 0.85, [0.3, 0.5, 0.2]);
  add(capsule(env, PALETTE.lilac), -2.3, -1.9, 0.4, 0.75, [0.4, 0.2, 0.5]);
  add(molecule(env, 0.42), -2.05, 1.95, -0.6, 1, [0.2, 0.4, 0.1]);
  add(molecule(env, 0.34), 2.25, -2.15, -0.3, 1, [0.1, 0.3, 0.3]);
  const bubbleMat = pearl(0xffffff, env, { iridescence: 1, roughness: 0.04, opacity: 0.55 });
  for (let i = 0; i < (isMobile ? 5 : 9); i++) {
    const b = new THREE.Mesh(new THREE.SphereGeometry(1, 40, 28), bubbleMat);
    const a = (i / 9) * Math.PI * 2;
    add(b, Math.cos(a) * (2.6 + (i % 3) * 0.4), Math.sin(a * 1.3) * 2.6, -1 - (i % 2), 0.1 + (i % 4) * 0.05, [0, 0, 0]);
  }

  const frame = (s, p) => {
    helix.rotation.y = s * 0.35;
    hg.rotation.x = p.y * 0.25; hg.rotation.y = p.x * 0.4;
    hg.position.y = Math.sin(s * 0.8) * 0.08;
    for (const o of floaters) {
      const { base, spin, ph } = o.userData;
      o.position.x = base.x + p.x * 0.5 * (1 + base.z * 0.2);
      o.position.y = base.y + Math.sin(s * 0.9 + ph) * 0.14 - p.y * 0.3;
      o.rotation.x += spin[0] * 0.01; o.rotation.y += spin[1] * 0.01; o.rotation.z += spin[2] * 0.01;
    }
  };
  frame.scene = scene;
  lifecycle(el, renderer, camera, frame, 12);
}

/* ================= HEART SCAN (diagnostics) ================= */
async function loadBin(url) {
  const buf = await (await fetch(url)).arrayBuffer();
  const [vc, ic] = new Uint32Array(buf, 0, 2);
  const q = new Int16Array(buf, 8, vc * 3), off = 8 + vc * 6;
  const idx = vc < 65536 ? new Uint16Array(buf.slice(off, off + ic * 2)) : new Uint32Array(buf.slice(off, off + ic * 4));
  const pos = new Float32Array(vc * 3); for (let i = 0; i < pos.length; i++) pos[i] = (q[i] / 32767) * 2.5;
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.BufferAttribute(pos, 3)); g.setIndex(new THREE.BufferAttribute(idx, 1));
  g.computeVertexNormals();
  return g;
}

const holoShader = (color) => new THREE.ShaderMaterial({
  transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide, clipping: true,
  uniforms: { uColor: { value: new THREE.Color(color) }, uTime: { value: 0 } },
  vertexShader: `#include <clipping_planes_pars_vertex>
    varying vec3 vP; varying vec3 vN; varying vec3 vV;
    void main(){ vP = position; vec4 mvPosition = modelViewMatrix*vec4(position,1.0); vN = normalize(normalMatrix*normal); vV = normalize(-mvPosition.xyz); gl_Position = projectionMatrix*mvPosition;
    #include <clipping_planes_vertex>
    }`,
  fragmentShader: `#include <clipping_planes_pars_fragment>
    uniform vec3 uColor; uniform float uTime; varying vec3 vP; varying vec3 vN; varying vec3 vV;
    float ln(float v,float w){ float f=abs(fract(v)-0.5); return smoothstep(0.5-w,0.5,f); }
    void main(){
      #include <clipping_planes_fragment>
      float g = max(ln(vP.y*6.0,0.07), ln(atan(vP.z,vP.x)/6.2831*34.0,0.08));
      float fr = pow(1.0-abs(dot(normalize(vN),normalize(vV))),2.2);
      float a = (g*0.8 + fr*0.9 + 0.04) * (0.85+0.15*sin(uTime*2.0+vP.y*3.0));
      gl_FragColor = vec4(uColor*a, a);
    }`,
});

export async function mountHeart(el, { onScan } = {}) {
  const { renderer, env } = baseRenderer(el, 0.95);
  const scene = new THREE.Scene();
  lights(scene, 0x8fdcff);
  const camera = new THREE.PerspectiveCamera(30, 1, 0.1, 100);
  camera.position.set(0, 0.1, 9.5);
  const geo = await loadBin('/assets/heart.bin');
  const grp = new THREE.Group(); scene.add(grp);
  const solidMat = pearl(PALETTE.coral, env, { iridescence: 0.7 });
  const holoMat = holoShader(0x8fdcff);
  const clipA = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0), clipB = new THREE.Plane(new THREE.Vector3(0, -1, 0), 0);
  solidMat.clippingPlanes = [clipA]; holoMat.clippingPlanes = [clipB];
  grp.add(new THREE.Mesh(geo, solidMat), new THREE.Mesh(geo, holoMat));
  grp.rotation.set(0.1, -0.3, 0.18);

  const laser = new THREE.Mesh(new THREE.PlaneGeometry(8, 0.22), new THREE.ShaderMaterial({
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
    vertexShader: 'varying vec2 vUv; void main(){vUv=uv; gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0);}',
    fragmentShader: 'varying vec2 vUv; void main(){ float y=abs(vUv.y-0.5)*2.0; float a=(exp(-y*y*60.0)+exp(-y*y*6.0)*0.35)*smoothstep(0.0,0.25,vUv.x)*smoothstep(1.0,0.75,vUv.x); gl_FragColor=vec4(mix(vec3(0.56,0.86,1.0),vec3(1.0),exp(-y*y*60.0)*0.8)*a,a); }',
  }));
  const ring = new THREE.Mesh(new THREE.RingGeometry(1.75, 1.82, 96), new THREE.MeshBasicMaterial({ color: 0x8fdcff, transparent: true, opacity: 0.7, side: THREE.DoubleSide, blending: THREE.AdditiveBlending, depthWrite: false }));
  ring.rotation.x = -Math.PI / 2;
  scene.add(laser, ring);

  let last = 0;
  const frame = (s, p) => {
    grp.rotation.y = -0.3 + s * 0.3 + p.x * 0.3;
    const beat = 1 + Math.pow(Math.max(0, Math.sin(s * 5.2)), 12) * 0.035;
    grp.scale.setScalar(beat);
    const k = 0.5 - 0.5 * Math.cos(s * 0.55 + 1.6), y = -1.85 + k * 3.6;
    clipA.constant = -y; clipB.constant = y;
    laser.position.y = y; ring.position.y = y;
    laser.lookAt(camera.position.x, y, camera.position.z);
    holoMat.uniforms.uTime.value = s;
    if (onScan && s - last > 0.06) { last = s; onScan(k); }
  };
  frame.scene = scene;
  lifecycle(el, renderer, camera, frame, 9.5);
}
