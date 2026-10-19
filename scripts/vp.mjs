import { chromium } from 'playwright';
const [,, out, w, h, ...urls] = process.argv;
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'] });
const p = await b.newPage({ viewport: { width: +w, height: +h } });
p.on('pageerror', e => console.log('pageerror:', e.message));
await p.route(/images\.unsplash\.com|fonts\.|openstreetmap/, r => r.abort());
let i = 0;
for (const u of urls) { await p.goto(u, { waitUntil: 'load' }); await p.evaluate(() => document.querySelectorAll('[data-reveal]').forEach(e => e.classList.add('is-in'))); await p.waitForTimeout(2200); await p.screenshot({ path: `${out}-${i++}.png` }); }
await b.close();
