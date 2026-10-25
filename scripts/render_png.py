#!/usr/bin/env python3
"""Rasterises every SVG in ./assets to a 2x transparent PNG in ./assets/png (needs Chromium).
PNGs show identical fonts and layout in every GitHub client, including the mobile app.
Run after build_assets.py: python3 scripts/render_png.py   (set CHROMIUM=/path/to/chromium if needed)"""
import os
import pathlib
import re
import shutil
import subprocess
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "assets"
DST = SRC / "png"
SCALE = 2


def chromium():
    for c in (os.environ.get("CHROMIUM"), "/opt/pw-browsers/chromium", shutil.which("chromium"),
              shutil.which("chromium-browser"), shutil.which("google-chrome")):
        if c and pathlib.Path(c).exists():
            return c
    raise SystemExit("Chromium not found; set CHROMIUM=/path/to/chromium")


def main():
    browser = chromium()
    shutil.rmtree(DST, ignore_errors=True)
    with tempfile.TemporaryDirectory() as tmp:
        for svg in sorted(SRC.rglob("*.svg")):
            w, h = (int(float(v)) for v in re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg.read_text()).groups())
            page = pathlib.Path(tmp) / "page.html"
            page.write_text(f'<html><body style="margin:0;background:transparent"><img src="file://{svg}" '
                            f'width="{w}" height="{h}" style="display:block"></body></html>')
            out = DST / svg.relative_to(SRC).with_suffix(".png")
            out.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run([browser, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                            "--force-prefers-reduced-motion", "--default-background-color=00000000",
                            f"--force-device-scale-factor={SCALE}", "--virtual-time-budget=2500",
                            f"--window-size={w},{h}", f"--screenshot={out}", f"file://{page}"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print("png rendered:", sum(1 for _ in DST.rglob("*.png")))


if __name__ == "__main__":
    main()
