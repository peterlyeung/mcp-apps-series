# mcp-apps-series videos (Remotion)

Code-driven video for all 6 episodes, built with [Remotion](https://github.com/remotion-dev/remotion)
(React + TypeScript). Replaced an earlier reveal.js/Mermaid/Playwright/MoviePy
pipeline (see `../render/`) after repeated, hard-to-diagnose layout bugs in
Mermaid's flowchart renderer. Remotion gives full manual control over layout
(plain React/CSS, hand-built SVG for the sequence diagrams) with no
auto-layout engine to fight, plus native audio-synced timing.

## Layout

- `content/*.json` — one file per episode. Each slide has a `type`
  (title, text, bullets, steps, twoColumn, grid, table, glossary, roadmap,
  partners, layers, sequence, sequenceWithBullets), its content, and a
  `narration` script. After running the audio script, each slide also gets
  `audioFile` and `durationInFrames` (at 30fps).
- `src/slides/*.tsx` — one component per slide type.
- `src/SlideRouter.tsx` — maps `type` to the right component.
- `src/Episode.tsx` — generic composition: lays out a slide array in
  sequence, each with its narration `<Audio>` track.
- `src/Root.tsx` — registers one `Composition` per episode (`Episode00`
  through `Episode05`), reading directly from `content/*.json`.
- `scripts/gen_audio.py` — generates narration WAVs via the Kokoro TTS venv
  at `../render/.venv` and writes `audioFile`/`durationInFrames` back into
  each content JSON. Re-run this after editing any `narration` text.
- `public/audio/` — generated WAVs (gitignored, regenerate with the script).
- `out/` — rendered MP4s (gitignored, regenerate with `npx remotion render`).

## Regenerating everything from scratch

```bash
# 1. Narration audio + durations (uses the existing Kokoro venv)
../render/.venv/bin/python scripts/gen_audio.py

# 2. Render one episode
npx remotion render Episode04 out/Episode04.mp4

# ...or preview interactively
npx remotion studio
```

## Editing content

Edit the relevant `content/NN.json` (heading text, bullets, diagram data,
narration), then re-run `gen_audio.py` (only regenerates what changed isn't
tracked — it currently re-synthesizes every slide) and re-render.
