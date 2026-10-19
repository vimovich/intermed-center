# INTERMED CENTER — сайт многопрофильной клиники

Vite + Three.js. 11 страниц, собственные 3D-модели (ДНК, сердце со сканированием, 3D-иконки направлений).

- Страницы генерируются из данных: `python3 scripts/gen.py` (направления, врачи, чек-апы, цены, FAQ, блог)
- 3D-сердце: `node scripts/build-models.mjs` → `public/assets/heart.bin`
- 3D-иконки: `tools/icons.html?shape=heart` (рендер в `public/img/3d/*.webp`)

```bash
npm install
npm run dev
npm run build
```
