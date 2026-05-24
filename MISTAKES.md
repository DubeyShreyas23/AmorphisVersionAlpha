# AMORPHIS — Mistakes & Lessons Learned
## Live Error Log | Updated in Real Time

> **Purpose:** Every bug, misconfiguration, wrong assumption, or gotcha encountered during development is logged here immediately. Before starting any new phase or sub-phase, this file is read top-to-bottom so mistakes are never repeated.

> **Repo:** https://github.com/DubeyShreyas23/AmorphisVersionAlpha.git

---

## 📋 HOW TO LOG A MISTAKE

```
### [PHASE X.Y] — Short title of the mistake
- **Branch:**      the branch it occurred on
- **Symptom:**     what went wrong / what error appeared
- **Root Cause:**  why it happened
- **Fix:**         exactly how it was resolved
- **Prevent:**     what to watch for in future phases
```

---

## ⚠️ STANDING RULES (never break these)

These are rules derived from known common pitfalls — logged before a single line of code is written.

### [STANDING-01] — Never commit directly to `main`
- **Rule:** All changes go through a secondary branch → PR → merge
- **Branch format:** `feat/`, `fix/`, `design/`, `perf/`, `qa/`, `deploy/`, `init/`
- **Prevent:** Before any `git commit`, verify you are NOT on `main` with `git branch`

### [STANDING-02] — Never commit `.env.local` or any secrets
- **Rule:** `.env.local` must be in `.gitignore` before first push
- **Prevent:** Run `cat .gitignore | grep .env` before first push to verify

### [STANDING-03] — Three.js / WebGL must be dynamically imported
- **Rule:** Never import Three.js or React Three Fiber at the top level in Next.js
- **Why:** Causes SSR crash — these are browser-only APIs
- **Fix:** Always use `dynamic(() => import(...), { ssr: false })`

### [STANDING-04] — pnpm lockfile must be committed
- **Rule:** Always commit `pnpm-lock.yaml` — never add it to `.gitignore`
- **Prevent:** CI will fail on dependency mismatch without the lockfile

### [STANDING-05] — Tailwind purge — custom class names must be safelisted
- **Rule:** Dynamically constructed class names (e.g. `text-${color}-500`) get purged
- **Fix:** Use `safelist` in `tailwind.config.ts` or use full class names in code

### [STANDING-06] — GSAP ScrollTrigger needs `ScrollTrigger.refresh()` after layout shifts
- **Rule:** Call `ScrollTrigger.refresh()` after any dynamic content loads (images, fonts)
- **Prevent:** Scroll animations will fire at wrong scroll positions otherwise

### [STANDING-07] — Sanity image URLs need the `urlFor()` builder — never use raw asset refs
- **Rule:** Raw Sanity image refs are not valid `<img>` src values
- **Fix:** Always pipe through `urlFor(image).url()` from `@sanity/image-url`

### [STANDING-08] — next/image requires explicit width/height or fill prop
- **Rule:** Missing dimensions causes a Next.js build error
- **Fix:** Use `fill` + a positioned parent, or provide explicit `width` and `height`

### [STANDING-09] — React Three Fiber Canvas must have explicit height
- **Rule:** An R3F `<Canvas>` inside a div with no height renders as 0px
- **Fix:** Parent div must have `height: 100vh` or explicit pixel height

### [STANDING-10] — Framer Motion `AnimatePresence` requires unique `key` on children
- **Rule:** Without a unique key, exit animations don't fire on route change
- **Fix:** Pass `key={pathname}` to the page wrapper inside `AnimatePresence`

---

## 🔴 PHASE ERRORS

### [HTML-01] — Footer base64 image prevents full footer replacement
- **Branch:** HTML prototype phase
- **Symptom:** The nav-brand and footer-brand divs contain huge embedded base64 JPEGs, making it impossible to use them as Edit tool anchor strings (too many tokens)
- **Root Cause:** Logo images were embedded as data URIs rather than external file references
- **Fix:** Added `footer-top` div BEFORE the `footer-inner` div, leaving the base64 content untouched. Used CSS overrides to reshape `footer-inner` into a bottom bar.
- **Prevent:** When embedding logos, always keep them in an external file (e.g. `/logo.png`) and reference by path. Embedding base64 makes surgical HTML edits extremely difficult.

### [HTML-02] — Token limit on file reads
- **Branch:** HTML prototype phase
- **Symptom:** Reading more than ~20 lines of the file at once hits token limits due to the embedded base64 images inflating per-line token counts
- **Root Cause:** Large data URIs in HTML attributes cause each line to have thousands of tokens
- **Fix:** Used `Grep` for targeted content discovery + `PowerShell Get-Content` with line-range selection for small targeted reads
- **Prevent:** Always use Grep + targeted reads when working with files containing base64 data URIs

### [HTML-03] — Cannot replace base64-laden hero-right block
- **Branch:** Phase 3 — 3D transformation
- **Symptom:** Wanted to swap the right-side static logo block for a 3D Three.js canvas. The `<div class="hero-right">` element contains a giant inline base64 JPEG (~80KB on one line), making it impossible to use as an Edit anchor.
- **Root Cause:** Same as HTML-01 — base64 data URI prevents string-based replacement on that block.
- **Fix:** Inserted the new `<div class="hero-3d-stage">` as a sibling BEFORE `<div class="hero-right">`, then added `style="display:none"` to the original hero-right inline. The grid (`grid-template-columns: 1fr 1fr`) ignores `display:none` children, so the layout snaps to the new stage cleanly.
- **Prevent:** When stuck on base64-blocked edits, prefer adding a sibling + hiding the original over trying to delete or replace the offending block.

### [HTML-04] — Three.js requires ES modules + importmap, not a plain script tag
- **Branch:** Phase 3 — 3D transformation
- **Symptom:** Modern Three.js (v0.150+) ships only as ESM; `<script src="three.min.js">` won't expose addons like `OrbitControls`.
- **Fix:** Used `<script type="importmap">` mapping `"three"` and `"three/addons/"` to unpkg URLs, then `<script type="module">` for scene code with normal `import` statements.
- **Prevent:** For any browser-side ES-module library, set up an importmap up front. Don't mix legacy `<script src>` with ESM imports.

### [HTML-06] — Three.js Group userData vs direct property
- **Branch:** Phase 3 — Dealmaker product demos
- **Symptom:** Forge section failed to initialize — `TypeError: Cannot read properties of undefined (reading 'tagline')`. Spec lookup `specs[variant.label]` returned undefined.
- **Root Cause:** `variant` was a `THREE.Group` instance. The label was stored on `variant.userData.label` (via `grp.userData = { label, accent }`), not as a direct property. So `variant.label` is undefined.
- **Fix:** Changed `specs[variant.label]` → `specs[variant.userData.label]`. Also added `!variant || !sp` guard at the top of setCard to fail soft.
- **Prevent:** When storing custom metadata on Three.js objects, ALWAYS use `.userData`. When reading back, ALWAYS go through `.userData` — never expect direct properties.

### [HTML-07] — TubeGeometry rebuild every frame causes GC stall
- **Branch:** Phase 3 — Dealmaker product demos (wire shape-memory animation)
- **Symptom:** Page becomes unresponsive (preview screenshots timeout, frames drop). Browser dev-tools showed garbage-collection pauses every ~50ms.
- **Root Cause:** Wire demo was rebuilding the entire `THREE.TubeGeometry` (60 segments × 16 radial = ~960 vertices) every frame via `new THREE.TubeGeometry(...)` + `geometry.dispose()`. ~58 allocate-and-dispose cycles per second.
- **Fix:** Pre-compute the TubeGeometry for BOTH target shapes once (curved + straight), keep their position arrays. Each frame, lerp the position values in-place into the working geometry's position attribute. Set `needsUpdate = true` and call `computeVertexNormals()`. Zero allocation per frame.
- **Prevent:** Never rebuild geometry every frame. Either deform vertex positions in-place (this approach), use a vertex shader to deform, or use morph targets. For animated meshes, always pre-allocate.

### [HTML-08] — Too many active WebGL contexts kills perf
- **Branch:** Phase 3 — Dealmaker product demos (10th scene added)
- **Symptom:** With ~10 simultaneous WebGL scenes (hero + sim×2 + forge + crystal-logo + hdrm + conf + 3 demos), framerate dropped well below 30fps. Screenshots timed out repeatedly.
- **Root Cause:** All scenes ran `requestAnimationFrame` continuously, even when scrolled off-screen. Each scene does its own GL state churn even if invisible.
- **Fix:** Added a shared `IntersectionObserver`-based visibility tracker. Each tick now checks `isVisible(canvas)` and skips both the resize + render if off-screen. The rAF loop continues (cheap), but actual GL work is gated. `rootMargin: '200px 0px'` so scenes warm up before entering viewport.
- **Prevent:** For any page with >2-3 WebGL contexts, gate per-scene render work by visibility. Don't trust the browser to throttle hidden tabs — explicit gating is more reliable.

### [HTML-05] — Existing 2D canvas draw loops still run after 3D replacement
- **Branch:** Phase 3 — 3D transformation
- **Symptom:** After hiding `#wireCanvas` and `#crystalCanvas` via CSS `display:none`, the original `draw()` loops still execute every frame.
- **Root Cause:** The 2D IIFEs were left in place to avoid risky edits to the existing inline `<script>` block.
- **Fix:** Acceptable — hidden canvases render off-screen with no visual effect, perf cost ~0.5ms/frame. Cleanup deferred to future pass.
- **Prevent:** When replacing canvases, either remove the 2D loops or guard with `if (!canvas.offsetParent) return;` at the top of each frame.

---

## ✅ PHASE COMPLETIONS

| Phase | Branch | Status | Notes |
|---|---|---|---|
| HTML Phase 1 — Modernization | `amorphis_.html` | ✅ Done | Loading screen, mobile nav, stats section, product filter, hysteresis graph, enhanced footer, scroll progress, back-to-top, toast system |
| HTML Phase 2 — ION-X Modernisation | `amorphis_.html` | ✅ Done | Slider −45→+75°C, austenite-white, removed wire annotations, cinematic 2D canvases, How-It-Works + Capabilities + Configurator sections |
| HTML Phase 3 — Full 3D Transformation | `amorphis_.html` | ✅ Done (2026-05-24) | Three.js v0.160 ESM, 6 WebGL scenes (Hero Living Wire, Sim 3D wire+lattice, Actuator Forge, Crystal Logo, HDRM Deployment, Configurator preview), Inter+JetBrains Mono+Space Grotesk typography, cyan accent system |
| Phase 0 — Foundation | `init/foundation` | ⏳ Pending | Next.js scaffold not yet started |
| Phase 1 — Design System | `design/system` | ⏳ Pending | — |
| Phase 2 — Core Architecture | `feat/core-architecture` | ⏳ Pending | — |
| Phase 3 — Hero & Simulations | `feat/hero-simulations` | ⏳ Pending | — |
| Phase 4 — Content Sections | `feat/content-sections` | ⏳ Pending | — |
| Phase 5 — Interactions & Haptics | `feat/interactions-haptics` | ⏳ Pending | — |
| Phase 6 — Performance & SEO | `perf/optimization` | ⏳ Pending | — |
| Phase 7 — Testing & QA | `qa/testing` | ⏳ Pending | — |
| Phase 8 — CI/CD & Deployment | `deploy/production` | ⏳ Pending | — |

---

*Document version: 1.0.0 | Amorphis — Shape Metal Alloys*
*This file lives alongside IMPLEMENTATION.md in the project root and is committed to every branch.*
