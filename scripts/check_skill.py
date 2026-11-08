#!/usr/bin/env python3
"""Dependency-free contract check for the agent skill repository.

This tests skill metadata and instruction coverage, not generated websites.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []


def read(path: str) -> str:
    file = ROOT / path
    if not file.is_file():
        errors.append(f"Missing file: {path}")
        return ""
    return file.read_text(encoding="utf-8")


def require(label: str, text: str, items: list[str]) -> None:
    for item in items:
        if item.casefold() not in text.casefold():
            errors.append(f"{label}: missing required phrase: {item}")


skill = read("SKILL.md")
readme = read("README.md")
research = read("references/design-research.md")
typography = read("references/typography.md")
accessibility = read("references/accessibility.md")
content = read("references/content-design.md")
testing = read("references/testing-and-qa.md")
read("references/design-principles.md")
read("references/motion-and-scrolling.md")

if not re.match(r"\A---\nname: world-class-website-design\ndescription: .+\n---\n", skill):
    errors.append("SKILL.md: invalid or missing Agent Skills frontmatter")

for path in sorted(set(re.findall(r"references/[\w-]+\.md", skill))):
    read(path)

require("SKILL.md", skill, [
    "reference-comparison table", "references/typography.md",
    "references/accessibility.md", "references/content-design.md",
    "references/testing-and-qa.md",
])
require("Design research", research, [
    "| Reference", "| Observed", "| Adapted", "| Why",
    "No external reference verified",
])
require("Typography", typography, [
    "font-display", "woff2", "clamp()", "line length",
    'dir="rtl"', 'lang="ar"', "logical properties",
])
require("Accessibility", accessibility, [
    "keyboard navigation", "visible focus", "contrast",
    "accessible forms", "screen reader", "4.5:1", "3:1",
])
require("Content design", content, [
    "empty", "loading", "error", "success", "validation", "microcopy",
])
require("Testing", testing, [
    "320px", "768px", "1440px", "python3 scripts/check_skill.py",
    "manual", "documentation contract test",
])
require("README", readme, [
    ".claude/skills/world-class-website-design",
    ".agents/skills/world-class-website-design",
    "python3 scripts/check_skill.py",
    "verification",
])
if not (ROOT / ".github/workflows/skill-checks.yml").is_file():
    errors.append("Missing GitHub Actions regression workflow")

if errors:
    print("Skill contract check FAILED:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)

print("Skill contract check PASSED: metadata, references, and guidance present.")
