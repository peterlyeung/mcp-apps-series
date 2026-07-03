#!/usr/bin/env python3
"""
Slides + narration -> video pipeline for the mcp-apps-series episodes.

Reads a reveal.js slide deck, pulls each slide's <aside class="notes">
as its narration script, synthesizes audio with Kokoro (offline TTS),
screenshots the slide with Playwright, and stitches image+audio pairs
into a single MP4 with MoviePy.

Usage:
    .venv/bin/python render.py <path/to/slides/index.html> [--out output.mp4] [--slides 1,2,3]
"""

import argparse
import pathlib
import re
import sys

from kokoro_onnx import Kokoro
import soundfile as sf
from playwright.sync_api import sync_playwright
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips

HERE = pathlib.Path(__file__).parent
MODEL_PATH = HERE / "models" / "kokoro-v1.0.onnx"
VOICES_PATH = HERE / "models" / "voices-v1.0.bin"
VOICE = "af_heart"
WIDTH, HEIGHT = 1280, 720


def extract_slide_notes(html_path: pathlib.Path) -> list[str]:
    html = html_path.read_text()
    sections = re.findall(r"<section\b.*?</section>", html, re.DOTALL)
    notes = []
    for section in sections:
        m = re.search(r'<aside class="notes">(.*?)</aside>', section, re.DOTALL)
        if not m:
            notes.append("")
            continue
        text = m.group(1)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        notes.append(text)
    return notes


def synthesize(kokoro: Kokoro, text: str, out_path: pathlib.Path) -> float:
    samples, sample_rate = kokoro.create(text, voice=VOICE, speed=1.0, lang="en-us")
    sf.write(str(out_path), samples, sample_rate)
    return len(samples) / sample_rate


def capture_slides(html_path: pathlib.Path, indices: list[int], out_dir: pathlib.Path) -> None:
    url = f"file://{html_path.resolve()}"
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": WIDTH, "height": HEIGHT})
        page.goto(url)
        page.wait_for_timeout(1200)
        current = 0
        for i in indices:
            while current < i:
                page.keyboard.press("ArrowRight")
                current += 1
            page.wait_for_timeout(700)
            page.screenshot(path=str(out_dir / f"slide-{i+1:02d}.png"))
        browser.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("slides_html", type=pathlib.Path)
    parser.add_argument("--out", type=pathlib.Path, default=HERE / "output" / "episode.mp4")
    parser.add_argument("--slides", type=str, default=None, help="comma-separated 1-based slide numbers, default all")
    args = parser.parse_args()

    work_dir = HERE / "output"
    work_dir.mkdir(exist_ok=True)

    all_notes = extract_slide_notes(args.slides_html)
    if args.slides:
        indices = [int(x) - 1 for x in args.slides.split(",")]
    else:
        indices = list(range(len(all_notes)))

    print(f"Found {len(all_notes)} slides, rendering {len(indices)} of them")

    print("Loading Kokoro model...")
    kokoro = Kokoro(str(MODEL_PATH), str(VOICES_PATH))

    print("Capturing slide screenshots...")
    capture_slides(args.slides_html, indices, work_dir)

    clips = []
    for i in indices:
        text = all_notes[i] or "This slide has no narration script yet."
        audio_path = work_dir / f"slide-{i+1:02d}.wav"
        print(f"Synthesizing narration for slide {i+1} ({len(text)} chars)...")
        duration = synthesize(kokoro, text, audio_path)

        image_path = work_dir / f"slide-{i+1:02d}.png"
        clip = ImageClip(str(image_path)).with_duration(duration + 0.4)
        audio_clip = AudioFileClip(str(audio_path))
        clip = clip.with_audio(audio_clip)
        clips.append(clip)
        print(f"  slide {i+1}: {duration:.1f}s narration")

    print("Concatenating clips...")
    final = concatenate_videoclips(clips, method="compose")
    args.out.parent.mkdir(exist_ok=True)
    final.write_videofile(str(args.out), fps=24, codec="libx264", audio_codec="aac")
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
