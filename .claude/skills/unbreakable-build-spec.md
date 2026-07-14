# Unbreakable Strength Training — Home Page Build Spec (1:1)

Decoded from the Claude Design bundle `Unbreakable Fitness Gym.html`. The bundle is a
self-unpacking React prototype; the real markup was recovered to **`design_markup.html`**
(full HTML/CSS) and **`design_component.js`** (interactivity) in the project root via
`_decode_design.py`. **Those two files are the source of truth — read them for exact values;
this doc is the map.** Single-page site; nav links are in-page anchors.

## Global tokens

### Fonts (register as Global Fonts / Theme Style)
| Role | Family | Weight | Notes |
|------|--------|--------|-------|
| Display / all headings | **Anton** | 400 | `text-transform:uppercase`, tight line-height (.8–.92) |
| Body / UI | **Inter** | 400–900 | site default; `body` uses Inter |
| Placeholder captions | ui-monospace/Menlo | — | only inside dashed image-placeholder boxes |

Enqueue Google Fonts **Anton** and **Inter** (Inter needs 400/500/600/700/800/900).

### Colours (register as Global Colours)
| Token | Hex | Use |
|-------|-----|-----|
| Accent (Primary) | `#FFC107` | brand gold — CTAs, eyebrows, accents, links |
| Accent hover | `#ffce3a` | link/gold hover |
| Black | `#000000` | page bg, hero, about, programs, CTA |
| Footer black | `#050505` | footer bg |
| Panel black | `#0a0a0a` | trust strip, why, memberships bg |
| Card black | `#0d0d0d` | program/pricing cards, form field |
| Texture black | `#0e0e0e` | hero/CTA diagonal-texture layer |
| Surface | `#141414` | image placeholders |
| Popular card | `#141005` | highlighted pricing card bg (gold border) |
| Hairline | `#161616` | section top/bottom borders |
| Border | `#1c1c1c` | card borders |
| Border 2 | `#1a1a1a` | why-grid gap/border |
| Border 3 | `#262626` | social icons, form border |
| Text primary | `#ffffff` | headings/body |
| Text 72 | `rgba(255,255,255,.72)` | lead paragraphs |
| Text 60/55 | `rgba(255,255,255,.6/.55)` | body copy |
| Text 50/45/40 | `rgba(255,255,255,.5/.45/.4)` | muted/legal/footer |
| Line 30/25 | `rgba(255,255,255,.3/.25)` | dividers, disabled ✕ |

### Layout
- Content container **max-width 1360px**, padding `0 40px` desktop → **`0 24px` ≤900px**.
- Section vertical padding: `clamp(80px,10vw,140–150px)`; hero `min-height:100vh`; CTA `clamp(90px,12vw,170px)`.
- Breakpoints: **≤900px** nav→burger + all 2-col splits→1col + hero pad 24px; **≤600px** pricing 4-col→1col.
- Buttons: `border-radius:2px`, uppercase, `font-weight:700–800`, letter-spacing ~.04em, padding ~`19px 30px`.

## Section order & key values (map each to one Elementor container)

1. **Fixed Nav** (`data-nav`, z100) — logo (barbell SVG + "unbreakable" 19px/800 + "STRENGTH TRAINING" 8.5px/.42em gold); desktop links About/Why Us/Programs/Memberships (13.5px/600); gold "Free Trial" button; burger ≤900px. **Behaviour:** transparent → bg `#000` + bottom border `#1a1a1a` + shadow after 40px scroll. Top **scroll-progress bar** 3px gold (`data-progress`).
2. **Hero** (`#home`, min-h 100vh, bottom-aligned) — eyebrow "Australia's Strength Training Gym"; H1 Anton `clamp(62px,12.5vw,182px)` line-height .86 "Become / **Unbreakable.**" (gold 2nd line); lead 520px; two CTAs (gold "Start Your Free Trial →", outline "View Memberships"); right **floating stats** column (500+ Members / 15+ Years / 24/7 Access, Anton 52px, gold left border on first); scroll cue. Decorative: rotating dashed plate, drifting outline text, diagonal texture, gold radial glow, **image placeholder** "Full-bleed hero — athlete mid-lift, low light".
3. **Trust strip** (`#0a0a0a`, hairline top/bottom) — 4 stat blocks (4.9 ★★★★★ Google 300+ / 15+ Years / 500+ Members / 12k+ Coached sessions); **marquee** of partner names (Powerlifting Australia · Eleiko · Best Gym Awards '25 · Rogue · Strength & Conditioning Assoc.), Anton 26px, opacity .16, masked edges.
4. **About** (`#about`, 2-col 1.05/.95) — left image placeholder "Coach spotting a barbell squat" (aspect 4/5) + gold badge "93% of members still training after 12 months"; right eyebrow "Who we are", H2 "Strength that outlasts the **hype.**" (last word gold outline text), lead, 2×2 feature list (Strength & longevity / Real coaching / Accountability / Community) with gold "/" markers.
5. **Why choose us** (`#why`, `#0a0a0a`) — eyebrow + H2 "Built different. On purpose." + intro; **6-cell grid** (1px gaps on `#1a1a1a`): 01 24/7 Access, 02 Elite Equipment, 03 Strength Coaching, 04 Small Group Training, 05 Recovery Zone, 06 Supportive Community. Numbers Anton 20px gold; titles Anton 27px; hover bg `#111`.
6. **Programs** (`#programs`) — eyebrow + H2 "Find the way you'll train."; **6 cards** (auto-fit minmax 320px), each = image placeholder (4/3) + Anton 28px title + copy + gold "Learn More →": Strength Training, Personal Training, Athlete Performance, Small Group Coaching, Weight Loss, Senior Strength. Card hover: translateY(-6px), border `#333`.
7. **Memberships** (`#memberships`, `#0a0a0a`, centered head) — eyebrow (flanked by rules) + H2 "No lock-in. No excuses."; **4 pricing cards** (grid 4→1col ≤600px): Casual Visit $20/visit, Standard $34/week, **Unlimited $44/week (Most Popular — gold border, `#141005`, badge, gold CTA)**, Personal Training from $80/session. Each has 3 feature lines (gold ✓ / muted ✕) + button. Footnote: week-to-week, no lock-in, AUD.
8. **Final CTA** (`#cta`) — eyebrow "Your first week is on us"; huge H2 Anton `clamp(52px,10vw,150px)` "Ready to become **unbreakable?**" (last word gold outline); two CTAs (gold "Book Your Free Trial →", outline "See Memberships"). Decorative texture + image placeholder "Wide gym-floor photo, dark overlay" + rotating dashed ring.
9. **Footer** (`#050505`) — giant outline wordmark "Unbreakable"; 4 columns: brand (logo + blurb + IG/FB/YT square icons), Explore links, Opening Hours (Mon–Fri 6a–8p / Sat–Sun 7a–2p / Members 24/7), newsletter form + `hello@unbreakable-strengthtraining.com.au` / `(02) 5550 0184`; bottom bar © 2026 Unbreakable Fitness Gym | Privacy Policy | Website by Webhouse (link `https://www.webhouse.com.au/`) + "Train hard. Live strong."

## Imagery — IMPORTANT
The prototype ships **no real photos** — every image is an intentional **dashed placeholder box** with a monospace caption describing the shot (hero, About coach, 6 program cards, CTA). Recreate each as a **native Elementor Image widget / container background** styled as a placeholder (dark `#141414` + diagonal texture + dashed border + caption), so the client can swap in real photography later. Never bake these as HTML `<img>`.

## Animations (Elementor Motion Effects first; minimal custom JS only where needed)
- **Scroll reveal** (`data-rv`, staggered `data-d` ms): opacity 0→1 + translateY 32px→0, .85s `cubic-bezier(.16,1,.3,1)`. → Elementor **Entrance Animation** (fadeInUp) + per-widget animation delay.
- **Count-up** (`data-count`, 1.5s ease-out cubic) on stats (500+, 15+, 4.9, 12k+, 93%). → Elementor **Counter** widget (Anton, gold/white) or small scoped JS if exact styling needs it.
- **Nav scroll state** + **progress bar** → sticky Elementor header effect + minimal custom JS/CSS.
- **Marquee** (partner logos), **rotating dashed plates/rings** (`ub-spin`), **floating stats** (`ub-float2`), **drifting outline word** (`ub-drift`), **hero mouse parallax** (`data-px`) → CSS keyframes / Elementor mouse-track effects; keep custom CSS scoped and minimal.
- Mobile menu overlay (full-screen `#000`, Anton 46px links) → Elementor mobile menu / nav widget.

## Build order (post-restart, with elementor-mcp tools)
1. `elementor-mcp-detect-elementor-version` + `list-pages`.
2. Set Global Colours + Global Fonts from the tables above (`update-global-colors`, `update-global-typography`); enqueue Anton + Inter.
3. Build **Header** + **Footer** as Theme Builder templates (global) — see `elementor-global-templates`.
4. `create-page` "Home" (or reuse), then build sections 2–8 with Flexbox containers + native widgets, chunked (hero first, verify, append with `position:-1`).
5. Placeholder image widgets/backgrounds for each shot; register the barbell logo SVG.
6. Verify with `get-page-structure` + spot-check `get-element-settings`; check ≤900px and ≤600px.
7. On approval: publish + set as static front page (`show_on_front=page`, `page_on_front=<id>`).
