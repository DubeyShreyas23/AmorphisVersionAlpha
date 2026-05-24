# AMORPHIS — Shape Metal Alloys
## End-to-End Website Implementation Plan
### Industry-Grade • Simulation-First • Deploy-Ready

---

> **Creative Direction:** Dark industrial luxury — molten metal aesthetics, morphing geometry, physics-driven interactions. Think liquid metal that solidifies into precision engineering. The site should feel like touching the future of materials science.

---

## 🔗 REPOSITORY

**GitHub:** https://github.com/DubeyShreyas23/AmorphisVersionAlpha.git

---

## 🌿 BRANCHING PROTOCOL (MANDATORY)

> **Rule:** `main` is NEVER committed to directly. Every change — no matter how small — goes through a secondary branch first, then merges into `main` via Pull Request.

### Branch Lifecycle (every phase & sub-phase):
```
1. git checkout main && git pull origin main       ← always start fresh from main
2. git checkout -b <branch-name>                   ← create secondary branch
3. [make all changes, commits on this branch]
4. git push origin <branch-name>                   ← push branch to GitHub
5. Open Pull Request on GitHub → review → merge    ← never skip this
6. git checkout main && git pull origin main       ← sync main after merge
7. Delete the feature branch (keep repo clean)
```

### Branch Naming Convention:
```
init/foundation
init/foundation-[sub]

design/system
design/system-[sub]

feat/[feature-name]
feat/[feature-name]-[sub]

perf/[area]
fix/[what-was-fixed]
qa/[what-was-tested]
deploy/[environment]
```

### PR Rules:
- Every PR must reference which Phase/Sub-phase it closes
- PR title format: `[Phase X.Y] Short description`
- Squash merge preferred — keeps main history clean
- Delete branch after merge

---

## 🐛 MISTAKES TRACKING

> All errors, gotchas, and lessons learned are logged in `MISTAKES.md` (co-located with this file).
> Before starting any new phase, the mistakes file is reviewed so past errors are not repeated.
> Every developer on the project is responsible for adding to it in real time.

---

## 📍 CURRENT STATUS

**Working on:** `amorphis_.html` — standalone HTML prototype (single file, no build step)

**HTML Phase 1 — COMPLETE ✅** (2026-05-24)
- ✅ Loading screen, scroll progress bar, mobile hamburger, active nav, back-to-top, toast system, enhanced footer
- ✅ Stats section (later removed per Phase 2)
- ✅ Product filter buttons (All / Pin Puller / HDRM / Ni-Ti Alloy)
- ✅ Initial Temperature–Strain Hysteresis Loop canvas in simulator

**HTML Phase 2 — COMPLETE ✅** (2026-05-24) — ION-X-inspired modernisation pass
- ✅ Removed "TRL 3 → 7 IN 24 MONTHS" item from ticker (both copies)
- ✅ Removed the SMA Advantage 4-cell stats section
- ✅ Removed wire-geometry annotation values (Length / Diameter / Contraction / State)
- ✅ Slider re-ranged to **−45°C → +75°C** with realistic Nitinol HT wire transition temperatures: Mf = −30°C · Ms = 0°C · As = +20°C · Af = +55°C
- ✅ Six rewritten phases (deep_martensite / martensite / armed / transition_start / transition / austenite) — physics-accurate strain & force values; strain now *decreases* with heating
- ✅ Austenite phase rendered in **#ffffff** (white) per request
- ✅ **Cinematic crystal canvas rewrite** — isometric polycrystalline grid of B2 unit cells with smooth monoclinic → cubic morphing, inter-atom bonds, travelling transformation wavefront, twin-boundary striations, spark particles, live transformation % readout
- ✅ **Cinematic hysteresis loop rewrite** — phase-region colour zones, gradient heating/cooling curves, animated trail of recent temperature path, pulsing marker with halo + crosshair guides + live readout pill
- ✅ **Cinematic wire canvas rewrite** — anchor mounts, hot-zone gradient, glow halo, current pulses, phase-front wave, heat-shimmer particles, frost crystals when cold
- ✅ **NEW section: How SMA Fires** — 4-step numbered process (Storage → Trigger → Transform → Fired) with SVG icons + spec meta lines
- ✅ **NEW section: Core Capabilities** — 6-card grid with SVG icons (zero shock / resettable / <2W / ITAR-free / 8% strain / domestic supply)
- ✅ **NEW section: Mission Configurator** — interactive calculator with 4 sliders (force / stroke / cycles / op-temp) that drives live wire-diameter sizing, length, trigger power, actuation time, housing mass, cycle margin, and recommended AMX family code

**HTML Phase 3 — COMPLETE ✅** (2026-05-24) — FULL 3D TRANSFORMATION (Three.js + WebGL)

The entire site is now powered by real-time Three.js 3D scenes. Six independent WebGL scenes,
custom GLSL shaders, cinematic lighting, scroll-driven assembly animations, and engineering-precision
typography overhaul. This is the "Impress investors" pass — the site went from a polished 2D
prototype to an industry-grade 3D engineering showroom.

### Foundation upgrade
- ✅ **Three.js v0.160** added via ES-module importmap (CDN, no build step) + OrbitControls addon
- ✅ **New typography:** Inter (UI body), Space Grotesk (display headers), JetBrains Mono (engineering labels), Black Han Sans retained for hero
- ✅ **Color system:** signature electric cyan `#7AE5FF` (active SMA / live state) + bronze `#D49B5C` (thermal) + lifted greys (`--steel`, `--muted`, `--chrome`) for WCAG-ready contrast
- ✅ **Font sizes:** mono labels minimum 11px (was 9-10px), body min 14px, headlines smoothed with antialiasing
- ✅ **Loader + scroll-progress + back-to-top** now use cyan accent gradient

### Six 3D scenes — built with Three.js + custom shaders

**① HERO — Living Nitinol Wire** (replaces static logo on right side)
- Full-bleed cinematic stage: hyper-realistic Nitinol wire (PhysicalMaterial with metalness 0.92, clearcoat, iridescence) suspended in space
- 32-cell inner crystal lattice glowing through the wire (additive blending octahedrons)
- 1200 particles with custom vertex/fragment shaders — heat-dust drift, cyan→ember color blend on fire
- Engineering wireframe rings (7 concentric, scroll-pulsing)
- Blueprint grid floor with custom shader (radial fade + line falloff)
- 3 dynamic lights (cyan key, bronze fill, cyan-soft rim) + ambient
- **Animation:** wire contracts 8% on fire, emissive ramps cyan→amber, breathing on idle, cursor parallax, auto-fire every 9 seconds + manual "FIRE ACTUATOR" button
- **Live readout pills:** material / temp / phase / strain / status — updates in real-time from animation state

**② SIMULATOR — 3D wire + 3D unit cell** (replaces 2D canvases #wireCanvas / #crystalCanvas which are now hidden via CSS)
- 3D wire (cylindrical, metallic) contracts with temperature slider — `window.__simTemp` global bridge
- 3D unit cell: 3×3×3 atomic lattice (Ni + Ti distinguished by material), monoclinic distortion at low temp, cubic perfect lattice at high temp, dynamic bonds redraw each frame
- **OrbitControls** on the crystal — user can drag to rotate (auto-rotate when idle)

**③ FORGE — Interactive Actuator Showroom** (NEW section inside #products)
- 6 procedurally-modelled actuator variants (NEXUS-HX flagship + 5 orbiters: PULSE-3K, BLADE-MX, ORBIT-S, STRIDER, HALO-MICRO)
- Each actuator built from primitives: body cylinder + tapered end caps + bolt heads (6-bolt hex pattern) + vertical flutes + accent torus ring with per-variant emissive color
- Orbital animation — variants orbit the flagship, spotlighted variant slides to centre-right
- **Click to spotlight** + control buttons below — left card shows flagship, right card shows selected
- Each card has spec sheet (force / stroke / cycles / TRL)
- Camera parallax follows cursor + slow drift

**④ TECH — Morphing Crystal Logo** (NEW header on #how-it-works)
- 1800 particles assemble from scattered orbit positions into a 6-fold hexagonal Amorphis logo
- Scroll-driven `uAssemble` uniform (0→1 as section enters viewport)
- Every 5 seconds: morphs from hexagonal (martensite/monoclinic) to 3D cubic lattice (austenite) and back
- Custom shader: positions interpolate between 3 targets (scatter / hex / lattice), additive blend, cyan→cyan-soft palette shift on morph
- Live phase tag updates synchronously

**⑤ ROADMAP — HDRM Space Deployment** (NEW cinematic header on #roadmap)
- Earth (8u sphere, deep blue with cloud band + atmosphere shell using custom rim-light shader, slow rotation)
- 1800 stars (custom shader with twinkle)
- Gold-foiled CubeSat 6U with antenna, vents, HDRM mount, fold-out solar panel (8 cell-grid lines)
- **4-phase sequence:** Orbit Insertion → HDRM Firing (cyan emissive flash + 80-particle burst) → Panel Deploying (hinge rotation π→0 with cubic easing) → Solar Acquisition (panel emissive ramps)
- Auto-loops every 12 seconds + manual REPLAY button
- Live telemetry counters (altitude wobble around 412km, velocity around 7.66 km/s)
- Phase label below stage updates to current sequence step

**⑥ CONFIGURATOR — Live 3D Actuator Preview** (inside #configurator output panel)
- Small reactive actuator that resizes in real-time as sliders move
- **Force** → body radius (0.28→0.55u over 1-20 kN)
- **Stroke** → body height (0.9→2.0u over 1-25 mm)
- **Cycles** → ring color (cyan→bronze, log-scale)
- **Temperature** → ring emissive intensity
- Slow auto-rotate + subtle vertical float

### Cross-cutting polish
- ✅ Cyan accent infused throughout: loader bar, scroll progress, KPI hover lines, stat-cell fills, timeline progress, completed TL dots
- ✅ CTA buttons get diagonal cyan sheen sweep on hover (`::before` overlay)
- ✅ Cards (`.prod-card`, `.team-card`, `.how-step`, `.cap-cell`) gain subtle cyan box-shadow on hover
- ✅ All 3D stages use cinematic radial-vignette + linear-fade overlay for depth
- ✅ Mobile fallbacks (max-width 768/600): 3D scenes shrink, info cards hide, layout collapses gracefully
- ✅ Section dividers (`section::before`) use centered gradient line for visual rhythm
- ✅ Tabular numerals (`font-variant-numeric: tabular-nums`) on all engineering data

### Technical notes
- All scenes wrap their init in `try/catch` so one failure can't break the page
- `sceneRegistry` keeps a reference to each (renderer/scene/camera/raf) for future cleanup
- `resizeRendererToDisplaySize` runs each frame for responsive resize without ResizeObserver overhead
- Pixel ratio clamped to `min(devicePixelRatio, 2)` for performance on retina + 4K
- `THREE.ACESFilmicToneMapping` everywhere for cinematic colour grading
- Custom shaders use `uTime` uniform for animation, `uPixelRatio` for crisp points at any DPR

**HTML Phase 3.5 — COMPLETE ✅** (2026-05-24) — Three Dealmaker Product Demos
- ✅ New section `#product-deepdive` between #products and #capabilities — alternating left/right rows
- ✅ **Pin Puller demo** (initPinPullerDemo): satellite wall + payload (gold box with antenna) + pin-puller actuator with cyan accent ring. 5-phase loop: ARMED → TRIGGER → PULL → RELEASE → RESET. Pin retracts smoothly; payload drifts away in zero-G with subtle rotation; heat particles emerge during firing; force arrow visible when armed.
- ✅ **HDRM demo** (initHdrmDemo): gold satellite body + solar panel + 4 corner HDRMs. 6-phase loop: STOWED → ARMED → FIRING → RELEASING → DEPLOYED → RESET. Panel pivots 180° with cubic ease; 4 actuators flash sync during firing; panel cells glow on deployed.
- ✅ **Ni-Ti Wire demo** (initWireDemo): curved memory shape (TubeGeometry) with internal lattice glow. 6-phase loop: SHAPE-SET → DEFORMING → DEFORMED → HEATING → RECOVERING → RECOVERED. Wire deforms from U-curve to straight (cold martensite), heats up (orange glow + heat particles rising), snaps back to memorized shape (austenite). Each phase updates strain (0-8%), temp (-25°C to +90°C), and phase label.
- ✅ Each stage has: cinematic label (top-left), live telemetry panel (top-right with 3 metrics), animated step indicator (bottom-center), click-to-restart, mouse parallax, blueprint floor grid.
- ✅ Visibility-gated rendering (IntersectionObserver, 200px margin) — scenes pause when off-screen. Critical for keeping ~10 simultaneous WebGL contexts performant.

**HTML Phase 4 — BACKLOG:**
- [ ] Product detail modal / drawer on card click (re-use Forge 3D model)
- [ ] Animated comparison table (scroll-triggered row reveals)
- [ ] Team card 3D flip (name/role → bio on hover)
- [ ] Newsletter / email capture section
- [ ] Keyboard nav improvements (focus traps in mobile menu, escape closes overlay)
- [ ] Add Forge + Configurator + Capabilities anchors to main nav
- [ ] WebGL feature detection + static-image fallbacks for unsupported browsers
- [ ] Replace `THREE.Points` shaders with `THREE.InstancedMesh` if particle counts grow further

---

## 🧭 MASTER OVERVIEW

```
AMORPHIS WEBSITE
├── Phase 0 — Foundation & Tooling        [Branch: init/foundation]
├── Phase 1 — Design System & Identity    [Branch: design/system]
├── Phase 2 — Core Architecture           [Branch: feat/core-architecture]
├── Phase 3 — Hero & Simulations          [Branch: feat/hero-simulations]
├── Phase 4 — Content Sections            [Branch: feat/content-sections]
├── Phase 5 — Interactions & Haptics      [Branch: feat/interactions-haptics]
├── Phase 6 — Performance & SEO           [Branch: perf/optimization]
├── Phase 7 — Testing & QA                [Branch: qa/testing]
├── Phase 8 — CI/CD & Deployment          [Branch: deploy/production]
└── Phase 9 — Post-Launch & Monitoring    [Branch: main (merge all)]
```

---

## PHASE 0 — FOUNDATION & TOOLING
### Branch: `init/foundation`

### 0.1 — Tech Stack Decision

| Layer | Choice | Reason |
|---|---|---|
| Framework | **Next.js 14** (App Router) | SSG/SSR hybrid, SEO, image optimization |
| Language | **TypeScript** | Type safety for complex simulation state |
| Styling | **Tailwind CSS + CSS Modules** | Utility + scoped component styles |
| 3D / Simulation | **Three.js + React Three Fiber** | WebGL metal simulations |
| Physics | **Rapier (via @react-three/rapier)** | Real-time physics for particle systems |
| Shaders | **GLSL custom shaders** | Molten metal, grain, iridescence effects |
| Animation | **GSAP + Framer Motion** | Page transitions + scroll choreography |
| CMS | **Sanity.io** | Headless CMS for products, blog, team |
| Forms | **React Hook Form + Zod** | Contact, inquiry, newsletter |
| Email | **Resend** | Transactional + marketing emails |
| Analytics | **Vercel Analytics + PostHog** | Privacy-first, funnel tracking |
| Deployment | **Vercel** | Edge network, preview deploys |
| Repo | **GitHub** | Version control, Actions CI/CD |
| Package Manager | **pnpm** | Faster, disk-efficient |

### 0.2 — Repository Setup

```bash
# Commands to run
pnpm create next-app@latest amorphis-web --typescript --tailwind --eslint --app
cd amorphis-web
git init
git remote add origin https://github.com/DubeyShreyas23/AmorphisVersionAlpha.git
git checkout -b init/foundation
```

**Files to create at root:**
- `.github/workflows/ci.yml` — lint, type-check, test on PR
- `.github/workflows/deploy-preview.yml` — Vercel preview on push
- `.github/workflows/deploy-prod.yml` — production on main merge
- `.eslintrc.json` — strict rules
- `.prettierrc` — consistent formatting
- `commitlint.config.js` — conventional commits
- `.husky/pre-commit` — lint-staged checks
- `CONTRIBUTING.md` — developer guide

### 0.3 — Project Structure

```
amorphis-web/
├── app/
│   ├── (marketing)/
│   │   ├── page.tsx               ← Home
│   │   ├── about/page.tsx
│   │   ├── products/page.tsx
│   │   ├── products/[slug]/page.tsx
│   │   ├── technology/page.tsx
│   │   ├── sustainability/page.tsx
│   │   ├── careers/page.tsx
│   │   └── contact/page.tsx
│   ├── (legal)/
│   │   ├── privacy/page.tsx
│   │   └── terms/page.tsx
│   ├── blog/
│   │   ├── page.tsx
│   │   └── [slug]/page.tsx
│   ├── api/
│   │   ├── contact/route.ts
│   │   ├── newsletter/route.ts
│   │   └── revalidate/route.ts
│   ├── layout.tsx
│   ├── not-found.tsx
│   └── error.tsx
├── components/
│   ├── three/                     ← All WebGL/Three.js
│   ├── sections/                  ← Page sections
│   ├── ui/                        ← Reusable primitives
│   ├── layout/                    ← Nav, Footer, etc.
│   └── animations/                ← GSAP/Framer wrappers
├── lib/
│   ├── sanity/                    ← CMS client + queries
│   ├── hooks/                     ← Custom React hooks
│   ├── utils/                     ← Helpers
│   └── constants/
├── shaders/                       ← .vert .frag GLSL files
├── public/
│   ├── fonts/
│   ├── models/                    ← .glb 3D models
│   ├── textures/                  ← Metal PBR textures
│   └── videos/
├── styles/
│   ├── globals.css
│   └── tokens.css                 ← CSS custom properties
└── sanity/                        ← Sanity Studio (co-located)
```

### 0.4 — Environment Variables

```env
# .env.local (never commit)
NEXT_PUBLIC_SANITY_PROJECT_ID=
NEXT_PUBLIC_SANITY_DATASET=
SANITY_API_TOKEN=
NEXT_PUBLIC_POSTHOG_KEY=
RESEND_API_KEY=
NEXT_PUBLIC_SITE_URL=
NEXT_PUBLIC_GA_ID=
```

**→ Git commit:** `chore: initialize project scaffold and tooling`
**→ Push to `init/foundation`, open PR → merge to `main`**

---

## PHASE 1 — DESIGN SYSTEM & IDENTITY
### Branch: `design/system`

### 1.1 — Visual Identity

**Aesthetic Direction:** *Liquid Metal Industrialism*
- Dark backgrounds with barely-there warm charcoal tones
- Molten gold/amber accents — like heated alloy
- Cold steel blues for technical data
- Iridescent surface effects on hover

**Color Tokens:**
```css
/* styles/tokens.css */
:root {
  /* Base */
  --color-void:        #080808;
  --color-forge:       #111010;
  --color-carbon:      #1A1918;
  --color-slag:        #2C2A28;
  --color-oxide:       #3F3C39;

  /* Metal surfaces */
  --color-steel:       #8C9BA8;
  --color-chrome:      #BFC8D0;
  --color-platinum:    #E8EBEE;

  /* Heat / accent */
  --color-ember:       #C84B0F;
  --color-molten:      #E8841A;
  --color-gold:        #F5C842;
  --color-plasma:      #FFE599;

  /* Technical */
  --color-cyan-cold:   #4ECDC4;
  --color-data-blue:   #3B82F6;

  /* Semantic */
  --color-bg:          var(--color-void);
  --color-surface:     var(--color-forge);
  --color-border:      var(--color-slag);
  --color-text:        var(--color-platinum);
  --color-muted:       var(--color-steel);
  --color-accent:      var(--color-molten);
  --color-accent-alt:  var(--color-gold);

  /* Typography Scale */
  --font-display:      'Neue Montreal', 'PP Neue Montreal', sans-serif;
  --font-body:         'Söhne', 'Helvetica Neue', sans-serif;
  --font-mono:         'Commit Mono', 'JetBrains Mono', monospace;

  /* Spacing Scale (8pt grid) */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-6: 1.5rem;
  --space-8: 2rem;
  --space-12: 3rem;
  --space-16: 4rem;
  --space-24: 6rem;
  --space-32: 8rem;

  /* Motion */
  --ease-metal:        cubic-bezier(0.25, 0.46, 0.45, 0.94);
  --ease-forge:        cubic-bezier(0.77, 0, 0.175, 1);
  --ease-spring:       cubic-bezier(0.34, 1.56, 0.64, 1);
  --duration-fast:     120ms;
  --duration-base:     240ms;
  --duration-slow:     480ms;
  --duration-cinematic: 1200ms;
}
```

### 1.2 — Typography

**Font Pairings:**
- **Display:** PP Neue Montreal (headings, hero) — geometric, engineered feel
- **Body:** Söhne (body copy) — warm, readable precision
- **Mono:** Commit Mono (data, specs, code) — technical readouts

```tsx
// app/layout.tsx font setup
// Self-host via next/font/local for performance
```

**Type Scale:**
```
Display XL:  96px / line-height 0.95 / tracking -0.04em
Display L:   72px / line-height 0.97 / tracking -0.03em
H1:          56px / line-height 1.05 / tracking -0.02em
H2:          40px / line-height 1.1  / tracking -0.01em
H3:          28px / line-height 1.2
Body L:      18px / line-height 1.65
Body:        16px / line-height 1.6
Caption:     13px / line-height 1.4  / tracking 0.04em (uppercase)
Mono:        14px / line-height 1.5
```

### 1.3 — Component Primitives

Build in order:
1. `<Button>` — 3 variants: primary (ember glow), ghost, outline-metal
2. `<Badge>` — for tags, statuses, material specs
3. `<Card>` — product cards, blog cards, team cards
4. `<Input>` / `<Textarea>` — with focus glow effect
5. `<Divider>` — horizontal rule with gradient fade
6. `<Tag>` — filterable taxonomy tags
7. `<Tooltip>` — technical spec callouts
8. `<Modal>` / `<Drawer>` — overlay system
9. `<Skeleton>` — loading states matching shapes
10. `<Icon>` — wrapper for custom SVG icon set

### 1.4 — Motion System

```tsx
// lib/motion.ts — shared animation variants
export const fadeUp = {
  hidden: { opacity: 0, y: 24 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.6, ease: [0.25, 0.46, 0.45, 0.94] } }
}

export const staggerChildren = {
  visible: { transition: { staggerChildren: 0.08 } }
}

export const metalReveal = {
  hidden: { clipPath: 'inset(0 100% 0 0)' },
  visible: { clipPath: 'inset(0 0% 0 0)', transition: { duration: 1.2, ease: [0.77, 0, 0.175, 1] } }
}
```

**→ Git commit:** `design: add design system tokens, typography, and component primitives`
**→ Push to `design/system`, open PR → merge to `main`**

---

## PHASE 2 — CORE ARCHITECTURE
### Branch: `feat/core-architecture`

### 2.1 — Navigation

**Desktop Nav:**
- Fixed top bar, height 72px
- Logo left (animated SVG mark — morphing amorphous shape)
- Nav links center with hover underline that slides in from left
- CTA button right: "Get Quote" (ember accent)
- On scroll > 100px: backdrop-blur glass effect activates
- Active link indicator: thin amber line beneath

**Mobile Nav:**
- Hamburger → full-screen overlay
- Links appear staggered with slide-from-right
- Background: full bleed dark with faint metal texture
- Close button morphs from hamburger

**Sub-navigation (mega menu for Products):**
- Triggered on hover/focus
- Shows product categories with mini 3D preview thumbnails
- Animated border that draws around hovered item

### 2.2 — Footer

**Structure:**
```
[Logo + tagline]          [Products]    [Company]    [Resources]
[Social links]            [Technology]  [About]      [Blog]
[Newsletter signup]       [Alloys]      [Careers]    [Docs]
                          [Custom]      [Contact]    [Downloads]

[Copyright] [Privacy] [Terms] [ISO Badges] [Certifications]
```

**Visual:** Faint topographic contour map of a metal grain structure as footer background texture.

### 2.3 — Page Transitions

```tsx
// Using Framer Motion AnimatePresence
// Each page: fade + slight Y shift (12px)
// Duration: 400ms with ease-forge curve
// Custom loading bar at top (like NProgress but custom styled in ember color)
```

### 2.4 — SEO & Metadata Infrastructure

```tsx
// app/layout.tsx
export const metadata: Metadata = {
  metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL),
  title: { template: '%s | Amorphis', default: 'Amorphis — Shape Metal Alloys' },
  description: '...',
  openGraph: { images: ['/og-image.png'] },
  twitter: { card: 'summary_large_image' },
  // ... full config
}
```

- `app/sitemap.ts` — auto-generated sitemap
- `app/robots.ts` — robots.txt
- JSON-LD structured data for: Organization, Product, Article, BreadcrumbList

### 2.5 — Sanity CMS Schema Design

**Content Types:**
```
Product
  - title, slug, tagline
  - category (enum: structural, aerospace, automotive, marine, custom)
  - composition (array of elements with percentages)
  - properties: { tensile, yield, hardness, density, meltingPoint }
  - applications (array)
  - gallery (images)
  - datasheet (PDF upload)
  - certifications

BlogPost
  - title, slug, excerpt
  - author (reference → Author)
  - publishedAt, updatedAt
  - categories
  - body (Portable Text)
  - featuredImage

TeamMember
  - name, role, department
  - bio, photo
  - linkedIn

Testimonial / Case Study
  - company, industry
  - challenge, solution, result
  - metrics (key numbers)

Certification
  - name, issuer, logoImage, validUntil

JobPosting
  - title, department, location, type
  - description (Portable Text)
  - applicationLink
```

**→ Git commit:** `feat: add nav, footer, page transitions, SEO, and CMS schemas`
**→ Push to `feat/core-architecture`, open PR → merge to `main`**

---

## PHASE 3 — HERO & SIMULATIONS
### Branch: `feat/hero-simulations`

> This is the crown jewel phase. The simulations define the brand.

### 3.1 — Hero Section (Homepage)

**Concept:** *"Amorphis"* means without fixed form. The hero visualizes an amorphous metal alloy — shifting, morphing, crystallizing, then settling into precision.

**Hero Layout:**
```
[Full-viewport]
  └── WebGL Canvas (full bleed background)
        ├── Molten metal fluid simulation
        ├── Crystallization particle effect on load
        └── Mouse-reactive surface ripples

  └── Foreground content (centered, z-index above canvas)
        ├── Eyebrow: "Advanced Materials Engineering"
        ├── H1: "Metal That Thinks" (character-by-character reveal)
        ├── Subhead: one-liner value proposition
        ├── CTAs: [Explore Alloys] [Request Samples]
        └── Scroll indicator: animated chevron + "Scroll to discover"
```

**WebGL Hero Simulation — `MoltenHero.tsx`:**
```glsl
/* Vertex Shader: molten-hero.vert */
// Perlin noise displacement on sphere geometry
// Creates organic, breathing surface movement
// Parameters: time, mouse position, amplitude

/* Fragment Shader: molten-hero.frag */
// PBR-lite metal shading
// Fresnel rim lighting (ember color at edges)
// Animated heat shimmer / chromatic aberration
// Iridescent thin-film interference effect
// Noise-based surface variation (scratches, grain)
```

**Implementation:**
```tsx
// components/three/MoltenHero.tsx
// - React Three Fiber Canvas
// - OrbitControls disabled, custom mouse tracking
// - useFrame for animation loop
// - Postprocessing: Bloom (ember glow), ChromaticAberration, Noise
// - Responsive: reduces geometry complexity on mobile
// - Suspense boundary with custom loader
```

### 3.2 — Material Simulation Section

**Concept:** Interactive property explorer — user selects a material condition (temperature, stress, composition) and watches the microstructure simulation update in real time.

**Components:**
```
MaterialSimulator/
├── SimulationCanvas.tsx      ← Three.js grain boundary visualization
├── ParameterControls.tsx     ← Sliders for temp, stress, composition %
├── PropertyReadout.tsx       ← Live updating specs (mono font)
└── PhaseDisplay.tsx          ← Crystal phase diagram overlay
```

**Simulation Detail:**
- Voronoi-based grain boundary mesh that responds to temperature slider
- Grain size shrinks/grows with temperature (Hall-Petch relationship)
- Color maps to actual material property (stress = rainbow heatmap)
- Particle system shows dislocation movement under stress
- "Crystallize" button — triggers dramatic phase transformation animation

### 3.3 — Manufacturing Process Visualization

**Concept:** Scroll-driven story of how Amorphis creates its alloys.

```
Scroll 0%:   Raw materials floating (particle system)
Scroll 20%:  Materials converge into crucible
Scroll 40%:  Melting — liquid metal simulation activates
Scroll 60%:  Rapid quenching — crystallization freeze
Scroll 80%:  Precision shaping — geometry morphs into product form
Scroll 100%: Final product with spec labels appearing
```

**Tech:** GSAP ScrollTrigger + Three.js morph targets

### 3.4 — Particle Field Background

**Used across multiple sections:**
- ~2000 small metal fragment particles
- Float slowly with Brownian motion
- On mouse proximity: repel (haptic-feel)
- On click: brief explosive scatter + reconvergence
- Color: dim steel with occasional gold flash

### 3.5 — Loading Screen

```
[Full black screen]
  └── Amorphis logo mark: draws via SVG stroke animation (2s)
  └── Progress bar: thin amber line fills from left (actual load progress)
  └── Loading label: rotating technical phrases in mono font
        "Initializing crystal lattice..."
        "Loading grain boundaries..."
        "Calibrating tensile modules..."
  └── Fade out: entire screen dissolves upward revealing site
```

**→ Git commit:** `feat: hero WebGL simulation, material explorer, scroll storytelling`
**→ Push to `feat/hero-simulations`, open PR → merge to `main`**

---

## PHASE 4 — CONTENT SECTIONS
### Branch: `feat/content-sections`

### 4.1 — Homepage Sections (in order)

```
1. [HERO]               Full viewport — molten simulation
2. [NUMBERS]            Key stats: animated counters on scroll
                        "47 Alloy Variants" / "99.7% Purity" / "12 Industries" / "Since 1998"
3. [PRODUCTS GRID]      3-column cards with 3D preview on hover
4. [MATERIAL SIM]       Interactive simulation explorer
5. [PROCESS]            Scroll-driven manufacturing story
6. [WHY AMORPHIS]       3-column feature blocks with icon animations
7. [CASE STUDIES]       Horizontal scroll carousel — client success stories
8. [CERTIFICATIONS]     Scrolling logo ticker — ISO, ASTM, AMS badges
9. [BLOG PREVIEW]       Latest 3 articles
10.[CTA BANNER]         Full-width dark section — "Ready to Spec Your Material?"
11.[FOOTER]
```

### 4.2 — Products Page

**Layout:**
- Filter bar: All / Structural / Aerospace / Automotive / Marine / Custom
- Filter animation: cards rearrange with FLIP animation
- Grid: 3 columns desktop, 2 tablet, 1 mobile
- Each card:
  - Animated WebGL preview (small canvas per card — lazy loaded)
  - Alloy designation (e.g., AMX-7042)
  - Key property highlights (3 badges)
  - Hover: card lifts, subtle glow, "View Specs →"

**Product Detail Page:**
- Hero: large 3D model viewer (interactive, orbit-able)
- Properties panel: tabular spec sheet with visual bar charts
- Composition visualizer: pie chart of element makeup
- Applications grid: industry icons with use-case descriptions
- Related products: horizontal scroll
- Download section: datasheet PDF, SDS, certifications
- Inquiry CTA: sticky sidebar or bottom bar on mobile

### 4.3 — Technology Page

**Sections:**
1. Hero with process animation
2. R&D capabilities — parallax image reveal
3. Patents & IP — animated number + title cards
4. Lab equipment showcase — horizontal scroll with 3D model previews
5. Quality control process — interactive flowchart
6. Material testing standards — expandable accordion

### 4.4 — About Page

**Sections:**
1. Brand story — editorial layout with large type
2. Timeline — horizontal scroll, year-by-year milestones with subtle parallax
3. Team grid — cards with hover flip (name/role front, bio back)
4. Culture / values — icon + short copy, staggered reveal
5. Offices / facilities — interactive map (Mapbox GL)

### 4.5 — Sustainability Page

**Sections:**
1. Impact hero — animated data visualization (emissions/energy saved)
2. Material efficiency — interactive infographic
3. Certifications — animated badge grid
4. Goals / commitments — progress bars animating to target %
5. Reports — downloadable PDF cards

### 4.6 — Careers Page

**Sections:**
1. Culture hero
2. Benefits grid — icon cards
3. Open positions — filterable by department/location
4. Each job → modal with full description + apply button (links to ATS)

### 4.7 — Contact Page

**Layout:**
- Left: Contact form (name, company, message, material interest)
- Right: Office addresses, email, phone, embedded map
- Form submission: optimistic UI → success animation (metal crystallization)
- Validation: Zod schema, inline error states
- Submission: Resend API → confirmation email

### 4.8 — Blog

- List: masonry grid, featured post full-width at top
- Article: editorial layout, estimated read time, table of contents (sticky sidebar)
- Categories: tag filtering
- Related articles at bottom

**→ Git commit:** `feat: all page sections — products, about, technology, contact, blog`
**→ Push to `feat/content-sections`, open PR → merge to `main`**

---

## PHASE 5 — INTERACTIONS & HAPTICS
### Branch: `feat/interactions-haptics`

### 5.1 — Haptic Feedback System

```tsx
// lib/hooks/useHaptics.ts
// Web Vibration API wrapper with fallback
// Patterns:
//   'light'  → 10ms (button tap)
//   'medium' → 20ms (card select)
//   'heavy'  → [30, 10, 30] (form submit)
//   'success'→ [10, 50, 20] (confirmation)
//   'error'  → [50, 10, 50, 10, 50] (form error)

export function useHaptics() {
  const trigger = (pattern: HapticPattern) => {
    if ('vibrate' in navigator) navigator.vibrate(PATTERNS[pattern])
  }
  return { trigger }
}
```

Applied to: all buttons, form submissions, product card selections, filter toggles, accordion opens.

### 5.2 — Cursor System

**Custom cursor (desktop only):**
- Default: small circle (16px, ember color, 50% opacity)
- On interactive element: expands to 48px ring, inner dot shrinks
- On text: morphs to thin vertical line (like I-beam but thinner)
- On 3D canvas: crosshair with radial gradient
- On drag: grab icon morphs in
- Lag: 80ms magnetic follow (lerp) for premium feel
- Click: burst/ripple animation from cursor center

### 5.3 — Scroll Interactions

**Technologies:** GSAP ScrollTrigger + Intersection Observer

- **Parallax:** Hero elements at different scroll speeds (0.3x, 0.6x, 1x)
- **Horizontal scroll sections:** Case studies, certifications ticker
- **Pinned sections:** Manufacturing process (section stays, content animates)
- **Counter animations:** Numbers count up when entering viewport
- **Text reveals:** Masked clip-path reveals (left-to-right wipe, ember colored edge)
- **Image reveals:** Scale from 1.1→1.0 as they enter viewport
- **Stagger reveals:** Child elements cascade in with 80ms offset

### 5.4 — Hover Micro-interactions

| Element | Interaction |
|---|---|
| Nav links | Underline slides in from left, text shifts 2px up |
| Product cards | Lift 8px, border glow intensifies, 3D tilt (Tilt.js) |
| Buttons | Background slides in from left, icon shifts right 4px |
| Blog cards | Image scale 1.0→1.05, overlay darkens |
| Team cards | Flip to bio side (3D perspective flip) |
| Certification logos | Brief shine sweep animation |
| Social icons | Color fill sweeps up from bottom |
| CTA section | Background particle density increases on hover |

### 5.5 — Page-Level Transitions

```tsx
// Using Framer Motion's AnimatePresence + layoutId
// Shared element transitions between product list → detail
// Product card image flies to hero position on navigation
// Stagger out animation before leaving page
```

### 5.6 — Form Interactions

- **Focus states:** Input border animates from left, subtle glow
- **Validation:** Red shake + haptic 'error' on invalid submit
- **Success state:** Input fields crystallize → green → form slides out → success card slides in with metal-melt animation
- **Character counters:** Appear when focus, count down in mono font

### 5.7 — 3D Interaction Details

- **Product viewer:** Orbit controls enabled, inertia on release
- **Tilt on scroll:** Subtle 3D perspective tilt on cards based on scroll position
- **Magnetic buttons:** Near-hover magnetic pull (8px radius)

**→ Git commit:** `feat: haptics system, cursor, scroll interactions, micro-animations`
**→ Push to `feat/interactions-haptics`, open PR → merge to `main`**

---

## PHASE 6 — PERFORMANCE & SEO
### Branch: `perf/optimization`

### 6.1 — Core Web Vitals Targets

| Metric | Target |
|---|---|
| LCP | < 2.5s |
| FID / INP | < 100ms |
| CLS | < 0.1 |
| Lighthouse Performance | ≥ 90 |
| Lighthouse Accessibility | ≥ 95 |
| Lighthouse SEO | 100 |
| Lighthouse Best Practices | 100 |

### 6.2 — WebGL Performance

- **LOD (Level of Detail):** Reduce polygon count based on device capability
- **Adaptive quality:** Detect GPU tier via `detect-gpu`, set quality level
- **Mobile fallback:** Replace heavy simulations with CSS animations + video
- **Lazy load canvases:** Only initialize WebGL when section enters viewport
- **Web Workers:** Offload physics calculations from main thread
- **RequestAnimationFrame throttle:** Cap at 60fps, drop to 30fps on low battery

```tsx
// lib/hooks/useGPUTier.ts
import { getGPUTier } from 'detect-gpu'

// Tier 0: no WebGL (very old/low-end) → static images
// Tier 1: basic WebGL → simplified geometries, no post-processing
// Tier 2: moderate → standard quality
// Tier 3: high-end → full effects, max particles
```

### 6.3 — Asset Optimization

- **Images:** `next/image`, WebP/AVIF, responsive srcsets, blur placeholders
- **Fonts:** Self-hosted, `font-display: swap`, preload critical variants
- **3D Models:** Compress `.glb` with `gltf-pipeline` (Draco compression)
- **Videos:** H.264 + WebM, poster images, lazy autoplay
- **Icons:** SVG sprite sheet, no icon fonts

### 6.4 — Code Splitting

- Dynamic imports for all Three.js components
- Route-level code splitting (Next.js default)
- Separate chunk for Sanity client (server-only)
- GSAP plugins imported only where used

### 6.5 — Caching Strategy

```
Static assets:     Cache-Control: public, max-age=31536000, immutable
Pages (ISR):       revalidate: 3600 (1 hour)
Product pages:     revalidate: 86400 (24 hours)
Blog posts:        revalidate: 3600
API routes:        no-store (contact form, newsletter)
```

### 6.6 — Accessibility (a11y)

- Semantic HTML throughout
- ARIA labels on all interactive elements
- Focus visible styles (custom, matches design system)
- Skip navigation link
- Keyboard navigation for all interactive components
- Reduced motion: `prefers-reduced-motion` respected — all animations halved or disabled
- Color contrast: all text ≥ 4.5:1 ratio
- Screen reader testing: NVDA + VoiceOver
- Alt text on all images (from Sanity CMS field)
- Form error announcements via `aria-live`

### 6.7 — Internationalization (i18n) — Future-Ready

- Structure locale files: `locales/en.json`
- `next-intl` installed but only EN active at launch
- RTL-ready CSS (logical properties used throughout)

**→ Git commit:** `perf: adaptive WebGL quality, asset optimization, a11y, caching`
**→ Push to `perf/optimization`, open PR → merge to `main`**

---

## PHASE 7 — TESTING & QA
### Branch: `qa/testing`

### 7.1 — Unit Tests (Vitest)

```
lib/utils/*.test.ts          ← Pure utility functions
lib/hooks/*.test.tsx         ← Hook behavior tests
components/ui/*.test.tsx     ← Primitive component rendering
api/contact/route.test.ts    ← API route validation logic
```

### 7.2 — Integration Tests (Playwright)

```
tests/
├── navigation.spec.ts       ← Full nav traversal
├── contact-form.spec.ts     ← Form validation + submission
├── product-filter.spec.ts   ← Filter + routing
├── cms-content.spec.ts      ← Sanity data loading
└── a11y.spec.ts             ← Axe accessibility scan
```

### 7.3 — Visual Regression (Chromatic / Percy)

- Storybook stories for all UI components
- Chromatic on every PR — fails on visual diff > 0.1%

### 7.4 — Performance Testing

- Lighthouse CI in GitHub Actions — fails PR if score drops
- `@vercel/speed-insights` in production
- WebPageTest profiles on staging before every release

### 7.5 — Cross-Browser & Device QA Matrix

| Browser | Desktop | Mobile |
|---|---|---|
| Chrome | ✓ | ✓ (Android) |
| Safari | ✓ | ✓ (iOS) |
| Firefox | ✓ | ✓ |
| Edge | ✓ | — |
| Samsung Internet | — | ✓ |

Breakpoints tested: 375px, 390px, 768px, 1024px, 1280px, 1440px, 1920px

### 7.6 — Content QA

- All Sanity content fields validated
- No broken links (automated with `link-checker`)
- All images have alt text
- All downloads accessible
- Forms receive confirmation emails

**→ Git commit:** `qa: unit tests, e2e tests, a11y suite, visual regression`
**→ Push to `qa/testing`, open PR → merge to `main`**

---

## PHASE 8 — CI/CD & DEPLOYMENT
### Branch: `deploy/production`

### 8.1 — GitHub Actions Workflows

**`ci.yml` — runs on every PR:**
```yaml
jobs:
  lint:        ESLint + Prettier check
  typecheck:   tsc --noEmit
  test:        vitest run
  e2e:         playwright test (headless)
  lighthouse:  Lighthouse CI against preview URL
  chromatic:   Visual regression
```

**`deploy-preview.yml` — on push to any branch:**
```yaml
- Deploy to Vercel preview URL
- Comment preview URL on PR
- Run Lighthouse against preview
```

**`deploy-prod.yml` — on merge to main:**
```yaml
- Build + deploy to production
- Run smoke tests against production URL
- Notify team on Slack
- Create GitHub Release tag
```

### 8.2 — Vercel Configuration

```json
// vercel.json
{
  "headers": [
    { "source": "/(.*)", "headers": [
      { "key": "X-Frame-Options", "value": "DENY" },
      { "key": "X-Content-Type-Options", "value": "nosniff" },
      { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" },
      { "key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=()" }
    ]}
  ],
  "rewrites": [...],
  "redirects": [...]
}
```

### 8.3 — Domain & DNS

```
Production:    amorphis.com (or amorphis.in / .io)
Staging:       staging.amorphis.com (password protected)
Preview:       [branch].amorphis.vercel.app

DNS Provider:  Cloudflare (for proxy + DDoS protection)
SSL:           Auto-managed by Vercel + Cloudflare
CDN:           Vercel Edge Network + Cloudflare
```

### 8.4 — Monitoring & Alerts

- **Uptime:** Better Uptime — alert on Slack if site down
- **Error tracking:** Sentry — capture JS errors in production
- **Analytics:** Vercel Analytics (performance) + PostHog (behavior)
- **Real User Monitoring:** Vercel Speed Insights
- **Log drains:** Vercel → Datadog or Logtail

### 8.5 — Security

- Rate limiting on all API routes (Upstash Redis)
- reCAPTCHA v3 on contact form
- Content Security Policy headers
- Dependency audit in CI (`pnpm audit`)
- Dependabot for automated security PRs
- Secret scanning enabled on GitHub repo

**→ Git commit:** `deploy: CI/CD pipelines, Vercel config, monitoring, security`
**→ Push to `deploy/production`, open PR → merge to `main`**

---

## PHASE 9 — POST-LAUNCH
### Branch: merges to `main`

### 9.1 — Launch Checklist

```
□ All pages render without errors (production)
□ Contact form submits and sends email
□ All PDFs/downloads accessible
□ Analytics firing correctly
□ Sentry capturing errors
□ Lighthouse ≥ 90 across all pages
□ Meta tags correct on all pages (check via opengraph.xyz)
□ Sitemap submitted to Google Search Console
□ Bing Webmaster Tools submitted
□ Social preview images correct
□ 404 page styled and functional
□ Cookie consent banner active (if required)
□ Privacy policy and terms published
□ All external links open in new tab
□ No console errors in production
```

### 9.2 — SEO Launch Tasks

- Submit sitemap to Google Search Console
- Set up Google Analytics 4 goals/conversions
- Implement structured data for products (schema.org/Product)
- Set up Google Search Console alerts
- Ahrefs / Semrush baseline snapshot

### 9.3 — Future Feature Backlog (Ready to Implement on Request)

| Feature | Complexity | Branch Naming |
|---|---|---|
| Product configurator (custom alloy % mixer) | High | `feat/alloy-configurator` |
| Customer portal / dashboard | Very High | `feat/customer-portal` |
| Real-time quote calculator | Medium | `feat/quote-calculator` |
| Material comparison tool | Medium | `feat/material-compare` |
| AR material preview (WebXR) | Very High | `feat/webxr-preview` |
| Live chat (Intercom/Crisp) | Low | `feat/live-chat` |
| Multi-language support | Medium | `feat/i18n-[locale]` |
| E-commerce / sample ordering | High | `feat/ecommerce` |
| API / developer docs | Medium | `feat/developer-docs` |
| Video library / webinars | Medium | `feat/video-library` |

---

## 📋 QUICK REFERENCE: BRANCH MAP

```
main
├── init/foundation              Phase 0
├── design/system               Phase 1
├── feat/core-architecture      Phase 2
├── feat/hero-simulations       Phase 3
│   ├── feat/hero-webgl             3.1 Molten hero
│   ├── feat/material-simulator     3.2 Property explorer
│   ├── feat/process-scroll         3.3 Scroll storytelling
│   └── feat/particle-field         3.4 Background particles
├── feat/content-sections       Phase 4
│   ├── feat/homepage-sections      4.1
│   ├── feat/products-page          4.2
│   ├── feat/technology-page        4.3
│   ├── feat/about-page             4.4
│   ├── feat/sustainability-page    4.5
│   ├── feat/careers-page           4.6
│   ├── feat/contact-page           4.7
│   └── feat/blog                   4.8
├── feat/interactions-haptics   Phase 5
├── perf/optimization           Phase 6
├── qa/testing                  Phase 7
└── deploy/production           Phase 8
```

---

## 🗓️ SPRINT TIMELINE — 4 to 5 Hours Total

> **Mode:** Full-speed sprint. One phase at a time, no context switching. Claude generates all code, you run commands and confirm. Move immediately to the next phase on confirmation.

| Block | Phase | Duration | What Gets Done |
|---|---|---|---|
| Block 1 | Phase 0 — Foundation | ~30 min | Repo clone, Next.js scaffold, dependencies, env setup, folder structure |
| Block 2 | Phase 1 — Design System | ~30 min | Tokens, typography, all UI primitives, motion variants |
| Block 3 | Phase 2 — Core Architecture | ~30 min | Nav, footer, page transitions, SEO metadata, Sanity schemas |
| Block 4 | Phase 3 — Hero & Simulations | ~60 min | WebGL hero, molten shader, material simulator, scroll story, particle field |
| Block 5 | Phase 4 — Content Sections | ~60 min | All pages: home, products, about, technology, contact, blog, careers |
| Block 6 | Phase 5 — Interactions & Haptics | ~30 min | Haptics, custom cursor, scroll choreography, hover micro-interactions |
| Block 7 | Phase 6 — Performance & SEO | ~20 min | Adaptive GPU tiers, image opt, a11y, code splitting, caching headers |
| Block 8 | Phase 7 — Testing & QA | ~15 min | Smoke tests, Lighthouse check, broken link scan, console error sweep |
| Block 9 | Phase 8 — Deployment | ~20 min | Vercel connect, env vars, domain, CI/CD pipelines, live URL |
| **Total** | | **~4.5 hours** | **Deployed, live, production-ready** |

### Sprint Rules:
- No phase is skipped — but scope is tightened, not cut
- Static/mock data used first, CMS wired in Phase 4
- Mobile-first but desktop-polished
- Every block ends with a branch push + PR merge before the next block starts
- Mistakes logged in `MISTAKES.md` in real time — reviewed before each block

---

## 🤝 HOW WE WORK TOGETHER

1. **You say "begin Phase X"** — I generate all code, files, configs
2. **Each sub-phase = one PR** — code committed, branch named per this doc
3. **You review, request changes** — I patch with new commits on same branch
4. **You approve → merge → next phase begins**
5. **Feature requests any time** — I'll scope, add to backlog or current phase

---

*Document version: 1.0.0 | Created for Amorphis — Shape Metal Alloys*
*All implementation decisions here are starting points — subject to revision based on your feedback.*
