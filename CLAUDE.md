# World Map — Project Guide for AI Assistants

This file is the complete handoff document for working on this project. Read it fully before making changes. It captures the architecture, every non-obvious decision, past bugs and their fixes, and the owner's working conventions. Trust this file over assumptions.

## What this is

An Electron desktop app for learning world countries and capitals. Three tabs:
1. **World Map** — interactive D3 map with 2D (Natural Earth) and 3D (orthographic globe) modes, hover tooltips (flag, name, capital), zoom/pan (2D) or drag-rotate (3D)
2. **Country List** — 197 countries grouped by continent, collapsible sections, search, pronunciation mic buttons (Web Speech API), per-country "learned" checkmarks with per-continent progress bars
3. **Quiz** — three modes (Guess the Capital / Country / Flag), 10 questions per round, same-continent distractors, streaks, per-mode best scores

## Architecture — read this before touching anything

- **Single-file app**: ALL HTML, CSS, and JS live in `index.html` (~1500 lines). This is deliberate — do not split it into modules. `main.js` is only the Electron main process.
- **No build step, no framework, no bundler.** Vanilla JS + D3. Keep it that way.
- **`vendor/` pattern**: the only runtime dependencies are 3 files copied into `vendor/` (`d3.min.js`, `topojson-client.min.js`, `countries-110m.json`). The npm packages (`d3`, `topojson-client`, `world-atlas`) are devDependencies only and are NOT bundled by electron-builder. This keeps the shipped app ~500KB instead of 15MB. If you upgrade d3, re-copy the min file into `vendor/`.
- **`main.js` settings that matter**: `webSecurity: false` is required — the app `fetch()`es `vendor/countries-110m.json` from a `file://` URL, which Chromium blocks by default. `contextIsolation: true`, no nodeIntegration.
- **Theming**: every color is a CSS custom property. Dark theme in `:root`, light overrides in `[data-theme="light"]` on `<html>`. Theme switching is ONLY `setAttribute('data-theme', ...)` + localStorage — **never redraw the map on theme change** (see Bug #2 below). All SVG map elements use CSS classes (`.ocean`, `.graticule`, `.c-Africa`, etc.), never inline fill/stroke attributes, so themes propagate automatically.
- Accent gradient pair: `--accent` (blue) → `--accent-2` (violet). Quiz feedback colors: `--success`, `--danger`, `--gold` (all have `-dim` variants for backgrounds).

## Data model

- `COUNTRIES` array in `index.html`: 197 entries of `{id, iso2, name, capital, continent}`, grouped by continent in source order (list is re-sorted alphabetically at render time by `buildList()`).
- `id` is the numeric ISO 3166-1 code and MUST match the topojson geometry id. The topojson stores ids as **strings**; map code coerces with `+d.id` before `countryById.get(...)`. Keep ids numeric in COUNTRIES.
- **110m topojson resolution limits**: some territories don't exist as separate features. Verified: Falkland Islands (238) EXISTS in topojson; French Guiana (254) does NOT (merged into France, id 250) — not even in the 50m or 10m files. French Guiana is therefore drawn as a **hand-traced GeoJSON polygon** in `initMap()` (search `frenchGuianaGeo`), layered on top of France with class `country c-SouthAmerica` and its own tooltip handlers. Greenland (304) EXISTS.
- To verify whether an id exists in the topojson before adding a country:
  ```bash
  node -e "const t=require('./vendor/countries-110m.json'); console.log(t.objects.countries.geometries.map(g=>g.id).includes('NNN'))"
  ```
- `flagEmoji(iso2)` converts ISO2 → regional indicator emoji. Continent styling: `CONTINENT_CLASS` (CSS class names) and `CONTINENT_COLOR` (hex for list dots).

## Map implementation (`initMap()`)

- **Idempotent by design**: first line wipes the SVG (`innerHTML = ''`). Never append to the SVG outside `initMap()`. Resize calls it debounced (150ms).
- **2D mode**: `geoNaturalEarth1`, ocean = full-SVG `<rect>`, zoom/pan via `d3.zoom` applying a transform to the single `g.map-g` group. Everything zoomable (including the graticule) MUST be inside `g` (see Bug #3).
- **3D mode**: `geoOrthographic().clipAngle(90)`, ocean = a Sphere path inside `g` (so the globe floats on the app background, not a blue rectangle). Interactions:
  - `d3.drag` rotates the projection (`projection.rotate`), with sensitivity `75 / projection.scale()` so rotation slows when zoomed in; vertical rotation clamped to ±90°.
  - `d3.zoom` is **filtered to wheel events only** (`.filter(e => e.type === 'wheel')`) so drag is reserved for rotation; the zoom handler rescales the projection (`baseScale * transform.k`) and calls `redraw()` (re-runs `pathGen` on all paths). The zoom buttons (`zoomIn/zoomOut/zoomReset`) work in both modes because programmatic `scaleBy`/`transform` calls bypass the filter.
- Mode is persisted in localStorage `wm-map-mode`; toggle pill is top-right of the map (`#mode-2d` / `#mode-3d`, `syncModeButtons()`).
- The mode toggle can only be clicked when the map tab is visible, so `initMap()` is never called with a hidden (zero-size) container from there — preserve that invariant.

## Quiz implementation

- All state in `quizState` object; `QUIZ_MODES` config object defines prompt/flag/answer/option per mode — add new modes there.
- Distractors: 3 random countries from the **same continent** as the answer (this is a deliberate difficulty feature — don't "fix" it to global random).
- Answer matching in the option-highlight loop compares by button text vs `answerText`; correct answer flashes green, picked wrong answer shakes red, others dim. Auto-advance: 1200ms after correct, 2200ms after wrong (time to read the correct answer).
- `quitQuiz()`/`showQuizHome()` must `clearTimeout(quizState.timer)` — already handled; keep it if refactoring.
- Best scores: localStorage `wm-quiz-best` = `{capital: n, country: n, flag: n}`; labels updated by `updateBestLabels()` (called at init and on returning to quiz home).

## Learned tracking (Country List)

- localStorage `wm-learned` = JSON array of iso2 codes, loaded into a `Set` named `learned`.
- `toggleLearned(iso2, btn)` flips the set, saves, toggles `.learned` on the button and `.row-learned` on the row, then `refreshContinentProgress()` updates each continent header's progress bar + "n/54 learned" label.
- The table has 4 columns (Flag | Country | Capital | Learned) with `table-layout: fixed` and explicit widths on `thead th:nth-child(1..4)` — this is what keeps columns aligned across the six separate per-continent tables (Bug #5). If you add a column, update those widths.
- `.continent-progress` has `margin-left: auto` and `.continent-arrow` does NOT — the progress element does the right-alignment pushing. Don't re-add `margin-left: auto` to the arrow.

## All localStorage keys

| Key | Content |
|---|---|
| `wm-theme` | `'dark'` / `'light'` |
| `wm-map-mode` | `'2d'` / `'3d'` |
| `wm-learned` | JSON array of iso2 codes |
| `wm-quiz-best` | `{capital, country, flag}` best scores |

## Past bugs and their fixes — do not reintroduce

1. **Two maps stacked on top of each other** — `initMap()` appended without clearing; load + resize stacked layers. Fix: wipe SVG first line of `initMap()`, debounce resize.
2. **Map disappears after theme toggle from the list tab** — `toggleTheme()` used to call `initMap()` while `#map-wrap` was `display:none`, so `clientWidth/Height` were 0 → zero-size map. Fix: theme toggle touches ONLY the `data-theme` attribute; CSS variables restyle the SVG with no redraw. Never call `initMap()` when the map tab may be hidden.
3. **Gridlines didn't move when zooming** — graticule was appended to the SVG root while the zoom transform applied to `g`. Fix: `g` is created before the async topojson fetch and the graticule goes inside it. Everything zoomable lives in `g.map-g`.
4. **Pillow's ICO encoder mis-encodes multi-size icons** — `scripts/create_ico.py` builds the ICO binary manually with `struct.pack`. Don't replace it with `img.save(..., append_images=...)`.
5. **Capital column misaligned across continents** — each continent is its own `<table>`; without `table-layout: fixed` + explicit column widths they each auto-sized differently.
6. **French Guiana can't be a topojson feature** — see Data model; it's a hand-drawn polygon overlay.

## Build, packaging, release

- `npm start` — run the app. To restart after edits: `pkill -f "electron"; sleep 1; npm start &` (there is no hot reload).
- `npm run icon` — regenerates icons: `scripts/create_icon.py` (Pillow globe → `build/icon-1024.png`) → `scripts/build_icons.sh` (sips + iconutil → `.icns`; `create_ico.py` → `.ico`).
- electron-builder config lives in `package.json` `"build"`:
  - `asar: false`, `files` lists ONLY `main.js`, `index.html`, and the 3 vendor files.
  - **macOS builds ONE dmg with `"arch": ["arm64", "x64"]`** — the owner explicitly wants exactly 2 release artifacts (macOS + Windows), not per-arch DMGs.
  - Windows: NSIS x64, `oneClick: false`.
- **GitHub repo**: `https://github.com/abhinavp403/world-map-list` (branch `main`).
- **GitHub Actions** (`.github/workflows/`):
  - `build.yml` triggers ONLY on `workflow_dispatch` and `release: published` — the owner does NOT want CI running on every push. Don't add push triggers.
  - Owner's preferred workflow shape (use this pattern in future projects too): separate `build-mac` / `build-windows` jobs (not a matrix), Node 20, `npm ci`, build, `upload-artifact` named `World-Map-macOS` (path `dist/*.dmg`) / `World-Map-Windows` (path `dist/*.exe`).
  - Build commands must use `--publish never` (`npx electron-builder --mac --publish never`) — otherwise electron-builder sees the git tag and tries to auto-publish, failing with "GitHub Personal Access Token is not set".
  - macOS signing is disabled via `CSC_IDENTITY_AUTO_DISCOVERY: false` (no Apple developer credentials configured); the app gets an ad-hoc signature.
  - `test-build.yml` is also `workflow_dispatch`-only.
- Release process: create annotated tag `vX.Y.Z`, push it, then create a GitHub Release from it (the `release: published` event builds and attaches installers), or run the workflow manually from the Actions tab. Node 18 does NOT work (deps require Node 20+).

## Owner's conventions — follow these

- **Never commit or push unless explicitly asked.** When asked, commit messages are imperative one-liners describing the change.
- After every functional change, **restart the Electron app** so the owner can see it immediately (`pkill -f "electron"; sleep 1; npm start &`), and verify it's running (`pgrep -f electron`).
- The owner reviews visually — describe what changed and where to click.
- Emoji-flavored, sectioned summaries are welcome in chat, README, and release notes (see README.md and the v1.0.0 release description for the house style).
- Keep the app dependency-free at runtime. If a feature needs a library, ask first.
- Both themes must be supported by any new UI — use the CSS variables, never hardcoded colors.
- New persistent state goes in localStorage with a `wm-` prefixed key; document it in the table above.

## Verification checklist after changes

1. `node -e "new Function(require('fs').readFileSync('index.html','utf8').match(/<script>([\s\S]*)<\/script>/)[1])"` — syntax-checks the inline script.
2. Restart app, confirm process alive.
3. Manually exercise: both tabs render, theme toggle in both tabs, 2D↔3D toggle, resize window (map must not stack/disappear), search + collapse in list, one quiz round.
4. Check both dark and light themes for any UI you touched.
