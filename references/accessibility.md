# Accessibility implementation and acceptance tests

Target WCAG 2.2 AA where applicable. Automated tools catch only a subset of accessibility failures; always include manual testing when a usable browser is available.

## Required test cases

| Area | Test action | Passing behavior |
| --- | --- | --- |
| Keyboard navigation | Navigate all major routes and controls with Tab, Shift+Tab, Enter, Space, arrow keys when applicable, and Escape for dismissible overlays. | Every interaction is operable without a pointer; focus follows a sensible order, and no keyboard trap occurs. |
| Visible focus | Tab through links, buttons, form inputs, menus, dialogs, and sticky headers. | Focus is clearly distinguishable on every interactive control and not hidden behind sticky UI. Do not remove outlines without an accessible replacement. |
| Contrast | Check body text, large text, controls, states, icons, and focus indicators with a contrast tool. | Normal text reaches at least 4.5:1, large text 3:1, and essential non-text UI indicators generally 3:1 unless a specific WCAG exception applies. |
| Accessible forms | Submit blank/invalid data, navigate labels and help text, and correct an error by keyboard. | Every control has an accessible name; required fields, instructions, and validation errors are understandable and programmatically associated; focus is managed appropriately. |
| Screen reader | Navigate landmarks, headings, links, buttons, form controls, dialogs, and dynamic status updates in NVDA, VoiceOver, or equivalent when available. | Structure and names are announced meaningfully, updates are conveyed without excessive interruptions, and controls communicate their states. |
| Reflow and zoom | Test 320 CSS px width, 200% zoom, and longer localized labels. | Content reflows without clipping or loss of essential functionality; avoid unnecessary two-dimensional scrolling. |
| Reduced motion | Enable `prefers-reduced-motion: reduce` and exercise navigation and animation-heavy sections. | Essential content and controls remain accessible without motion; interactions don't become unusable. |

## Implementation rules

- Prefer native semantic elements and their expected keyboard behavior over custom ARIA-heavy replacements.
- Provide a skip link for longer pages, sensible heading order, meaningful landmarks, accessible menu/dialog names, and logical focus restoration on dismiss.
- Associate each form control with an explicit visible label whenever possible. Do not use placeholder text as a substitute for labels. Surface errors near the field and in a useful summary when appropriate.
- Never rely on color alone to communicate state. Make error, success, disabled, selected, and required states clear in text and/or accessible semantics.
- Give meaningful images appropriate alternative text; mark purely decorative images as decorative. Icon-only buttons require accessible names.
- Use appropriate live regions for asynchronous status changes, and avoid announcing every decorative or intermediate animation step.
- Preserve browser zoom, focus visibility, keyboard scrolling, native links, and screen-reader access when adding scroll effects.

## Evidence and reporting

Report what was actually tested, the tool/device or screen reader used, failures found, fixes made, and what remains unverified. If there is no browser or assistive technology available, do not claim the manual tests passed. See [testing and QA](testing-and-qa.md).
