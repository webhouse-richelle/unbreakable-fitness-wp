---
name: nextjs-to-elementor
description: "Build a WordPress/Elementor page as a 1:1 replica of a Next.js source route (app/**/page.tsx) using the elementor-mcp tools over the WP REST API. Use whenever the user wants to recreate, port, rebuild, or sync a page from this Next.js codebase onto the live Elementor site, or asks to build the home/about/courses/our-method/resources/careers/franchise/contact page in Elementor to match the code."
compatibility: claude-code-only
---

# Next.js → Elementor (1:1 page builds via elementor-mcp)

Recreate a page from The Writing Club Next.js codebase onto the live WordPress/Elementor
site so it matches the source **section-for-section, token-for-token**. Uses the
**elementor-mcp** MCP tools (REST-based), NOT WP-CLI or browser automation.

This project's live target, credentials, and TLS quirk are configured in `.mcp.json`:
the proxy runs via `node ./emcp-proxy.mjs` (copied into this repo root) against
`WP_URL=https://syn06be.syd6.hostyourservices.net/~writingc/`. The shared host's
self-signed cert is handled by `NODE_TLS_REJECT_UNAUTHORIZED=0` in that env. **Ignore the
`wordpress/` folder in this repo — it is the deprecated local pipeline; we build directly
on the live host.**

## Golden rule of 1:1 fidelity

**The Next.js source is the single source of truth. Never invent content.** For each page:

| Content | Source file |
|---------|-------------|
| Page body sections & copy | `app/<route>/page.tsx` (+ its section components in `components/`) |
| Course data (per year / level) | `lib/course-details.ts` (rendered via `components/course-detail-page.tsx`, `components/year-course-page.tsx`) |
| Centres / locations / contact / business info | `lib/centres.ts` (single Thornleigh centre) |
| Resources & downloads | `lib/resources.ts` |
| Blog posts | `content/blog-posts/*.mdx` (+ `content/blog.tsx`) |
| Blog authors | `lib/blog-authors.ts` |
| Home FAQ | `lib/home-faq.ts` |
| Header nav / mega menu | inline `programsMega` in `components/site-header.tsx` |
| Footer nav / columns | inline link arrays in `components/site-footer.tsx` |
| Colors, fonts, spacing, breakpoints | `app/globals.css` (`@theme inline` + the `:root` design-system block) |
| Header / Footer (global templates) | `components/site-header.tsx` / `components/site-footer.tsx` — see `elementor-global-templates` skill |
| SEO / metadata | per-page `export const metadata` + `lib/seo.ts` |
| Images | referenced as `/twc/...` → files in `public/twc/...` |

Read the actual `page.tsx` (and any section component it imports) every time — do not rely
on memory of it. Decompose the page into ordered sections, then map each section to an
Elementor container.

## Match every value EXACTLY — no eyeballing, no "close enough"

Fidelity is not just content and section order. Every **numeric and stylistic value**
must be copied verbatim from the source (Tailwind classes + `globals.css`) into the
Elementor setting — never approximated, rounded, or invented:

- **Font family** per role: headings/titles and body both use **Inter** (`--font-sans`,
  applied on `html`); **Fraunces** (`--font-serif`) is the italic serif display accent.
  Set `typography_font_family` explicitly on every text widget; do not rely on inherited
  defaults.
- **Font size** — read the exact size from the Tailwind class and set
  `typography_font_size` to that px (e.g. hero h1 `clamp(32px,4.5vw,60px)`, section h2
  `text-2xl`=24px → `md:text-4xl`=36px, h3 20→24px, body `16.5–19px`, eyebrow `13px`).
  Copy the mobile size (the non-`md:` value) into `typography_font_size_mobile`.
- **Font weight, line-height, letter-spacing** — match the classes (h1 `font-extrabold`
  800 `leading-[1.04]` `tracking-[-0.025em]`; h2 `font-extrabold` 800 `tracking-tight`;
  h3 `font-bold` 700; eyebrow `font-semibold` 600 `uppercase` `tracking-[0.2em]`; body
  `leading-relaxed`). Don't leave them at Elementor defaults.
- **Padding / margin** — transcribe each section's exact spacing. Section rhythm is
  `.site-section` = `py-12` (48px) / `md:py-16` (64px); container gutters are `px-6`
  (24px) / `md:px-8` (32px). Put the mobile-reduced values into `padding_mobile`.
- **Container / column sizing** — reproduce the grid ratios as widths: the home hero
  `lg:grid-cols-[minmax(0,1fr)_minmax(0,1.05fr)]` → ~49% / 51%; footer
  `lg:grid-cols-[320px_1fr]`. Respect the container max: page bodies use `.site-container`
  = **1400px**; the header mega-menu and footer inner use **1320px** (`--twc-max`). Match
  `gap`, `min-height`, and flex gaps from the source.
- **Colors** — use the exact hex from `globals.css` (navy `#1D44B0`, navy-700 `#16337F`,
  red `#D70434`, red-700 `#AB0329`, cream `#FAF7F2`, cream-2 `#F4EFE6`, ink `#15202B`,
  slate `#475569`, rule `#E5DFD3`; UI grays via Tailwind), not a global-kit slot that
  might differ by a shade.

After building, spot-check with `get-element-settings` and diff the value against the
source. If the source changes a value, the build must change too.

## Effects, links & interactions must match too (body AND header/footer)

Carry over every interactive/visual detail, not just the static layout:

- **Button/link targets** — every `href` (including `tel:`/`mailto:` and hash anchors),
  `target`/`rel`, and which element is the click target (e.g. whole-card links via the
  container `link` setting) must match the source markup exactly. Primary CTA is
  **Book Free Assessment** → `/book-free-assessment`; phone `tel:0294843350` shows
  `(02) 9484 3350`.
- **Hover states** — button hover bg/text colors (`button_background_hover_color`,
  `hover_color`), nav link hover color (`text-twc-navy` `#1D44B0`), footer link hover
  (`text-gray-900`), card hover, etc. Reproduce them, using scoped `<style>` in an HTML
  widget where a native control doesn't exist.
- **Header/Footer effects** — replicate the source behaviours from `site-header.tsx` /
  `site-footer.tsx`: the Courses mega-menu, nav hover/active colors, the mobile navy
  (`#1D44B0`) overlay + burger, the fixed header, social-icon hover, and radii. Match
  these token-for-token just like the body.
- **Carousels/JS sections** (photo scroller, testimonials, clients marquee) — preserve the
  exact copy and, where a native widget can't reproduce the interaction, embed a scoped
  HTML/CSS/JS carousel that mirrors the source styling and controls.

## Editable images — collect and place as widgets (never HTML)

The client must be able to swap images themselves in the Elementor/WordPress editor.
So images are handled two ways, together, on every page build:

1. **Identify every image the page actually uses.**
   - As you decompose the source page, note each real image reference (hero, logos,
     partner/badge strips, section art, background images, OG image). Resolve each to its
     file under `public/twc/...` (e.g. `/twc/classroom.jpg` → `public/twc/classroom.jpg`,
     `/twc/heros/...`, `/twc/covers/...`). Only handle images genuinely used on the site —
     do not dump the whole `public/twc/` tree.

2. **Place every image as a native, editable Elementor image widget — never as raw HTML.**
   - Sideload with `elementor-mcp-sideload-image` from the deployed Next.js site URL
     (confirm the current deploy origin serving `/twc/...`), then use
     `elementor-mcp-add-image` (or an `{ "elType":"widget", "widgetType":"image" }` object)
     with the returned `{ url, id }`. This gives the client a real image control they can
     click and replace in the editor. Check `elementor-mcp-list-media` first to avoid dupes.
   - The same applies to **background images**: prefer a container background set via
     `background_image: { url, id }` (an editable control) over an `<img>` baked into an
     HTML widget.
   - **Do NOT** embed images as `<img src>` inside an `add-html` / HTML widget, as inline
     CSS `background:url(...)`, or as base64. Those are not editable from the WordPress UI
     and defeat the purpose. The only images allowed inside an HTML widget are ones that
     literally cannot be a widget (e.g. an image baked into a scoped-CSS carousel) — and
     even then, prefer refactoring so the client can still swap it.
   - Every image widget keeps its `alt` text from the source `alt` attribute.

Net effect: the client edits or replaces any picture directly through the Elementor image
widgets.

## Prerequisites (verify once per session)

1. elementor-mcp connected: call `elementor-mcp-list-pages`. If it errors, the MCP
   didn't load — check `.mcp.json` points at the `emcp-proxy.mjs` in `command`/`args` and
   restart, and that `WP_URL`/creds are the live host.
2. Confirm Elementor version: `elementor-mcp-detect-elementor-version`.

## First: present the site page list so the user picks what to build next

Before building, **enumerate every page on the site and show it to the user so they can
choose which one to build next.** Build the list fresh from `app/` each time (it changes) —
read the folder, expand dynamic routes, and present it as a checklist noting what's already
built vs. pending. Current inventory:

**Core pages**
- Home — `app/page.tsx` (`/`)
- About — `app/about/page.tsx` (`/about`)
- Our Method — `app/our-method/page.tsx` (`/our-method`)
- Contact — `app/contact/page.tsx` (`/contact`)
- Careers — `app/careers/page.tsx` (`/careers`)
- Franchise — `app/franchise/page.tsx` (`/franchise`)

**Courses** (`app/courses/...`)
- Courses hub — `courses/page.tsx` (`/courses`)
- High School Writing — `courses/high-school-writing/page.tsx`
- High School years — `courses/high-school/year-7|8|9|10/page.tsx`
- Primary School years — `courses/primary-school/year-1…6/page.tsx`
- Selective School — `courses/selective-school/page.tsx`
- NAPLAN & Scholarship — `courses/naplan-scholarship/page.tsx`
- Advanced Writing — `courses/advanced-writing/page.tsx`
- Year 9 Writing — `courses/year-9-writing/page.tsx`
- School Holiday Programs — `courses/school-holiday-programs/page.tsx`
- Online Learning Hub — `courses/online-writing-workshops/page.tsx`
- Free Live Webinar — `courses/free-live-webinar/page.tsx`

**Resources / Blog / Locations**
- Resource Centre — `app/resources/page.tsx` (`/resources`)
- Downloads — `app/resources/downloads/page.tsx` (`/resources/downloads`)
- Blog index — `app/blog/page.tsx` (`/blog`)
- Blog post — `app/blog/[slug]/page.tsx` (dynamic, one per `content/blog-posts/*.mdx`)
- Blog author — `app/blog/author/[slug]/page.tsx` (dynamic, per `lib/blog-authors.ts`)
- Locations — `app/locations/page.tsx` (`/locations`)
- Location detail — `app/locations/[slug]/page.tsx` (dynamic, per `lib/centres.ts` — Thornleigh)

**Booking** (route group `(booking)` — uses its own minimal layout)
- Book Free Assessment — `app/(booking)/book-free-assessment/page.tsx` (`/book-free-assessment`)
- Booking Thank You — `app/(booking)/book-free-assessment/thank-you/page.tsx`

**Utility / legal**
- Privacy Policy — `app/privacy-policy/page.tsx` (`/privacy-policy`)
- Thank You — `app/thank-you/page.tsx` (`/thank-you`)
- 404 — `app/not-found.tsx`

Ask the user which page to build, then proceed with the workflow below for that page.

## Workflow

1. **Read the source page** `app/<route>/page.tsx` end to end (plus any section components
   it imports from `components/`). List its sections in order (hero, programs, method,
   testimonials, FAQ, CTA, etc.).
2. **Identify or create the WP page**: `elementor-mcp-list-pages`. If it doesn't exist,
   `elementor-mcp-create-page`. Record the post ID.
3. **Sideload images.** For each image the page uses (`/twc/...` → `public/twc/...`):
   `elementor-mcp-sideload-image` from the deployed Next.js site, then reuse the returned
   `{ url, id }` in **editable image widgets / container backgrounds — never HTML `<img>`**.
   Check `elementor-mcp-list-media` first to avoid duplicates.
4. **Build the body**: `elementor-mcp-delete-page-content(post_id)` then
   `elementor-mcp-import-template(post_id, [containers], position:-1)`. Use the
   container/flex model and design tokens — see `references/build-recipe.md` and
   `references/design-tokens.md`. Chunk large pages into multiple imports.
5. **Verify**: `elementor-mcp-get-page-structure(post_id)`. Compare section count and
   order against the source. Spot-check colors/fonts via `elementor-mcp-get-element-settings`.
6. **Publish** only when asked (`elementor-mcp-update-page-settings` status=publish).
   For the home page also set it as the static front page via WP REST settings
   (`show_on_front=page`, `page_on_front=<id>`).

## Critical gotchas

- **A "Proxy error" / timeout response can still mean the import SUCCEEDED.** Always
  verify with `get-page-structure` before retrying. Do NOT blind-retry — you'll double
  the content.
- **Chunk big imports.** One giant container tree times out the HTTP response. Import
  the hero first, verify, then append remaining sections with `position:-1`.
- **Mobile matters.** Every row container needs `flex_direction_mobile:"column"` and
  children need `width_mobile:100`. Source breakpoints (Tailwind): `lg` 1024px (nav/layout
  collapse) and `md` 768px (typography/hero), plus a `max-width:767px` hero crop rule.
- **Fonts:** headings + body = **Inter** (`--font-sans`); serif italic accents = **Fraunces**
  (`--font-serif`). Both load via `next/font/google` on the Next.js side — on WordPress
  enqueue the matching Google Fonts (Inter, Fraunces) so text doesn't fall back.

See `references/design-tokens.md` for the exact color/font/spacing → Elementor settings
map, and `references/build-recipe.md` for the container JSON recipe and widget patterns.
