# Repeatable visual and functional evaluation

This skill repository contains instructions, not a runnable website. Its automated CI check validates skill structure and required guidance; it does **not** prove that a generated website passes accessibility, UX, or browser tests.

## A repeatable agent evaluation

For a website built with this skill, record the project URL/commit, baseline screenshots, viewport sizes, browser, and test outcomes. Run the following:

| Step | Test and evidence |
| --- | --- |
| 1. Launch | Install and run using the existing package manager/scripts. Record any errors and the tested commit. |
| 2. Responsive screenshots | Capture and inspect representative pages at 320px mobile, 768px tablet, and 1440px desktop widths. Add project-specific breakpoints. |
| 3. Routes and controls | Exercise navigation, primary CTA, menus, links, dialogs, and forms, including empty/invalid/success/failure states when available. |
| 4. Accessibility | Perform the explicit keyboard, focus, contrast, forms, screen-reader, and reduced-motion cases in [accessibility](accessibility.md). Use axe or equivalent as an additional tool, not as a substitute for manual checks. |
| 5. Typography/locales | Check text wrapping, font swaps, zoom and supported multilingual/RTL variants using [typography](typography.md). |
| 6. Performance | Run a suitable profiler or Lighthouse in a realistic build; document measured values and testing conditions. Prioritize layout stability, responsiveness, and media loading. |
| 7. Refine | Compare screenshots to the design brief, list the three most serious observable defects, fix them, and repeat the affected checks. |

A critical blocker includes an inaccessible primary flow, a broken route/form, missing essential content, or a trapping animation. Do not average such blockers away with visual scores.

## Skill repository regression check

From this repository's root, run:

```bash
python3 scripts/check_skill.py
```

The checker uses the Python standard library. It validates the skill frontmatter, required reference paths, the design-research table contract, expected accessibility cases, and documented agent installation paths. GitHub Actions runs it for every pull request and pushes to main.

This is a **documentation contract test**. It intentionally does not claim a browser run or generated-site quality. When an actual site is available, apply the evaluation steps above and report real evidence.

## Reporting

For every review, include: pages/flows tested, viewport sizes, checks that passed, failures fixed, outstanding defects, and tests not executed due to missing tools or access.
