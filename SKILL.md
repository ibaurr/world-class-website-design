---
name: world-class-website-design
description: Research, design, redesign, and implement distinctive, high-quality websites. Use when creating a new website, redesigning an existing website, improving a website's visual design or UX, or adding polished motion and scrolling experiences.
---

# World-Class Website Design

## Purpose

Create distinctive, thoughtful, production-quality websites through a research-led design process and careful implementation.

This skill applies to both:
- **Redesigns:** Improve an existing website while preserving its identity, positioning, content, routes, and working functionality unless there is a clear reason to change them.
- **New websites:** Establish an original creative direction based on the product, audience, and requirements rather than defaulting to a generic template.

The goal is not to imitate a design gallery. It is to produce a coherent, memorable experience with excellent craft.

## Core principles

1. **Understand before changing.** Learn what the product or company does, who it serves, and what the website needs to achieve.
2. **Research before designing.** Inspect relevant references and identify useful design decisions; do not copy layouts or visual identities.
3. **Give every project its own identity.** Do not reuse the same visual direction, hero layout, section sequence, or decorative style across unrelated projects.
4. **Design with purpose.** Every section, animation, image, and interaction should support communication, usability, or brand character.
5. **Balance originality and clarity.** Be visually ambitious without making the website confusing or difficult to use.
6. **Build, inspect, and refine.** A design is not complete until the actual implementation has been reviewed at realistic viewport sizes.

## Workflow

### 1. Discover the project

Before editing files:

- Inspect the repository structure, framework, package manager, dependencies, scripts, and existing conventions.
- Run the existing project when possible and inspect the current rendered website.
- Review all relevant pages, routes, navigation, forms, calls to action, and interactive states.
- Understand the product, audience, positioning, value proposition, brand voice, and conversion goals.
- Identify existing assets, fonts, colors, design tokens, components, and integrations.
- For a redesign, treat the existing website and project materials as the source of truth. Do not invent product claims or remove important content and functionality without justification.

If essential information is unavailable, make conservative assumptions and clearly distinguish them from verified facts. Ask a question only when the missing information blocks meaningful progress.

### 2. Research visual references

When browser access or web research is available, inspect a varied selection of high-quality websites. Useful discovery sources include:

- https://www.awwwards.com/websites/
- https://www.siteinspire.com/
- https://www.siteofsites.co/
- https://curated.design/
- https://land-book.com/
- https://recent.design/
- https://minimal.gallery/
- https://www.landingfolio.com/
- https://saaslandingpage.com/
- https://www.lapa.ninja/
- https://www.framer.com/startups/ycombinator

Inspect actual pages and interactions where possible, not just thumbnails or search snippets.

Study:
- Art direction and brand expression.
- Composition, grids, spacing, and visual rhythm.
- Typography, hierarchy, and readable line lengths.
- Color, contrast, borders, surfaces, and texture.
- Hero sections and first-impression experiences.
- Navigation and information architecture.
- Product demonstrations and visual storytelling.
- Photography, illustration, 3D, and other assets.
- Motion, transitions, and interaction details.
- Responsive behavior.

Select references for specific reasons. Do not reproduce another site's distinctive design wholesale.

**Required research output:** Before implementing, produce a small **reference-comparison table** with columns `Reference (URL)`, `Observed`, `Adapted`, and `Why`. Usually include 2–4 genuinely inspected references. Explain exactly which idea is useful, how it will be transformed for this brand, and why. Distinguish direct observations from assumptions. If browsing is unavailable, write "No external reference verified" and make a brief table based only on locally accessible project examples, explicitly labeling them as such. Follow [design research](references/design-research.md).

If external browsing is unavailable, do not claim to have inspected these galleries. Work from available project context and state the limitation when relevant.

### 3. Establish creative direction

Before implementation, form a clear design direction appropriate to this specific brand and audience.

Define:
- The intended feeling and personality.
- Visual concept and art direction.
- Typography approach and hierarchy.
- Color palette and contrast strategy.
- Layout and grid principles.
- Image and illustration direction.
- Component and surface language.
- Motion principles.
- The relationship between brand expression and usability.

Use the existing identity as a starting point for redesigns. Preserve recognizable brand elements when they remain effective, but improve weak or inconsistent execution.

Record a concise creative-direction brief before implementation: audience, primary task/conversion, tone, visual concept, typography, color, layout, imagery, and motion. Use it to critique the rendered result. For typography—including font loading, fluid type scales, readable line lengths, localization, and RTL layouts—consult [typography](references/typography.md).

Avoid defaulting to:
- Generic SaaS landing-page structures.
- Unmotivated gradients and glow effects.
- Repetitive bento grids.
- Decorative blobs and generic AI imagery.
- Excessive cards, pills, borders, and shadows.
- Arbitrary oversized typography.
- Animation that delays or obscures information.

These patterns are not forbidden; use them only when they genuinely fit the project.

### 4. Plan the experience

Map the page or site structure before building.

- Prioritize the user's questions and tasks.
- Establish a clear hierarchy and logical content flow.
- Make the value proposition understandable quickly.
- Give each section a distinct purpose.
- Use visual variation without losing coherence.
- Keep calls to action clear and appropriately placed.
- Specify normal, empty, loading, error, success, and form-validation states for key journeys; use actionable, truthful microcopy. See [content design](references/content-design.md).
- Preserve important existing routes, content, integrations, and user journeys in redesigns.

Do not add sections simply to make a page longer. Do not remove useful content merely to achieve minimalism.

### 5. Design and implement

Work directly in the existing codebase unless the user requests a separate prototype.

- Follow the project's framework, conventions, and package manager.
- Reuse and improve existing components where sensible.
- Create reusable components and design tokens for repeated patterns.
- Use semantic HTML and accessible interaction patterns. Explicitly test keyboard navigation, visible focus, text/non-text contrast, accessible forms, and screen-reader behavior using [accessibility](references/accessibility.md).
- Use real project assets where available; do not invent testimonials, customer logos, statistics, awards, or product capabilities.
- Choose dependencies deliberately and avoid unnecessary packages.
- Ensure links, buttons, forms, menus, and other controls perform their intended actions.
- Keep responsive behavior intentional rather than merely shrinking desktop layouts.
- Optimize images, fonts, and loading behavior. Verify loading behavior and correct font shaping for every supported language, including RTL scripts.

Do not replace a working application with a static mockup. Do not claim an integration or interaction works unless it has been implemented and tested.

## Motion and scrolling standards

### Global smooth / eased scrolling

Smooth, eased scrolling is a default preference across website projects.

Aim for movement that feels fluid, controlled, and natural:
- Use smooth/eased scrolling where appropriate.
- Tune easing and duration so the page remains responsive to user input.
- Support mouse wheels, trackpads, keyboard navigation, and touch input.
- Keep anchor navigation smooth without causing confusing jumps.
- Avoid excessive smoothing, artificial lag, or a feeling that the page is detached from the user's input.
- Preserve expected browser behavior and avoid unnecessary scroll locking.
- Ensure the implementation works with sticky elements, dynamic content, and route changes.

Inspect the existing stack before choosing an implementation. A library such as Lenis may be appropriate, but it is not mandatory. Prefer native browser capabilities when they meet the design and accessibility requirements. Do not add a scrolling library just for its own sake.

Respect `prefers-reduced-motion`. Provide a reduced-motion experience and ensure core content and navigation remain available without animation.

### Optional section-specific scroll techniques

Use these selectively when they improve storytelling or comprehension:

- **Pinned sections:** Hold a section or visual in place while its content changes.
- **Scroll-driven animation:** Tie animation progress to scroll position.
- **Sticky storytelling:** Keep a visual fixed while related text or data changes.
- **Parallax:** Create restrained depth through layered movement.
- **Horizontal sequences:** Map vertical scroll to horizontal content movement when it is intuitive.
- **Section transitions:** Connect scenes or sections with purposeful transitions.
- **Micro-interactions:** Provide responsive feedback for hover, focus, press, and state changes.

Do not confuse smooth scrolling with scroll hijacking.

Avoid taking control of the entire page's scroll behavior. Users must not feel trapped. Preserve intuitive scrolling, keyboard access, touch behavior, browser history, and the ability to reach content directly. If a pinned or scroll-controlled section is used, provide a sensible mobile and reduced-motion alternative.

### Motion quality

- Motion should communicate hierarchy, state, continuity, or brand personality.
- Use consistent timing and easing.
- Avoid animating every element.
- Avoid layout shifts and animation that blocks reading or interaction.
- Prefer transform and opacity for performant effects where suitable.
- Keep essential content visible and usable if animation fails or is disabled.

## Quality assurance

Do not finish after the first implementation.

When tools and environment permit:

1. Run the project using its existing scripts.
2. Inspect the rendered website in a browser.
3. Review all relevant pages and important states.
4. Test desktop, tablet, and mobile viewport sizes.
5. Test navigation, links, forms, menus, and calls to action.
6. Test smooth scrolling with mouse wheel, trackpad, touch, and keyboard.
7. Check pinned sections and scroll animations for trapping, jitter, or layout issues.
8. Check reduced-motion behavior.
9. Inspect console errors and failed network assets.
10. Refine spacing, typography, alignment, responsive layouts, and motion.

If browser inspection or a particular test is unavailable, say so rather than claiming it passed.

Use the repeatable evaluation plan in [testing and QA](references/testing-and-qa.md). For the skill repository itself, run `python3 scripts/check_skill.py` to validate documentation contracts; this cannot replace functional or browser QA of a generated website.

## Definition of done

A project is ready when:

- Its design direction fits the actual brand and audience.
- The visual hierarchy and content flow are clear.
- The experience is coherent across pages and viewport sizes.
- Global smooth/eased scrolling feels polished without harming control.
- Optional motion techniques add value rather than friction.
- Existing essential functionality remains intact.
- Interactive elements work as intended.
- Accessibility and reduced-motion behavior have been considered.
- The implementation has been run and visually reviewed where possible.
- Known limitations are disclosed.

## Final response

Summarize:
- What changed.
- The creative direction and key design decisions.
- Important motion and scrolling behavior.
- Pages or components updated.
- Tests actually performed.
- Any remaining issues or limitations.
- The reference-comparison table and which sources were actually inspected.
- Accessibility and interface-state tests actually performed, and any checks left unverified.

Do not claim award-worthiness, perfect quality, or successful testing without evidence.
