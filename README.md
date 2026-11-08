# World-Class Website Design

A reusable Agent Skill for research-led website design, redesign, frontend implementation, and polished motion experiences.

It gives compatible coding agents a repeatable process for understanding a project, researching design references, establishing a distinct creative direction, implementing the experience, and reviewing the rendered result.

## What it covers

- Design research with a **reference-comparison table** recording observations, adaptations, and rationale.
- Brand-aware creative direction and an explicit design brief.
- Typography: font loading, variable type scales, line length, multilingual scripts, and RTL layouts.
- Accessibility: keyboard, visible focus, contrast, forms, screen-reader behavior, reflow, and reduced motion.
- Meaningful content for empty, loading, error, validation, and success states.
- Website redesigns that preserve existing identity and functionality.
- Responsive, accessible frontend implementation and selective premium motion.
- Visual QA, iterative refinement, and repeatable documentation contract checks.

## Installation

Prerequisites: Git and a compatible installation of Claude Code or Codex. Run one of the following **from the root of the website project** where you want the skill available. These commands install the skill at project scope; the skill is available only to that project's agent sessions. Windows users can run them in Git Bash or WSL.

### Claude Code (project-level)

```bash
mkdir -p .claude/skills
git clone --depth 1 https://github.com/ibaurr/world-class-website-design.git .claude/skills/world-class-website-design
```

**Verification:** Confirm the file exists with `test -f .claude/skills/world-class-website-design/SKILL.md && echo "Skill installed"`. Start a fresh Claude Code session in this project and ask, "Which website design skill is available?" If your version supports the skills listing or slash-command discovery, check for `world-class-website-design`. Ask Claude Code to use the skill on a test page and verify it follows the research/design/QA workflow. Skill discovery and invocation can vary by client version.

### Codex (project-level)

```bash
mkdir -p .agents/skills
git clone --depth 1 https://github.com/ibaurr/world-class-website-design.git .agents/skills/world-class-website-design
```

**Verification:** Confirm the file exists with `test -f .agents/skills/world-class-website-design/SKILL.md && echo "Skill installed"`. Start a fresh Codex session from the project directory and request, "Use the $world-class-website-design skill to review this website." Where supported, use Codex's skill picker/listing to confirm discovery. Validate that it produces an actual reference-comparison table and reports tests performed, rather than merely claiming it used the skill.

### Updating an existing installation

```bash
git -C .claude/skills/world-class-website-design pull --ff-only
# Or for Codex:
git -C .agents/skills/world-class-website-design pull --ff-only
```

These commands assume the destination is a Git clone. If the directory already exists and is not a clone, inspect or remove it before running the installation command; do not overwrite local files blindly.

For alternative global/user-level installations or changes in discovery behavior, consult the current [Claude Code skills docs](https://code.claude.com/docs/en/skills) and [Codex skills docs](https://developers.openai.com/codex/skills).

## Usage

For an existing site:

```text
Use the world-class-website-design skill to redesign this existing website.
Inspect the existing product, brand, pages, and codebase first. Preserve essential
functionality. Produce a concise reference-comparison table and creative-direction
brief, implement the redesign, and review the actual rendered result.
```

For a new website:

```text
Use the world-class-website-design skill to design and build this website from
the brief. Define a distinctive visual direction, explain the references you
adapted and why, build responsive and accessible pages, and verify the results.
```

## Design philosophy

The skill is not a fixed template. Every project should establish its own visual identity and balance compelling design with usable, accessible interaction. Smooth/eased scrolling is a preference when it genuinely improves the experience; never sacrifice natural scrolling, accessibility, or performance to achieve it. Optional pinned sections, parallax, and scroll-driven storytelling should justify their complexity.

## Repository structure

```text
world-class-website-design/
├── SKILL.md
├── README.md
├── LICENSE
├── references/
│   ├── design-principles.md
│   ├── motion-and-scrolling.md
│   ├── design-research.md
│   ├── typography.md
│   ├── accessibility.md
│   ├── content-design.md
│   └── testing-and-qa.md
├── scripts/
│   └── check_skill.py
└── .github/workflows/
    └── skill-checks.yml
```

## Testing and verification

Run the dependency-free repository contract test:

```bash
python3 scripts/check_skill.py
```

GitHub Actions runs the same check on pull requests and pushes to main. It validates the skill's metadata, reference links, research-table contract, key test cases, and installation documentation. It **does not** test actual rendered websites. For a website produced by the skill, use the browser/functional regression procedure in [testing and QA](references/testing-and-qa.md).

## Contributing

Suggestions and improvements are welcome. Keep the skill reusable, brand-agnostic, accessible, and grounded in practical design and implementation principles.

## License

MIT. See [LICENSE](LICENSE).
