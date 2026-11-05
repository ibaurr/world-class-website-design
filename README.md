# World-Class Website Design

A reusable Agent Skill for research-led website design, redesign, frontend implementation, and polished motion experiences.

It gives compatible coding agents a repeatable process for understanding a project, researching design references, establishing a distinct creative direction, implementing the experience, and reviewing the rendered result.

## What it covers

- Design research using leading website galleries.
- Brand-aware creative direction.
- UI/UX, layout, typography, color, and visual hierarchy.
- Website redesigns that preserve existing identity and functionality.
- Responsive, accessible frontend implementation.
- Global smooth/eased scrolling as a default design preference.
- Optional pinned sections, scroll-driven storytelling, parallax, and transitions.
- Browser-based visual QA and iterative refinement.

## Installation

This repository follows the Agent Skills format. Installation paths and discovery mechanisms vary by agent.

### Claude Code

Copy or clone this repository into the appropriate skills directory for your Claude Code setup. A common project-level location is:

```text
.claude/skills/world-class-website-design/
```

### Codex

Copy or clone the skill into a skills directory that your Codex environment discovers. A common repository-level location is:

```text
.agents/skills/world-class-website-design/
```

Consult your agent's current documentation for supported locations and installation behavior.

## Usage

Ask your coding agent to use the skill:

```text
Use the world-class-website-design skill to redesign this existing website.
Inspect the current product, brand, pages, and codebase first. Preserve essential
functionality, establish an original creative direction, implement the redesign,
and review the rendered result.
```

For a new website:

```text
Use the world-class-website-design skill to design and build this website from
the project brief. Establish a visual direction specific to this product and
audience before implementation.
```

## Design philosophy

The skill is intentionally not a fixed visual template. It defines a process and quality bar, not one universal aesthetic.

Every project should have its own visual identity. Smooth/eased scrolling is a default preference, while pinned sections, parallax, horizontal sequences, and scroll-driven storytelling are optional techniques that should be used only when they improve the experience.

## Repository structure

```text
world-class-website-design/
├── SKILL.md
├── README.md
├── LICENSE
├── references/
│   ├── design-principles.md
│   ├── motion-and-scrolling.md
│   └── design-research.md
└── assets/
    └── examples/
```

## Contributing

Suggestions and improvements are welcome. Keep the skill broadly reusable, brand-agnostic, and grounded in practical design and implementation principles.

## License

MIT. See [LICENSE](LICENSE).
