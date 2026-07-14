# Design tokens → Elementor settings map

**Authoritative source:** `app/globals.css` — the `@theme inline` block, the `:root`
shadcn tokens, and the second `:root` "The Writing Club — design system" block. Re-read it
before a build — if it has changed, this snapshot is stale. Snapshot as of 2026-07-02:

## Colors

| Token | Hex | Used for |
|-------|-----|----------|
| `--twc-navy` / `--navy` | `#1D44B0` | brand primary; headings/link hover, hero band, mobile nav overlay |
| `--twc-navy-700` / `--navy-700` | `#16337F` | navy hovers / dark navy |
| `--navy-500` | `#3D5DCC` | navy accents |
| `--twc-red` / `--red` (`--primary`) | `#D70434` | **primary CTA buttons**, eyebrows, star/rating accents |
| `--twc-red-700` / `--red-700` | `#AB0329` | primary button hover |
| `--twc-cream` / `--cream` | `#FAF7F2` | soft section backgrounds |
| `--twc-cream-2` / `--cream-2` | `#F4EFE6` | alt cream background |
| `--twc-ink` / `--ink` | `#15202B` | headings / dark body text |
| `--twc-slate` / `--slate` | `#475569` | secondary text |
| `--slate-soft` | `#64748B` | muted secondary text |
| `--twc-rule` / `--rule` | `#E5DFD3` | borders / rules |
| `--rule-light` | `#EFEAE0` | light borders |
| hero overlay | `#102C7A` | hero gradient scrims (`.hero-gradient-r/-b`, at various opacities) |
| UI grays | Tailwind `gray-200/500/600/900`, `white #ffffff` | header/footer chrome, nav text, card borders |

shadcn mapping: `--primary` = `#D70434` (red), `--secondary` = `#1D44B0` (navy).

## Typography

| Role | Family | Notes |
|------|--------|-------|
| Headings h1–h6 **and** reading body | `Inter` (`--font-sans`, via `next/font`) | applied globally on `html` |
| Serif display accent (italic flourishes) | `Fraunces` (`--font-serif`, axes SOFT/WONK/opsz) | used italic |

Base `html` font-size `16px`. Page-body container max width **1400px** (`.site-container`,
padding `24px`/`32px@md`); header mega-menu + footer inner use **1320px** (`--twc-max`).
Header height `96px` (`h-24`). Section rhythm `.site-section` = `48px`/`64px@md`.

Heading scale (from `@layer base`):

| Tag | Mobile | ≥`md` (768px) | Weight / tracking |
|-----|--------|---------------|-------------------|
| h1 | `text-3xl` 30px | `text-5xl` 48px | bold 700, `leading-[1.05]`, tracking-tight |
| h2 | `text-2xl` 24px | `text-4xl` 36px | extrabold 800, `leading-[1.1]`, tracking-tight |
| h3 | `text-xl` 20px | `text-2xl` 24px | bold 700, `leading-[1.1]` |
| body | `16.5px` | up to `19px` in heroes | `leading-relaxed` |
| eyebrow | `13px` | — | semibold 600, uppercase, `tracking-[0.2em]` |

(Home hero h1 is custom: `clamp(32px,4.5vw,60px)`, extrabold 800, `leading-[1.04]`,
`tracking-[-0.025em]`, white.)

Apply to heading widgets:
```
title_color: <hex>
typography_typography: "yes"
typography_font_family: "Inter"
typography_font_size: { unit:"px", size:<n> }
typography_font_size_mobile: { unit:"px", size:<n> }
typography_font_weight: "700"        // 800 for h2 / hero
typography_letter_spacing: { unit:"px", size:-0.4 }   // tracking-tight ≈ -0.025em
```

## Buttons (rounded 6px — NOT pill)

The `Button` component (`components/ui/button.tsx`) is `rounded-md` (radius `6px`),
`font-semibold` (600). Primary variant = red CTA:
```
button_text_color: "#ffffff"
background_color: "#D70434"            // --twc-red / variant="primary"
button_background_hover_color: "#AB0329"   // --twc-red-700
hover_color: "#ffffff"
border_radius: { unit:"px", top:6, right:6, bottom:6, left:6 }
typography_typography:"yes"; typography_font_family:"Inter"; typography_font_weight:"600"
```
Sizes: `default` = height 48px, padding `0 24px`, 16px text; `lg` = height 56px,
padding `0 28px`, 15px text; `sm` = height 40px, padding `0 20px`.
Other variants: `navy` (`bg #1D44B0`, hover opacity 90%), `ghost-white`
(border `rgba(255,255,255,.3)`, text white, hover `bg white/10`), `outline-navy`
(border/text `#1D44B0`, hover fill navy + white text).

## Global kit (do once)

Set these on the Elementor global kit so widgets inherit them, reducing per-widget
overrides:
- `elementor-mcp-update-global-colors`: map primary→red `#D70434`, secondary→navy `#1D44B0`,
  accent→navy-700 `#16337F`, text→ink `#15202B`.
- `elementor-mcp-update-global-typography`: primary font Inter, text font Inter, and add
  Fraunces for serif display accents.
