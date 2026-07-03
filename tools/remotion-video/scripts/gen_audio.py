#!/usr/bin/env python3
"""
Generate narration audio for every slide in content/*.json, and rewrite
each content file in place with durationInFrames (at 30fps) and audioFile
(relative to public/) added to each slide.
"""

import json
import pathlib

from kokoro_onnx import Kokoro
import soundfile as sf

HERE = pathlib.Path(__file__).parent.parent
CONTENT_DIR = HERE / "content"
PUBLIC_AUDIO_DIR = HERE / "public" / "audio"
MODEL_PATH = HERE.parent / "render" / "models" / "kokoro-v1.0.onnx"
VOICES_PATH = HERE.parent / "render" / "models" / "voices-v1.0.bin"
VOICE = "af_heart"
FPS = 30
TAIL_PADDING_SECONDS = 0.6


def main():
    kokoro = Kokoro(str(MODEL_PATH), str(VOICES_PATH))

    for content_path in sorted(CONTENT_DIR.glob("*.json")):
        data = json.loads(content_path.read_text())
        episode_id = data["id"]
        audio_dir = PUBLIC_AUDIO_DIR / episode_id
        audio_dir.mkdir(parents=True, exist_ok=True)

        print(f"=== {episode_id} ({content_path.name}) ===")
        for i, slide in enumerate(data["slides"]):
            text = slide.get("narration", "").strip()
            if not text:
                slide["durationInFrames"] = 90
                continue

            filename = f"slide-{i+1:02d}.wav"
            out_path = audio_dir / filename
            samples, sample_rate = kokoro.create(
                text, voice=VOICE, speed=1.0, lang="en-us"
            )
            sf.write(str(out_path), samples, sample_rate)

            duration_seconds = len(samples) / sample_rate + TAIL_PADDING_SECONDS
            duration_frames = round(duration_seconds * FPS)

            slide["audioFile"] = f"audio/{episode_id}/{filename}"
            slide["durationInFrames"] = duration_frames

            print(f"  slide {i+1}: {duration_seconds:.1f}s ({duration_frames} frames)")

        content_path.write_text(json.dumps(data, indent=2) + "\n")

    print("Done.")


if __name__ == "__main__":
    main()
