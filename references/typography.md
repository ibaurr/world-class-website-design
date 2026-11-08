# Typography and multilingual layout

Use this when selecting, implementing, or reviewing type systems. Typography must support readability, performance, and every language the site actually presents.

## Font selection and loading

- Choose typefaces based on brand tone, readability at small sizes, weight coverage, and required glyphs. Verify Arabic, Urdu, Hebrew, CJK, and accented Latin coverage instead of assuming one font supports every script.
- Prefer locally hosted, properly licensed WOFF2 subsets when appropriate. Avoid downloading multiple unused weights or loading a third-party font simply for decoration.
- Use `font-display: swap` or `optional` as appropriate; provide a metrics-compatible fallback font stack and verify that swapping does not cause major layout shifts.
- Preload only the font files needed by visible, above-the-fold content. Pair preloads with the correct `crossorigin` attribute when required; measure whether they improve loading.
- Prefer a variable font when it reduces the total font payload; request only the axes and ranges actually used. Be cautious with large variable fonts and multilingual subsets.
- Check that bold, italic, numerals, punctuation, and form controls render correctly in the chosen fallback fonts.

## Responsive type scales

- Define semantic typography tokens for display, heading, body, small text, captions, and controls. Reuse them instead of assigning unrelated sizes per section.
- Use `rem` for base sizing and accessible user scaling. `clamp()` can create fluid headings, but set readable minimums and reasonable maximums; do not prevent browser zoom.
- Example starting point, not a universal prescription:

```css
:root {
  --text-body: 1rem;
  --text-small: 0.875rem;
  --text-heading: clamp(1.75rem, 1.25rem + 2vw, 3rem);
  --text-display: clamp(2.75rem, 1.5rem + 5vw, 5.5rem);
  --leading-body: 1.5;
}
```

- Test wrapping at 320 CSS px, 200% zoom, and long translated strings. Avoid fixed-height text containers that clip when content expands.
- Start with roughly 45–75 characters per line for longer Latin-script body copy, then verify visually; this heuristic does not translate directly to every script. Use narrower display text measures and appropriate language-specific line breaking.

## Multilingual and RTL requirements

- Set the page's `lang` accurately and annotate language changes where needed (for example, `lang="ar"` or `lang="ur"`). Use `dir="rtl"` on the relevant document or container for right-to-left content; use `dir="auto"` for user-generated content when direction is unknown.
- Use CSS logical properties (`margin-inline-start`, `padding-inline`, `inset-inline-start`, `text-align: start`) to support both directions. Do not implement RTL as a naive horizontal mirror of the entire interface.
- Allow mixed-direction content—Arabic/Urdu text alongside Latin brands, email addresses, numbers, or URLs—to remain readable. Isolate dynamic mixed-direction tokens when necessary (for example, `<bdi>`).
- Check script-specific font shaping, ligatures, diacritics, baseline alignment, letter spacing, and paragraph rhythm. Do not apply Latin tracking conventions indiscriminately to connected Arabic scripts.
- Verify which directional icons actually need mirroring (back/forward arrows often do; logos, media controls, charts, and brand symbols generally do not).
- Test real copy, form inputs, dates, buttons, navigation, and error messages in both LTR and RTL at mobile and desktop widths.
