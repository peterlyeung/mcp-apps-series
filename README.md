# MCP Apps Video Series (working title)

Learning-first workspace for a planned video series on **MCP Apps** — the new
Model Context Protocol extension that lets MCP servers render interactive UI
(dashboards, forms, 3D viewers, etc.) directly inside chat clients like Claude
Desktop.

Right now the goal is just to **learn the topic**. Video production stuff
(scripts, recordings, thumbnails) can come later once the material is solid.

## Folder layout

Each episode gets its own numbered folder:

- `notes.md` — what I've learned, in my own words, with source links
- `script.md` — empty placeholder for a future video script
- `assets/` — empty placeholder for screenshots, diagrams, demo code, b-roll

```
00-series-overview/           series-level notes, glossary, source index
01-mcp-recap-why-apps/        quick MCP recap + why "Apps" was added
02-mcp-apps-deep-dive/        how MCP Apps works technically (protocol, security)
03-claude-desktop-mcp-support/ what Claude Desktop specifically supports (MCP Apps vs MCPB extensions vs connectors)
04-build-your-first-mcp-app/  hands-on: build + install a minimal MCP App
05-real-world-examples/       tour of official example servers, launch partners
```

Feel free to reorder/rename/merge episodes as the learning (and later, the
video plan) evolves — this is just a reasonable starting scaffold.

## Status

- [x] 00 — series overview / glossary drafted
- [x] 01 — MCP recap + why Apps drafted
- [x] 02 — MCP Apps deep dive drafted
- [x] 03 — Claude Desktop support drafted
- [x] 04 — hands-on build (dependency-free Python MCP server + MCP App built, unit-tested, and confirmed working live in Claude Desktop)
- [ ] 05 — examples tour (not started)

Spec status as of 2026-06-30: MCP Apps (SEP-1865) shipped Jan 26, 2026 as the
first official MCP extension. A broader MCP spec release candidate
(2026-07-28) is in progress — worth re-checking before recording, since
extensions can still evolve pre-final-spec.
