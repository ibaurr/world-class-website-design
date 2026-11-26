# Creative ambition

Use this when forming the creative-direction brief. Avoiding bad design produces a competent site; a distinctive one needs a clear idea, a deliberate level of risk, and at least one moment people remember. Decide all three before building.

## 1. Choose an ambition level

Pick one level for the project and record it in the brief with a one-line reason. The user's stated preference overrides these defaults.

| Level | Fits | What it allows | Motion |
| --- | --- | --- | --- |
| **Restrained** | Documentation, finance, health, government, checkout and account flows, content-dense sites | Craft through type, spacing, color, and one subtle detail. Conventional navigation and layout. | Hover, focus, and state transitions only. No scroll choreography. |
| **Expressive** | Product and marketing sites, studios, brands, launches | Distinctive typography, strong art direction, varied section composition, one signature moment, choreographed reveals. | A consistent motion system; scroll-linked effects where they explain or delight. |
| **Experimental** | Portfolios, campaigns, culture and creative work | Unconventional layout, navigation, or interaction; WebGL, shaders, or custom cursors. | Rich, but every effect needs a plain fallback and a usability check. |

Rules:
- Default to **Expressive** when the user gives no signal and the site is marketing-led; default to **Restrained** when the main job is a task (buying, reading, signing in).
- Do not use **Experimental** on a conversion-critical or task-critical flow without saying so and getting agreement. Keep an ordinary path to the same content and action.
- Higher ambition does not mean more effects. It means fewer, more deliberate ones, executed with more care.

## 2. State the big idea

Write one sentence: "This site feels like ___ because ___." Then show the idea in at least three of these: typography, color, layout, imagery, motion, copy tone.

Test: if the same design could be placed on an unrelated brand by swapping the logo and words, there is no big idea yet. Return to the brand, audience, and references.

## 3. Specify one signature moment

At Expressive and Experimental levels, name one moment a visitor could describe to someone else. Examples of the kind of thing, not a menu to copy from: a hero where the headline is itself the interaction, a pinned sequence that explains the product step by step, a transition that carries one object between sections, a typographic treatment that responds to the pointer.

Specify it before building:

- **Trigger:** what the visitor does or where they scroll.
- **Change:** what visibly happens, in one sentence.
- **Timing:** duration and easing, taken from the project's motion tokens.
- **Reduced motion:** what replaces it (usually the end state, shown immediately).
- **Mobile:** what replaces it on touch and small screens.
- **Budget:** the performance cost you will accept, then measure it.

Limit the site to one signature moment, or two at most. Everything else should support it rather than compete with it.

## 4. Craft details that separate polished from adequate

At Expressive and Experimental levels, check that:

- Easing and duration come from a small shared set of tokens, not per-element values.
- Every interactive element has a designed hover, focus, and pressed state.
- Selection color, scrollbar, cursor, favicon, and social preview image match the brand.
- Loading, empty, error, and 404 states share the site's voice and visual language.
- Type has been adjusted by eye: display sizes are tracked and leaded individually, and no headline is left with an orphaned word.
- Imagery shares one treatment (crop, color grade, grain, or framing) so unrelated sources read as one set.

## 5. Guardrails

Ambition never overrides these:

- Content and navigation remain usable with JavaScript animation off, with reduced motion on, and on a mid-range phone.
- Effects do not delay the first meaningful content or the primary action.
- Contrast, focus visibility, keyboard access, and zoom remain intact. See [accessibility](accessibility.md).
- Do not invent proof, assets, or claims to make a design feel richer. When real imagery is missing, build the visual language from type, color, layout, SVG, or procedural graphics, and say so.

## 6. Record it in the brief

Add these lines to the creative-direction brief:

```text
Ambition level: <restrained | expressive | experimental> — <one-line reason>
Big idea: This site feels like ___ because ___.
Signature moment: <trigger / change / timing / reduced-motion / mobile / budget>
```

At review time, judge the rendered result against these three lines, not against general taste.
