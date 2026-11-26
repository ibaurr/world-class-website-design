#!/usr/bin/env python3
"""Offline tests for scripts/analyze_site.py. No browser or network required."""
import argparse
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import analyze_site  # noqa: E402


def make_raw(**overrides):
    raw = {
        "title": "Fixture", "lang": "en", "docHeight": 3000, "scrollBehavior": "smooth",
        "text": {
            json.dumps([96, "700", "Georgia", 0.95, -0.03, "none", "h1"]): 20,
            json.dumps([48, "600", "Georgia", 1.2, 0, "none", "h2"]): 40,
            json.dumps([16, "400", "Georgia", 1.5, 0, "none", "p"]): 900,
        },
        "textColor": {"#111111": 900, "#f4efe6": 60},
        "bgColor": {"#f4efe6": 2000000.0, "#111111": 900000.0},
        "padY": {"160": 4, "80": 1}, "gaps": {"32": 3}, "maxW": {"1200": 2},
        "easing": {json.dumps([0.6, "cubic-bezier(0.16, 1, 0.3, 1)"]): 5},
        "props": {"transform": 5},
        "fonts": [["Inter", "400", "normal"], ["Inter", "400", "normal"]],
        "customProps": {"--ink": "#111111"}, "keyframes": ["rise"],
        "liveAnimations": 1, "animatedElements": 1, "sticky": 1, "willChange": 0,
        "blockedSheets": 0, "reducedMotionRules": 1, "scrollTimeline": 0, "viewTimeline": 0,
        "globals": {"GSAP": True, "Lenis": False},
        "scriptSrcs": ["https://cdn.example.com/lenis@1.0/lenis.min.js"],
        "canvases": [{"ctx": "webgl2", "w": 100, "h": 100}],
        "counts": {"sections": 3, "images": 2, "videos": 0, "svgs": 1, "iframes": 0,
                   "links": 4, "buttons": 1, "forms": 0},
        "headings": [["h1", "Make it unforgettable"]], "navLinks": ["Work", "About"],
    }
    raw.update(overrides)
    return raw


class SummarizeTests(unittest.TestCase):
    def test_type_styles_sorted_largest_first_with_fields_decoded(self):
        s = analyze_site.summarize(make_raw())
        self.assertEqual([t["size_px"] for t in s["type_styles"]], [96, 48, 16])
        self.assertEqual(s["type_styles"][0]["tag"], "h1")
        self.assertEqual(s["type_styles"][0]["letter_spacing_em"], -0.03)

    def test_type_scale_ratio_is_true_median(self):
        # Sizes 16, 48, 96 give steps 3.0 and 2.0; the median is 2.5.
        self.assertEqual(analyze_site.summarize(make_raw())["type_scale_median_ratio"], 2.5)

    def test_type_scale_ratio_none_with_fewer_than_three_sizes(self):
        raw = make_raw(text={json.dumps([16, "400", "A", 1.5, 0, "none", "p"]): 10})
        self.assertIsNone(analyze_site.summarize(raw)["type_scale_median_ratio"])

    def test_libraries_merge_globals_script_urls_and_webgl(self):
        libs = analyze_site.summarize(make_raw())["libraries"]
        self.assertEqual(libs, ["GSAP", "Lenis", "WebGL canvas"])

    def test_loaded_fonts_deduplicated(self):
        self.assertEqual(analyze_site.summarize(make_raw())["loaded_fonts"], ["Inter 400 normal"])

    def test_colors_ranked_by_weight(self):
        s = analyze_site.summarize(make_raw())
        self.assertEqual(s["background_colors"][0][0], "#f4efe6")
        self.assertEqual(s["text_colors"][0][0], "#111111")

    def test_motion_decoded(self):
        m = analyze_site.summarize(make_raw())["motion"][0]
        self.assertEqual((m["duration_s"], m["uses"]), (0.6, 5))


class ExtractorSourceTests(unittest.TestCase):
    def test_near_instant_transitions_are_ignored_in_page_script(self):
        # Production sites declare 0s/1ms transitions as placeholders; they are noise.
        self.assertIn("sec >= 0.01", analyze_site.EXTRACT_JS)


class RenderTests(unittest.TestCase):
    meta = {"viewport": "1440x900", "reduced_motion": False,
            "screenshots": [("00-scroll-0.png", 0)], "screenshot_dir": "screenshots"}

    def test_markdown_contains_every_section_and_the_caveat(self):
        md = analyze_site.render_markdown("https://example.com", analyze_site.summarize(make_raw()), self.meta)
        for heading in ("## Typography", "## Color", "## Spacing and layout", "## Motion",
                        "## Stack signals", "## Structure", "## Screenshots",
                        "## Limits of this measurement"):
            self.assertIn(heading, md)
        self.assertIn("never copy layouts", md)

    def test_empty_tables_render_a_placeholder_not_a_broken_table(self):
        raw = make_raw(easing={}, text={})
        md = analyze_site.render_markdown("https://example.com", analyze_site.summarize(raw), self.meta)
        self.assertIn("_None observed._", md)

    def test_unreadable_stylesheets_are_disclosed(self):
        s = analyze_site.summarize(make_raw(blockedSheets=3))
        md = analyze_site.render_markdown("https://example.com", s, self.meta)
        self.assertIn("3 cross-origin stylesheets unreadable", md)


class ArgumentTests(unittest.TestCase):
    def test_viewport_parsing(self):
        self.assertEqual(analyze_site.parse_viewport("1440x900"), (1440, 900))
        with self.assertRaises(argparse.ArgumentTypeError):
            analyze_site.parse_viewport("wide")

    def test_only_http_urls_accepted(self):
        self.assertEqual(analyze_site.parse_url("https://example.com"), "https://example.com")
        for bad in ("file:///etc/passwd", "javascript:alert(1)", "example.com", "http://"):
            with self.assertRaises(argparse.ArgumentTypeError, msg=bad):
                analyze_site.parse_url(bad)


if __name__ == "__main__":
    unittest.main()
