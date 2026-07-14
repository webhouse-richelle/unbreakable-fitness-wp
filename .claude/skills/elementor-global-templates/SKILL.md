---
name: elementor-global-templates
description: "Build site-wide global Header and Footer as Elementor Pro Theme Builder templates (and set the global color/typography kit) so every page inherits them, replicating components/site-header.tsx and site-footer.tsx. Use when the user wants a global/site-wide header or footer, a Theme Builder template, or asks to make the nav/footer apply across all pages instead of per-page."
compatibility: claude-code-only
---

# Elementor global templates (Header / Footer / Kit)

Recreate the Next.js `site-header.tsx` and `site-footer.tsx` as **Elementor Pro Theme
Builder** documents displayed site-wide, so page bodies contain only their own content
(matching the Next.js layout where Header/Footer live in `SiteShell` / `app/layout.tsx`,
not each page).

Pairs with the `nextjs-to-elementor` skill (page bodies). Live target, credentials, and the
`emcp-proxy.mjs` path are configured in `.mcp.json` (`WP_URL=https://syn06be.syd6.hostyourservices.net/~writingc/`).

## Sources of truth

| Template | Source | Data |
|----------|--------|------|
| Header | `components/site-header.tsx` | inline `programsMega`, `TwcLogo` (`public/twc/*` logos), phone `(02) 9484 3350` |
| Footer | `components/site-footer.tsx` | inline `programLinksCol1/2`, `locationLinks`, `companyLinks`; `lib/centres.ts` |

Header nav (lean): **Courses** (mega menu), **Our Method**, **Resource Centre**,
**Careers**, **Franchise**; right side: **Login**, **Book Free Assessment** (red CTA),
phone. Footer groups: **Programs** (two sub-columns), **Locations** (Thornleigh),
**Company**. Read the actual files — do not rely on memory.

## Header spec (from site-header.tsx)

- Fixed full-width bar, **white** background, `border-b` `gray-200`, height `96px`
  (`h-24`). Logo left (`TwcLogo`, `h-16`/`md:h-20`, link to `/`).
- Desktop (`lg` ≥1024px): horizontal nav, `text-gray-600`, `Inter`, hover →
  `bg-gray-100` + `text-twc-navy` (`#1D44B0`).
- **Courses** opens a 3-column mega menu (tagline / category list / year-links panel)
  driven by `programsMega` — build as a nav submenu / mega (or an Elementor Pro Nav Menu
  widget pointed at a WP menu; see below).
- Right cluster: `Login` text link, `Book Free Assessment` red button
  (`bg-twc-red` → `/book-free-assessment`), phone `(02) 9484 3350` (`tel:0294843350`).
- Mobile (<`lg` 1024px): collapse to a burger toggle opening a full **navy** (`#1D44B0`)
  overlay with accordion (Courses expands to year links).

## Footer spec (from site-footer.tsx)

- **White** background, `border-t`. Grid `lg:grid-cols-[320px_1fr]`: brand column
  (footer logo `public/twc/twc-logo-footer.png` + blurb "Sydney's writing specialists…
  Thornleigh centre and live online.") + link groups.
- Link groups: **Programs** (`programLinksCol1` + `programLinksCol2`), **Locations**
  (`/locations#thornleigh`), **Company** (`Our Method`, `Resource Centre`, `Contact Us`,
  `Privacy Policy`, phone). Link text `14px` `text-gray-500` hover `text-gray-900`.
- Bottom bar: `© {year} The Writing Club. All Rights Reserved.` + `Privacy Policy` +
  `Website by Webhouse` (→ webhouse.com.au) + Facebook + Instagram icon links.
- Note the `minimal` variant (used by the `(booking)` route group) = single copyright +
  Privacy Policy line only.

## Match every value EXACTLY — fonts, spacing, effects, links

The Header/Footer must be a token-for-token replica of `site-header.tsx` / `site-footer.tsx`
+ their `globals.css` rules, not an approximation. Copy each value verbatim:

- **Fonts** — nav/buttons/headings/body all `Inter`; set `font_family` explicitly on every
  text element (don't rely on inheritance).
- **Sizes / weights / spacing** — exact px and weights: nav link `16px`/`font-medium` 500,
  mega tagline `22px` bold `leading-[1.28]`, mega eyebrow `11px` bold uppercase
  `tracking-[0.18em]`, footer links `14px`, footer heading `13px` bold, brand blurb `14px`
  `leading-[1.7]`, social svg `20px`. Match line-heights and `letter-spacing` too.
- **Padding / container sizing** — header bar height `96px`, `.site-container` gutters
  `24px`/`32px@md`; mega-menu + footer inner max width `1320px`. Footer main pad `24px`/
  `32px@md`, bottom bar `20px`. Transcribe exactly, with mobile-reduced values.
- **Colors** — exact hex: white `#ffffff` bar, `border-gray-200`, nav text `gray-600`
  hover `twc-navy #1D44B0`, mega active `twc-red #D70434` + `bg-red-50`, mobile overlay
  `#1D44B0`, footer text `gray-500` hover `gray-900`, red CTA `#D70434`/hover `#AB0329`.
- **Effects & links** — reproduce every hover (nav bg/text, mega category highlight, footer
  links, social hover), the **fixed** header behaviour, the Courses mega + mobile burger
  overlay, `tel:0294843350` on the phone, `Book Free Assessment` → `/book-free-assessment`,
  and radii (`6px`). Use scoped `<style>` in an HTML widget for hovers/interactions a native
  control can't express.

After building, `get-element-settings` on each element and diff against the source; also
`get-page-structure` and re-fetch the live page to confirm the templates still render.

## How to build (REST + elementor-mcp)

Theme Builder header/footer are Elementor Pro **library documents** with
`_elementor_template_type` = `header` / `footer` and a display condition of
`include/general` (entire site).

1. **Best path — Elementor Pro Nav Menu:** create a WP menu (Appearance → Menus, or via
   REST `wp/v2/menus` + `menu-items`) mirroring the header nav / footer groups, then
   reference it from a Nav Menu widget. This keeps nav data-driven.
2. **Create the template document.** If an `elementor-mcp` tool exposes template-type /
   theme-builder creation (`elementor-mcp-list-templates`, `save-as-template`,
   `apply-template`), use it. Otherwise create the library post via WP REST:
   - POST a post of type `elementor_library` with meta `_elementor_template_type: header`
     (or `footer`) and `_elementor_edit_mode: builder`.
   - Set the display condition meta (`_elementor_conditions`: `["include/general"]`).
3. **Build the content** with the container model + tokens (see the
   `nextjs-to-elementor` build-recipe and design-tokens references).
4. **Verify** the condition is site-wide and the template renders on the home page and
   one interior page. Confirm the active theme is `hello-elementor` so the theme's own
   header/footer don't double up.

If a step genuinely cannot be done via REST/MCP (e.g. assigning display conditions in
some Elementor versions), say so and hand off the exact wp-admin click-path:
Templates → Theme Builder → Header/Footer → Add New → Display Conditions → Entire Site.

## Global kit (do first)

Set brand colors + fonts on the active Elementor kit so header/footer and all pages
inherit them: `elementor-mcp-update-global-colors`, `elementor-mcp-update-global-typography`
(map: primary=red `#D70434`, secondary=navy `#1D44B0`, accent=navy-700 `#16337F`,
text=ink `#15202B`; primary + text font `Inter`, serif display accent `Fraunces`).
