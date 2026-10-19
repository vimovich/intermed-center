const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const html = document.documentElement;
html.classList.remove('no-js');
html.dataset.v = '1.1';

/* active nav */
const norm = (p) => p.replace(/\.html$/, '').replace(/\/index$/, '/').replace(/\/+$/, '') || '/';
const here = norm(location.pathname);
$$('.nav a, .mnav__links a').forEach((a) => {
  const p = norm(new URL(a.href).pathname);
  if (p === here || (p !== '/' && here.startsWith(p)) || (a.dataset.also && a.dataset.also.split(',').some((x) => here === x))) {
    a.classList.add('is-active'); a.setAttribute('aria-current', 'page');
  }
});

/* header */
const hdr = $('[data-hdr]');
const onScroll = () => hdr?.classList.toggle('is-scrolled', scrollY > 6);
addEventListener('scroll', onScroll, { passive: true }); onScroll();

/* menu */
const burger = $('[data-burger]'), mnav = $('[data-mnav]');
const setMenu = (o) => { html.classList.toggle('menu-open', o); burger?.setAttribute('aria-expanded', String(o)); mnav?.setAttribute('aria-hidden', String(!o)); };
burger?.addEventListener('click', () => setMenu(!html.classList.contains('menu-open')));
mnav && $$('a', mnav).forEach((a) => a.addEventListener('click', () => setMenu(false)));
matchMedia('(min-width: 1081px)').addEventListener('change', (e) => e.matches && setMenu(false));

/* reveal */
const rio = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add('is-in'); rio.unobserve(e.target); } }), { threshold: 0.1, rootMargin: '0px 0px -30px 0px' });
$$('[data-reveal]').forEach((el) => rio.observe(el));

/* modal */
let lastFocus;
const openModal = (m) => { lastFocus = document.activeElement; m.classList.add('is-open'); m.setAttribute('aria-hidden', 'false'); html.style.overflow = 'hidden'; setTimeout(() => $('input', m)?.focus({ preventScroll: true }), 80); };
const closeModal = (m) => { m.classList.remove('is-open'); m.setAttribute('aria-hidden', 'true'); html.style.overflow = ''; lastFocus?.focus?.({ preventScroll: true }); };
const modal = $('[data-modal]');
document.addEventListener('click', (e) => {
  const b = e.target.closest('[data-book]');
  if (b && modal) {
    e.preventDefault(); setMenu(false);
    const f = $('form', modal); f.classList.remove('is-sent');
    const want = b.getAttribute('data-book'), sel = $('select', modal);
    if (sel) { const o = want && [...sel.options].find((o) => o.text.toLowerCase().includes(want.toLowerCase())); sel.value = o ? o.value : ''; }
    openModal(modal);
  }
  const c = e.target.closest('[data-close]'); if (c) closeModal(c.closest('.modal'));
});
document.addEventListener('keydown', (e) => { if (e.key === 'Escape') { $$('.modal.is-open').forEach(closeModal); setMenu(false); } });

/* forms */
const mask = (v) => {
  let d = v.replace(/\D/g, ''); if (d.startsWith('998')) d = d.slice(3); d = d.slice(0, 9);
  let o = '+998'; if (d.length) o += ' ' + d.slice(0, 2); if (d.length > 2) o += ' ' + d.slice(2, 5); if (d.length > 5) o += '-' + d.slice(5, 7); if (d.length > 7) o += '-' + d.slice(7, 9);
  return o;
};
$$('input[type=tel]').forEach((i) => {
  i.addEventListener('focus', () => { if (!i.value) i.value = '+998 '; });
  i.addEventListener('input', () => { i.value = mask(i.value); });
  i.addEventListener('blur', () => { if (i.value.trim() === '+998') i.value = ''; });
});
$$('form[data-form]').forEach((f) => {
  f.addEventListener('submit', (e) => {
    e.preventDefault();
    let ok = true;
    $$('[required]', f).forEach((i) => {
      let v = i.type === 'checkbox' ? i.checked : i.value.trim().length > 1;
      if (i.type === 'tel') v = i.value.replace(/\D/g, '').length === 12;
      (i.closest('.fld') || i.parentElement).classList.toggle('is-err', !v);
      if (!v) ok = false;
    });
    if (!ok) return;
    // TODO: connect Telegram bot / CRM webhook
    f.classList.add('is-sent'); setTimeout(() => f.reset(), 300);
  });
  f.addEventListener('input', (e) => (e.target.closest('.fld') || e.target.parentElement).classList.remove('is-err'));
});

/* horizontal strips: drag + arrows */
$$('[data-strip]').forEach((s) => {
  let down = false, x0 = 0, sl = 0, moved = false;
  s.addEventListener('pointerdown', (e) => { if (e.pointerType !== 'mouse') return; down = true; moved = false; x0 = e.clientX; sl = s.scrollLeft; s.classList.add('is-drag'); });
  addEventListener('pointermove', (e) => { if (!down) return; const dx = e.clientX - x0; if (Math.abs(dx) > 4) moved = true; s.scrollLeft = sl - dx; });
  addEventListener('pointerup', () => { if (!down) return; down = false; s.classList.remove('is-drag'); });
  s.addEventListener('click', (e) => { if (moved) { e.preventDefault(); e.stopPropagation(); } }, true);
  const id = s.id, ctr = id && $(`[data-for="${id}"]`);
  if (ctr) {
    const step = () => (s.firstElementChild?.getBoundingClientRect().width || 300) + 16;
    $('[data-prev]', ctr).addEventListener('click', () => s.scrollBy({ left: -step(), behavior: 'smooth' }));
    $('[data-next]', ctr).addEventListener('click', () => s.scrollBy({ left: step(), behavior: 'smooth' }));
  }
});

/* filter chips */
$$('[data-filter]').forEach((w) => w.addEventListener('click', (e) => {
  const b = e.target.closest('button'); if (!b) return;
  $$('button', w).forEach((x) => x.classList.toggle('is-active', x === b));
  const f = b.dataset.f;
  $$('[data-cat]').forEach((el) => el.classList.toggle('is-hidden', f !== 'all' && !el.dataset.cat.split(' ').includes(f)));
}));

/* counters */
$$('[data-count]').forEach((el) => {
  const io = new IntersectionObserver(([e]) => {
    if (!e.isIntersecting) return; io.disconnect();
    const to = parseFloat(el.dataset.count), t0 = performance.now();
    const step = (t) => { const p = Math.min((t - t0) / 1500, 1); el.firstChild.nodeValue = Math.round(to * (1 - Math.pow(1 - p, 3))).toLocaleString('ru-RU'); if (p < 1) requestAnimationFrame(step); };
    requestAnimationFrame(step);
  }, { threshold: 0.6 });
  io.observe(el);
});

/* 3D (lazy) */
const gl = (() => { try { const c = document.createElement('canvas'); return !!(c.getContext('webgl2') || c.getContext('webgl')); } catch { return false; } })();
const lazy = (el, fn) => { const io = new IntersectionObserver(([e]) => { if (e.isIntersecting) { io.disconnect(); fn(); } }, { rootMargin: '300px' }); io.observe(el); };
if (gl) {
  $$('[data-hero3d]').forEach((el) => lazy(el, async () => (await import('./scene3d.js')).mountHero(el)));
  $$('[data-heart3d]').forEach((el) => lazy(el, async () => {
    const root = el.closest('section');
    const pct = $('[data-scan-v]', root), bar = $('[data-scan-bar]', root), bpm = $('[data-bpm]', root);
    (await import('./scene3d.js')).mountHeart(el, {
      onScan(k) {
        if (pct) pct.textContent = Math.round(k * 100) + '%';
        if (bar) bar.style.setProperty('--w', 30 + k * 70 + '%');
        if (bpm && Math.random() < 0.08) bpm.textContent = 68 + Math.round(Math.random() * 6);
      },
    });
  }));
} else {
  $$('[data-hero3d], [data-heart3d]').forEach((el) => el.remove());
}
