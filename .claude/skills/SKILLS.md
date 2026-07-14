# Project Skills & Standards — Unbreakable Fitness Gym (WordPress + Elementor)

This file defines the standards and workflow for building the **Unbreakable Fitness Gym**
website on the **live** WordPress host. It is the umbrella standards doc; the detailed,
tool-specific playbooks live in the sibling skill folders:

- [`unbreakable-build-spec.md`](unbreakable-build-spec.md) — **the 1:1 build spec for this
  project's Home page**, decoded from the Claude Design prototype (tokens, section map,
  copy, animations, build order). Start here.
- [`nextjs-to-elementor/SKILL.md`](nextjs-to-elementor/SKILL.md) — reusable `elementor-mcp`
  container/flex build patterns, image sideloading, chunked imports, gotchas. (Its
  Writing-Club content inventory is from a different site — ignore that part; the mechanics
  still apply.)
- [`elementor-global-templates/SKILL.md`](elementor-global-templates/SKILL.md) — site-wide
  Header/Footer as Theme Builder templates + the global color/typography kit.
- `wordpress-elementor` (user-level, `~/.claude/skills/`) — WP-CLI / browser-automation
  fallbacks for text/URL edits and template management when the MCP is unavailable.

> **Source of truth is the Claude Design prototype**, not a Next.js codebase. The prototype
> `Unbreakable Fitness Gym.html` is a self-unpacking React bundle; it was decoded to
> **`design_markup.html`** (full HTML/CSS) + **`design_component.js`** (interactivity) in the
> project root via `_decode_design.py`. **Read those decoded files for exact values**, and
> use [`unbreakable-build-spec.md`](unbreakable-build-spec.md) as the section-by-section map.
> Where `nextjs-to-elementor` says "read `app/<route>/page.tsx`", substitute these files.

---

## Live environment (verified 2026-07-14)

| Item | Value |
|------|-------|
| Site name | Unbreakable Fitness Gym |
| WP host (`WP_URL`) | `https://syn04ae.syd5.hostyourservices.net/~unbreaka/` |
| Public/brand domain | `https://unbreakable-strengthtraining.com.au` |
| Auth | Application Password (Basic auth) for `admin_6qxcmjpy` — **works** |
| TLS | Shared host uses a self-signed cert → `NODE_TLS_REJECT_UNAUTHORIZED=0` / `curl -k` |
| Elementor | **Elementor + Elementor Pro + PRO Elements active** (Theme Builder, Forms, dynamic content all available) |
| Other plugins | EMCP Tools (server-side MCP companion), Gravity Forms, WP File Manager |
| Pages | `Sample Page` (id 2, publish), `Privacy Policy` (id 3, draft) — clean slate |
| Media library | **Empty** (0 items) — all imagery must be sideloaded |
| Front page | `show_on_front=posts` — set a static front page once Home is built |

### REST API quirk — MUST use the query form, not pretty permalinks
The site runs under a `/~unbreaka/` userdir path, so **pretty REST permalinks 404**:

```
❌ https://.../~unbreaka/wp-json/wp/v2/pages        → 404
✅ https://.../~unbreaka/?rest_route=/wp/v2/pages   → 200
✅ https://.../~unbreaka/index.php?rest_route=/wp/v2/...  (for POST endpoints)
```

Always call REST as `?rest_route=/<namespace>/<route>` with `curl -k -u user:app_password`.

### MCP topology
- The Claude Code `elementor-mcp` server is a **stdio→HTTP bridge** (`emcp-proxy.mjs`) that
  talks to the server-side **EMCP Tools** plugin. Confirm `.mcp.json` `command`/`args`
  point at an existing `emcp-proxy.mjs` before relying on `elementor-mcp-*` tools.
- A generic WordPress MCP endpoint also exists at
  `?rest_route=/mcp/mcp-adapter-default-server` (WP Abilities: discover / get-info /
  execute). Useful as a low-level fallback, but it is **not** a substitute for the rich
  `elementor-mcp` toolset.

---

## Core principles

1. **Production-first, live host.** Every change lands on the live site. Treat it as a
   client production build: no throwaway experiments, no orphaned drafts, back up
   `_elementor_data` before any destructive edit, and publish only when asked.
2. **Elementor-first, native widgets over custom HTML.** Build with native Elementor
   widgets (Heading, Text Editor, Image, Button, Icon Box, Icon List, Star Rating, Form,
   etc.). **Avoid the HTML widget** — only reach for it when no native widget or container
   setting can achieve the result, and keep any such code minimal and scoped.
3. **Flexbox Containers, not the legacy Section/Column model.** Lay out every page with
   nested Flexbox containers. Row containers must set `flex_direction_mobile: "column"`
   and their children `width_mobile: 100`.
4. **Global Fonts, Global Colours, Theme Styles.** Register the prototype's palette as
   Global Colours and its type scale as Global Fonts / Theme Style typography, then
   reference those globals from widgets instead of hard-coding hex/px per widget. This is
   what makes the site editable and consistent for non-technical users later.
5. **Reusable Templates.** Header and Footer are Theme Builder templates (see the
   `elementor-global-templates` skill). Repeated section patterns (CTA band, testimonial
   card, pricing tier) should be saved as library templates and reused.
6. **1:1 fidelity — match every value exactly.** Copy layout, spacing, typography (family,
   size, weight, line-height, letter-spacing), colours, borders, radii, shadows, overlays,
   and image placement/sizing verbatim from the prototype. No eyeballing or "close enough".
   Copy mobile values into the `*_mobile` responsive controls.
7. **Responsive-first.** Verify desktop, tablet (1024px), and mobile (768px) breakpoints
   for every section. Elementor default breakpoints unless the prototype dictates otherwise.
8. **Editable imagery as widgets.** Sideload every image into the Media Library and place
   it as a native Image widget or a container `background_image: { url, id }` — **never** an
   `<img>` in an HTML widget, inline `background:url(...)`, or base64. The client must be
   able to swap any picture from the editor. Carry `alt` text from the prototype.
9. **Accessibility.** Correct heading hierarchy (one H1/page), meaningful `alt` text,
   sufficient colour contrast (WCAG AA), keyboard-navigable interactive elements, visible
   focus states, form labels, and `aria`/link text that makes sense out of context.
10. **SEO.** One H1 per page, logical H2/H3 outline, descriptive page titles + meta
    descriptions, clean slugs, descriptive image filenames/alt, and set the static front
    page once Home exists (`show_on_front=page`, `page_on_front=<id>`).
11. **Performance.** Right-size and compress images before sideloading, prefer native
    widgets (less CSS/JS than custom HTML), reuse global styles to reduce generated CSS,
    lazy-load below-the-fold imagery, and avoid unnecessary nesting/animation.
12. **Minimal custom CSS/JS.** Recreate motion with Elementor's native Motion Effects
    (entrance animations, scrolling/mouse effects, sticky) first. Only add scoped custom
    CSS/JS when a native capability genuinely cannot reproduce the effect.
13. **Maintainable, non-technical-editor-friendly structure.** Clear container nesting,
    named sections, global styles, reusable templates, and text/images living in native
    widgets so a non-developer can edit them in the Elementor UI without touching code.

---

## Standard build workflow

1. **Import & read the design.** Import `Unbreakable.dc.html` via the Claude Design MCP.
   Read it end-to-end and decompose the page into an ordered list of sections. Extract the
   exact design tokens (colours, fonts, sizes, spacing, radii, shadows) — record them in
   `nextjs-to-elementor/references/design-tokens.md`.
2. **Verify connections (once per session).** Confirm `elementor-mcp` responds
   (`elementor-mcp-list-pages`) and REST auth works (`?rest_route=/wp/v2/users/me`). If the
   MCP proxy is missing or the design import failed, **stop and report** — do not improvise.
3. **Set up globals first.** Register Global Colours + Global Fonts / Theme Style typography
   from the extracted tokens so every widget can reference them.
4. **Build Header & Footer** as Theme Builder templates (global) — see the
   `elementor-global-templates` skill.
5. **Sideload images** into the Media Library (`elementor-mcp-sideload-image` /
   `elementor-mcp-list-media` to dedupe); keep the returned `{ url, id }` for widgets.
6. **Build the page body** with Flexbox containers + native widgets, section by section.
   Chunk large imports (hero first, verify, then append with `position:-1`) — one giant
   container tree times out.
7. **Verify fidelity.** `elementor-mcp-get-page-structure` for section count/order;
   spot-check colours/fonts/spacing with `get-element-settings` against the tokens; check
   all three breakpoints.
8. **Publish only when asked.** Then set the static front page for Home via REST settings.

### Critical gotchas
- **A "Proxy error"/timeout can still mean the import SUCCEEDED.** Verify with
  `get-page-structure` before retrying, or you'll double the content.
- **Flush Elementor CSS** after any direct `_elementor_data` edit
  (`wp elementor flush-css`, or delete `_elementor_css` postmeta / `_elementor_global_css`).
- **Back up `_elementor_data`** before any destructive/search-replace edit.
- **Mobile:** always set `flex_direction_mobile` + `width_mobile` on row containers/children.
