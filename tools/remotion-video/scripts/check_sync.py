#!/usr/bin/env python3
"""Verify each slide's narration audio fits within its allocated on-screen slot."""

import json
import pathlib
import soundfile as sf

HERE = pathlib.Path(__file__).parent.parent
CONTENT_DIR = HERE / "content"
PUBLIC_DIR = HERE / "public"
FPS = 30

problems = []

for content_path in sorted(CONTENT_DIR.glob("*.json")):
    data = json.loads(content_path.read_text())
    episode_id = data["id"]
    total_frames = 0
    print(f"=== {episode_id} ===")
    for i, slide in enumerate(data["slides"]):
        duration_frames = slide.get("durationInFrames")
        audio_file = slide.get("audioFile")
        total_frames += duration_frames or 0

        if not audio_file:
            print(f"  slide {i+1}: no audio ({duration_frames} frames, silent)")
            continue

        wav_path = PUBLIC_DIR / audio_file
        if not wav_path.exists():
            problems.append(f"{episode_id} slide {i+1}: audio file missing: {wav_path}")
            continue

        info = sf.info(str(wav_path))
        audio_seconds = info.frames / info.samplerate
        slot_seconds = duration_frames / FPS
        slack = slot_seconds - audio_seconds

        flag = ""
        if slack < 0:
            flag = "  <<< AUDIO LONGER THAN SLOT, WILL BE CUT OFF"
            problems.append(
                f"{episode_id} slide {i+1}: audio {audio_seconds:.2f}s > slot {slot_seconds:.2f}s"
            )
        elif slack > 1.5:
            flag = f"  <<< {slack:.2f}s of dead air, unusually large gap"
            problems.append(
                f"{episode_id} slide {i+1}: {slack:.2f}s slack (audio {audio_seconds:.2f}s, slot {slot_seconds:.2f}s)"
            )

        print(
            f"  slide {i+1}: audio={audio_seconds:.2f}s slot={slot_seconds:.2f}s slack={slack:.2f}s{flag}"
        )

    print(f"  TOTAL: {total_frames} frames = {total_frames/FPS:.2f}s")

print()
if problems:
    print("ISSUES FOUND:")
    for p in problems:
        print(" -", p)
else:
    print("No sync issues found: every slide's audio fits its slot with a normal tail buffer.")
