#!/usr/bin/env python3
"""Tear down a live website into measurable design facts.

Opens one page in a real browser (Playwright), scrolls through it, and records
what was actually rendered: fonts, type scale, colors, spacing, motion timing,
detected libraries, page structure, and screenshots at several scroll depths.

The output is evidence for the reference-comparison table in
references/design-research.md. It is a measurement of one render, not a
template: learn the underlying decisions, do not copy layouts, copy, or assets.

Usage:
    python3 scripts/analyze_site.py https://example.com --out teardown/example

Requires (only for this script, not for check_skill.py):
    pip install playwright && python3 -m playwright install chromium
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from pathlib import Path
from urllib.parse import urlparse

# --------------------------------------------------------------------------
# In-page extraction. Runs inside the browser and returns plain JSON data.
# --------------------------------------------------------------------------
EXTRACT_JS = r"""
() => {
  const MAX = 4000;
  const all = [document.documentElement, document.body, ...Array.from(document.querySelectorAll('body *'))].slice(0, MAX);
  const vw = window.innerWidth;

  const toHex = (c) => {
    const m = c.match(/rgba?\(([^)]+)\)/);
    if (!m) return null;
    const p = m[1].split(/[ ,\/]+/).filter(Boolean).map(Number);
    if (p.length >= 4 && p[3] === 0) return null;
    const h = (n) => Math.round(n).toString(16).padStart(2, '0');
    return '#' + h(p[0]) + h(p[1]) + h(p[2]);
  };
  const bump = (map, key, w = 1) => { map[key] = (map[key] || 0) + w; };
  const visible = (el, cs) => cs.display !== 'none' && cs.visibility !== 'hidden';

  const text = {}, textColor = {}, bgColor = {}, padY = {}, gaps = {}, maxW = {};
  const easing = {}, props = {};
  let sticky = 0, willChange = 0, animated = 0;

  for (const el of all) {
    const cs = getComputedStyle(el);
    if (!visible(el, cs)) continue;
    const r = el.getBoundingClientRect();
    const area = Math.max(0, Math.min(r.width, vw)) * Math.max(0, r.height);

    // Text styles, weighted by amount of text actually set in that style.
    let chars = 0;
    for (const n of el.childNodes) {
      if (n.nodeType === 3) chars += n.textContent.trim().length;
    }
    if (chars > 0) {
      const fam = cs.fontFamily.split(',')[0].replace(/["']/g, '').trim();
      const key = JSON.stringify([
        parseFloat(cs.fontSize), cs.fontWeight, fam,
        cs.lineHeight === 'normal' ? 'normal' : +(parseFloat(cs.lineHeight) / parseFloat(cs.fontSize)).toFixed(2),
        cs.letterSpacing === 'normal' ? 0 : +(parseFloat(cs.letterSpacing) / parseFloat(cs.fontSize)).toFixed(3),
        cs.textTransform, el.tagName.toLowerCase(),
      ]);
      bump(text, key, chars);
      const tc = toHex(cs.color);
      if (tc) bump(textColor, tc, chars);
    }
    const bg = toHex(cs.backgroundColor);
    if (bg) bump(bgColor, bg, area);

    if (cs.position === 'sticky') sticky++;
    if (cs.willChange && cs.willChange !== 'auto') willChange++;

    // Vertical rhythm of large blocks.
    if (r.width > vw * 0.6 && r.height > 120) {
      const pt = parseFloat(cs.paddingTop), pb = parseFloat(cs.paddingBottom);
      if (pt > 0) bump(padY, Math.round(pt));
      if (pb > 0) bump(padY, Math.round(pb));
    }
    if ((cs.display.includes('grid') || cs.display.includes('flex')) && cs.rowGap !== 'normal') {
      const g = Math.round(parseFloat(cs.rowGap));
      if (g > 0) bump(gaps, g);
    }
    if (cs.maxWidth !== 'none' && cs.maxWidth.endsWith('px')) bump(maxW, Math.round(parseFloat(cs.maxWidth)));

    // Motion timing declared in CSS.
    const durs = cs.transitionDuration.split(',').map((s) => s.trim());
    const eases = cs.transitionTimingFunction.split(/,(?![^(]*\))/).map((s) => s.trim());
    const tprops = cs.transitionProperty.split(',').map((s) => s.trim());
    durs.forEach((d, i) => {
      const sec = parseFloat(d) * (d.endsWith('ms') ? 0.001 : 1);
      if (sec >= 0.01) {  // ignore 0s/1ms placeholder transitions
        bump(easing, JSON.stringify([+sec.toFixed(3), eases[i % eases.length]]));
        bump(props, tprops[i % tprops.length]);
      }
    });
    if (cs.animationName !== 'none') animated++;
  }

  // Fonts that actually loaded.
  const fonts = [];
  document.fonts.forEach((f) => { if (f.status === 'loaded') fonts.push([f.family.replace(/["']/g, ''), f.weight, f.style]); });

  // Stylesheet-level facts (cross-origin sheets are unreadable; count them).
  let blockedSheets = 0, reducedMotionRules = 0, scrollTimeline = 0, viewTimeline = 0;
  const keyframes = new Set(), customProps = {};
  const walk = (rules) => {
    for (const rule of rules) {
      if (rule.type === CSSRule.KEYFRAMES_RULE) keyframes.add(rule.name);
      if (rule.media && /prefers-reduced-motion/.test(rule.media.mediaText)) reducedMotionRules++;
      const css = rule.cssText || '';
      if (/animation-timeline\s*:\s*(scroll|view)\(/.test(css)) {
        if (/view\(/.test(css)) viewTimeline++; else scrollTimeline++;
      }
      if (rule.selectorText === ':root' && rule.style) {
        for (const n of rule.style) if (n.startsWith('--')) customProps[n] = rule.style.getPropertyValue(n).trim();
      }
      if (rule.cssRules) walk(rule.cssRules);
    }
  };
  for (const sheet of document.styleSheets) {
    try { walk(sheet.cssRules); } catch (e) { blockedSheets++; }
  }

  // Libraries and rendering stack.
  const w = window;
  const globals = {
    'GSAP': !!w.gsap, 'ScrollTrigger': !!w.ScrollTrigger, 'Lenis': !!w.Lenis || !!document.querySelector('.lenis, html.lenis'),
    'Locomotive Scroll': !!w.LocomotiveScroll, 'Three.js': !!w.THREE, 'PixiJS': !!w.PIXI, 'Lottie': !!(w.lottie || w.bodymovin),
    'Swiper': !!w.Swiper, 'Barba': !!w.barba, 'Splitting': !!w.Splitting, 'Webflow': !!w.Webflow,
    'Next.js': !!w.__NEXT_DATA__, 'Nuxt': !!w.__NUXT__, 'Astro': !!document.querySelector('astro-island'),
    'Framer': !!document.querySelector('[data-framer-name], #__framer-badge-container') || /framer/i.test(document.querySelector('meta[name=generator]')?.content || ''),
  };
  const scriptSrcs = Array.from(document.scripts).map((s) => s.src).filter(Boolean);
  const canvases = Array.from(document.querySelectorAll('canvas')).map((c) => {
    let ctx = '2d/unknown';
    try { if (c.getContext('webgl2')) ctx = 'webgl2'; else if (c.getContext('webgl')) ctx = 'webgl'; } catch (e) {}
    return { ctx, w: c.width, h: c.height };
  });

  // Structure.
  const headings = Array.from(document.querySelectorAll('h1,h2,h3')).slice(0, 40)
    .map((h) => [h.tagName.toLowerCase(), h.textContent.trim().replace(/\s+/g, ' ').slice(0, 90)]);
  const navLinks = Array.from(document.querySelectorAll('header a, nav a')).slice(0, 20)
    .map((a) => a.textContent.trim().replace(/\s+/g, ' ').slice(0, 40)).filter(Boolean);

  return {
    title: document.title,
    lang: document.documentElement.lang || null,
    docHeight: document.documentElement.scrollHeight,
    scrollBehavior: getComputedStyle(document.documentElement).scrollBehavior,
    text, textColor, bgColor, padY, gaps, maxW, easing, props,
    fonts, customProps, keyframes: Array.from(keyframes).slice(0, 40),
    liveAnimations: document.getAnimations().length, animatedElements: animated,
    sticky, willChange, blockedSheets, reducedMotionRules, scrollTimeline, viewTimeline,
    globals, scriptSrcs, canvases,
    counts: {
      sections: document.querySelectorAll('section').length,
      images: document.images.length, videos: document.querySelectorAll('video').length,
      svgs: document.querySelectorAll('svg').length, iframes: document.querySelectorAll('iframe').length,
      links: document.links.length, buttons: document.querySelectorAll('button, [role=button]').length,
      forms: document.forms.length,
    },
    headings, navLinks,
  };
}
"""

SCRIPT_SIGNATURES = {
    "GSAP": r"gsap|tweenmax",
    "ScrollTrigger": r"scrolltrigger",
    "Lenis": r"lenis",
    "Locomotive Scroll": r"locomotive",
    "Three.js": r"three(\.module)?(\.min)?\.js|/three@",
    "OGL": r"/ogl",
    "PixiJS": r"pixi",
    "Lottie": r"lottie|bodymovin",
    "Swiper": r"swiper",
    "Barba": r"barba",
    "Framer Motion": r"framer-motion",
    "Splitting": r"splitting|split-type|splittype",
}


# --------------------------------------------------------------------------
# Pure post-processing (unit-testable without a browser).
# --------------------------------------------------------------------------
def top(counter: dict, n: int) -> list:
    """Return the n heaviest (key, weight) pairs of a dict, heaviest first."""
    return sorted(counter.items(), key=lambda kv: -kv[1])[:n]


def summarize(raw: dict) -> dict:
    """Turn raw browser measurements into a compact, ranked design summary."""
    type_styles = []
    for key, weight in top(raw["text"], 14):
        size, wt, fam, lh, ls, tt, tag = json.loads(key)
        type_styles.append({
            "size_px": size, "weight": wt, "family": fam, "line_height": lh,
            "letter_spacing_em": ls, "transform": tt, "tag": tag, "chars": weight,
        })
    type_styles.sort(key=lambda s: -s["size_px"])

    sizes = sorted({s["size_px"] for s in type_styles})
    ratio = None
    if len(sizes) >= 3:
        steps = [b / a for a, b in zip(sizes, sizes[1:]) if a > 0]
        ratio = round(statistics.median(steps), 2)

    motion = []
    for key, weight in top(raw["easing"], 8):
        dur, ease = json.loads(key)
        motion.append({"duration_s": dur, "easing": ease, "uses": weight})

    libs = {name for name, present in raw["globals"].items() if present}
    for src in raw["scriptSrcs"]:
        for name, pattern in SCRIPT_SIGNATURES.items():
            if re.search(pattern, src, re.I):
                libs.add(name)
    webgl = [c for c in raw["canvases"] if c["ctx"].startswith("webgl")]
    if webgl:
        libs.add("WebGL canvas")

    return {
        "title": raw["title"], "lang": raw["lang"], "doc_height_px": raw["docHeight"],
        "type_styles": type_styles, "type_scale_median_ratio": ratio,
        "loaded_fonts": sorted({f"{f[0]} {f[1]} {f[2]}" for f in raw["fonts"]}),
        "text_colors": [(c, int(w)) for c, w in top(raw["textColor"], 6)],
        "background_colors": [(c, int(w)) for c, w in top(raw["bgColor"], 6)],
        "section_padding_px": [(int(k), v) for k, v in top(raw["padY"], 6)],
        "layout_gaps_px": [(int(k), v) for k, v in top(raw["gaps"], 6)],
        "max_widths_px": [(int(k), v) for k, v in top(raw["maxW"], 4)],
        "css_variables": dict(list(raw["customProps"].items())[:40]),
        "motion": motion,
        "transition_properties": top(raw["props"], 6),
        "keyframes": raw["keyframes"],
        "live_animations": raw["liveAnimations"],
        "sticky_elements": raw["sticky"],
        "scroll_behavior": raw["scrollBehavior"],
        "css_scroll_timelines": raw["scrollTimeline"],
        "css_view_timelines": raw["viewTimeline"],
        "reduced_motion_rules": raw["reducedMotionRules"],
        "unreadable_stylesheets": raw["blockedSheets"],
        "libraries": sorted(libs),
        "canvases": raw["canvases"],
        "counts": raw["counts"],
        "headings": raw["headings"],
        "nav_links": raw["navLinks"],
    }


def _table(headers: list[str], rows: list[list]) -> str:
    if not rows:
        return "_None observed._\n"
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    out += ["| " + " | ".join(str(c) for c in row) + " |" for row in rows]
    return "\n".join(out) + "\n"


def render_markdown(url: str, s: dict, meta: dict) -> str:
    """Render the summary as a Markdown teardown a design brief can cite."""
    md = [f"# Site teardown: {s['title'] or url}", ""]
    md += [
        f"- URL: {url}",
        f"- Rendered at: {meta['viewport']} ({'reduced motion' if meta['reduced_motion'] else 'default motion'}), Chromium",
        f"- Page height: {s['doc_height_px']}px; lang: {s['lang'] or 'not set'}",
        f"- Screenshots: {len(meta['screenshots'])} in `{meta['screenshot_dir']}/`",
        "",
        "> Measured from one render. Use it as evidence for the reference-comparison table; "
        "adapt the underlying decisions, never copy layouts, copy, or assets.",
        "",
        "## Typography",
        "",
        _table(["Size px", "Weight", "Family", "Line height", "Tracking em", "Case", "Tag"],
               [[t["size_px"], t["weight"], t["family"], t["line_height"], t["letter_spacing_em"],
                 t["transform"], t["tag"]] for t in s["type_styles"]]),
        f"Median step between adjacent sizes: {s['type_scale_median_ratio'] or 'n/a'}x. "
        f"Loaded font faces: {', '.join(s['loaded_fonts']) or 'none detected'}.",
        "",
        "## Color",
        "",
        "Text colors (by amount of text): " + (", ".join(f"`{c}`" for c, _ in s["text_colors"]) or "none"),
        "",
        "Backgrounds (by area): " + (", ".join(f"`{c}`" for c, _ in s["background_colors"]) or "none"),
        "",
        "## Spacing and layout",
        "",
        f"- Large-block vertical padding (px, most common first): {[p for p, _ in s['section_padding_px']]}",
        f"- Flex/grid gaps (px): {[g for g, _ in s['layout_gaps_px']]}",
        f"- Max widths (px): {[w for w, _ in s['max_widths_px']]}",
        f"- Sections: {s['counts']['sections']}; sticky elements: {s['sticky_elements']}",
        "",
        "## Motion",
        "",
        _table(["Duration s", "Easing", "Uses"], [[m["duration_s"], f"`{m['easing']}`", m["uses"]] for m in s["motion"]]),
        f"- Scroll behavior: {s['scroll_behavior']}; CSS scroll timelines: {s['css_scroll_timelines']}; "
        f"view timelines: {s['css_view_timelines']}",
        f"- Live animations at capture: {s['live_animations']}; named keyframes: {', '.join(s['keyframes'][:12]) or 'none'}",
        f"- `prefers-reduced-motion` rules found: {s['reduced_motion_rules']}"
        + (f" ({s['unreadable_stylesheets']} cross-origin stylesheets unreadable, so this may undercount)"
           if s["unreadable_stylesheets"] else ""),
        "",
        "## Stack signals",
        "",
        f"- Libraries detected: {', '.join(s['libraries']) or 'none'}",
        f"- Canvases: {s['canvases'] or 'none'}",
        f"- Media: {s['counts']['images']} images, {s['counts']['videos']} videos, {s['counts']['svgs']} SVGs",
        "",
        "## Structure",
        "",
        "Navigation: " + (" · ".join(s["nav_links"]) or "not detected"),
        "",
        "Headings:",
        "",
    ]
    md += [f"- `{tag}` {text}" for tag, text in s["headings"][:25]] or ["_None._"]
    md += ["", "## Screenshots", ""]
    md += [f"- `{name}` (scrollY {y}px)" for name, y in meta["screenshots"]]
    md += ["", "## Limits of this measurement", "",
           "- JavaScript-driven animation (GSAP, Lenis, WebGL) is only visible through screenshots and detected libraries; "
           "tween durations and easings set in JS are not in the CSS motion table.",
           "- Values are from one viewport and one load. Re-run at another width to compare responsive behavior.",
           "- Detection is by global names and script URLs, so bundled or renamed libraries can be missed.", ""]
    return "\n".join(md)


# --------------------------------------------------------------------------
# Browser driver.
# --------------------------------------------------------------------------
def parse_viewport(value: str) -> tuple[int, int]:
    m = re.fullmatch(r"(\d{3,4})x(\d{3,4})", value)
    if not m:
        raise argparse.ArgumentTypeError("viewport must look like 1440x900")
    return int(m.group(1)), int(m.group(2))


def parse_url(value: str) -> str:
    parsed = urlparse(value)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise argparse.ArgumentTypeError("URL must start with http:// or https://")
    return value


def capture(url: str, out: Path, viewport: tuple[int, int], shots: int,
            reduced_motion: bool, timeout_ms: int) -> tuple[dict, dict]:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("Playwright is required: pip install playwright && python3 -m playwright install chromium")

    shot_dir = out / "screenshots"
    shot_dir.mkdir(parents=True, exist_ok=True)
    taken: list[tuple[str, int]] = []

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        context = browser.new_context(
            viewport={"width": viewport[0], "height": viewport[1]},
            reduced_motion="reduce" if reduced_motion else "no-preference",
        )
        page = context.new_page()
        page.goto(url, wait_until="load", timeout=timeout_ms)
        try:
            page.wait_for_load_state("networkidle", timeout=min(timeout_ms, 8000))
        except Exception:
            pass  # Long-polling sites never go idle; the load event is enough.
        page.wait_for_timeout(1500)  # Let intro animations and preloaders settle.

        height = page.evaluate("document.documentElement.scrollHeight")
        step = int(viewport[1] * 0.85)
        # Wheel input, not scrollTo, so smooth-scroll libraries respond as they would to a user.
        for i in range(shots):
            y = int(page.evaluate("window.scrollY"))
            name = f"{i:02d}-scroll-{y}.png"
            page.screenshot(path=str(shot_dir / name))
            taken.append((name, y))
            if y + viewport[1] >= height - 4:
                break
            page.mouse.wheel(0, step)
            page.wait_for_timeout(1100)
            height = page.evaluate("document.documentElement.scrollHeight")

        page.mouse.wheel(0, -height)
        page.wait_for_timeout(1200)
        raw = page.evaluate(EXTRACT_JS)
        browser.close()

    meta = {
        "viewport": f"{viewport[0]}x{viewport[1]}", "reduced_motion": reduced_motion,
        "screenshots": taken, "screenshot_dir": "screenshots",
    }
    return raw, meta


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Tear down a live website into measurable design facts.")
    ap.add_argument("url", type=parse_url)
    ap.add_argument("--out", type=Path, default=Path("teardown"), help="output directory (default: ./teardown)")
    ap.add_argument("--viewport", type=parse_viewport, default=(1440, 900), help="WIDTHxHEIGHT (default 1440x900)")
    ap.add_argument("--shots", type=int, default=8, help="maximum scroll-depth screenshots (default 8)")
    ap.add_argument("--reduced-motion", action="store_true", help="emulate prefers-reduced-motion: reduce")
    ap.add_argument("--timeout", type=int, default=45, help="page load timeout in seconds (default 45)")
    args = ap.parse_args(argv)

    args.out.mkdir(parents=True, exist_ok=True)
    raw, meta = capture(args.url, args.out, args.viewport, max(1, args.shots),
                        args.reduced_motion, args.timeout * 1000)
    summary = summarize(raw)
    (args.out / "teardown.json").write_text(json.dumps({"url": args.url, "meta": meta, "summary": summary},
                                                       indent=2), encoding="utf-8")
    (args.out / "teardown.md").write_text(render_markdown(args.url, summary, meta), encoding="utf-8")
    print(f"Wrote {args.out / 'teardown.md'}, teardown.json and {len(meta['screenshots'])} screenshots.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
