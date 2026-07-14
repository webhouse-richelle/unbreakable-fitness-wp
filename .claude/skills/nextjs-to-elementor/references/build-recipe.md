# Container-model build recipe (elementor-mcp)

The technique proven on prior builds. Elementor supports both the classic
section/column model and the newer **container (flexbox)** model — use **containers**,
since the Next.js source is built with Tailwind fl/grid.

## Section = one top-level container

```jsonc
{
  "elType": "container",
  "settings": {
    "content_width": "full",              // full-bleed section
    "flex_direction": "column",           // stack the inner rows
    "padding": { "unit":"px", "top":64, "right":32, "bottom":64, "left":32,
                 "isLinked":false },       // .site-section py-16 + px-8 gutters
    "padding_mobile": { "unit":"px", "top":48, "right":24, "bottom":48, "left":24 },
    // background:
    "background_background": "classic",
    "background_color": "#FAF7F2"          // --cream section bg
    // OR image:
    // "background_image": { "url": "<sideloaded url>", "id": <attach id> },
    // "background_size": "cover", "background_position": "center center",
    // "background_overlay_color": "#102C7A",
    // "background_overlay_opacity": { "unit":"px", "size":0.6 }
  },
  "elements": [ /* inner row containers + widgets */ ]
}
```

## Row of columns

```jsonc
{
  "elType": "container",
  "settings": {
    "flex_direction": "row",
    "flex_direction_mobile": "column",    // ALWAYS stack on mobile
    "flex_gap": { "unit":"px", "size":32 },
    "content_width": "boxed",
    "width": { "unit":"px", "size":1400 } // .site-container max (1320 for mega/footer)
  },
  "elements": [
    { "elType":"container",
      "settings": { "width": {"unit":"%","size":50}, "width_mobile": {"unit":"%","size":100} },
      "elements": [ /* widgets */ ] }
  ]
}
```

## Widgets

Prefer the dedicated adders when building fresh, or embed widget objects in the
import tree:
- Heading → `elementor-mcp-add-heading` / `{ "elType":"widget","widgetType":"heading" }`
- Body copy → `add-text-editor`
- Image → `add-image` (use sideloaded `{url,id}` — see the SKILL editable-images rule)
- Button → `add-button` (radius 6px + tokens from design-tokens.md)
- Icon list / image box / testimonial / tabs / accordion / google-maps → matching adders
- Linkable card = wrap content in a container and set `settings.link: { "url": "<path>" }`

## Forms (Elementor Pro)

Enquiry/assessment form = a `form` widget with `form_fields[]` (name/email/phone/message),
plus `email_to` and `redirect_to`. On this site the booking flow lands on
`/book-free-assessment/thank-you`; generic forms redirect to `/thank-you`. Requires
Elementor Pro active. (In the Next.js source, forms POST to API routes that email via
Resend + create a Pipedrive lead — replicate the destination/redirect, not the backend.)

## Import + verify loop

```
elementor-mcp-delete-page-content(post_id)
elementor-mcp-import-template(post_id, [hero_container], position:-1)
elementor-mcp-get-page-structure(post_id)          # confirm hero landed
elementor-mcp-import-template(post_id, [section2, section3, ...], position:-1)
elementor-mcp-get-page-structure(post_id)          # confirm count/order vs source
```

- **Never blind-retry on a "Proxy error"/timeout — verify first.** The import often
  succeeded server-side even when the HTTP response failed.
- Keep each import small enough to return within the timeout; split by section.
- After building, spot-check with `elementor-mcp-get-element-settings` that colors,
  font family, and radii match the tokens.

## Responsive checklist (per section)

- Row containers: `flex_direction_mobile:"column"`.
- Column children: `width_mobile:{unit:"%",size:100}`.
- Reduce side padding on mobile (32→24px) and font sizes per the source Tailwind
  responsive prefixes. Breakpoints: `lg` 1024px (nav/layout), `md` 768px (typography/hero),
  and a `max-width:767px` hero-photo crop rule.
