#!/usr/bin/env python3
"""Render Python Lisbon Meetup event images with the group's own image builder.

Usage:
    python3 render_images.py event.json [output_dir]

event.json:
{
  "title": "#15 Python Lisbon Meetup at Gapstars",
  "date": "2026-12-03",
  "time": "18:30",
  "location": "Gapstars, Edifício Atrium Saldanha, 11th floor",
  "description": "Talk title:\\nSubtitle\\nby Speaker\\n\\nPlus lightning talks, networking and socializing!",
  "formats": {                          # optional; these two are the defaults
    "widescreen": {"size": "1920,1080"},
    "square": {"size": "1080,1080",
               "location": "Gapstars, Atrium Saldanha, 11th floor",   # optional override
               "description": "..."}                                  # optional override
  }
}

Other sizes the builder supports: 1080,1350 (portrait), 1080,1920 (story), 1200,630 (landscape).
Optional top-level fields: "corner" (top-right | top-left | bottom-right | bottom-left), "font_scale" (75/100/125/150).

The description keeps \\n line breaks. The location is a single-line input and drops them.
Look at every output image afterwards and fix any line that ends with one orphaned word.

Needs: git, network access to github.com, and Python Playwright with Chromium.
"""
import base64
import functools
import http.server
import json
import os
import subprocess
import sys
import tempfile
import threading

REPO = "https://github.com/python-lisbon-meetup/python-lisbon-meetup.github.io.git"
DEFAULT_FORMATS = {"widescreen": {"size": "1920,1080"}, "square": {"size": "1080,1080"}}


def get_site() -> str:
    site = os.path.join(tempfile.gettempdir(), "pylm-site")
    if not os.path.isdir(os.path.join(site, "sharing")):
        subprocess.run(["git", "clone", "--depth", "1", REPO, site], check=True)
    return site


def serve(root: str) -> int:
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass

    handler = functools.partial(Quiet, directory=root)
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd.server_address[1]


def main() -> None:
    event = json.load(open(sys.argv[1], encoding="utf-8"))
    out_dir = sys.argv[2] if len(sys.argv) > 2 else "."
    os.makedirs(out_dir, exist_ok=True)
    port = serve(get_site())

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"http://127.0.0.1:{port}/sharing/")
        page.wait_for_function("!document.querySelector('#download').disabled", timeout=30000)
        for name, fmt in event.get("formats", DEFAULT_FORMATS).items():
            values = {
                "title": event["title"],
                "date": event["date"],
                "time": event.get("time", "18:30"),
                "location": fmt.get("location", event["location"]),
                "description": fmt.get("description", event.get("description", "")),
                "format": fmt["size"],
                "corner": event.get("corner", "top-right"),
                "font-scale": str(event.get("font_scale", 100)),
            }
            page.evaluate(
                """v => {
                    for (const [id, val] of Object.entries(v)) document.getElementById(id).value = val;
                    document.getElementById('editor').dispatchEvent(new Event('input'));
                }""",
                values,
            )
            data = page.evaluate("document.querySelector('#preview').toDataURL('image/png')")
            w, h = fmt["size"].split(",")
            path = os.path.join(out_dir, f"python-lisbon-{event['date']}-{name}-{w}x{h}.png")
            with open(path, "wb") as f:
                f.write(base64.b64decode(data.split(",", 1)[1]))
            print(path)
        browser.close()


if __name__ == "__main__":
    main()
