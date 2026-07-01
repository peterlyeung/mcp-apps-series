# 04 — Build Your First MCP App (hands-on)

## What we actually built

Not the official `basic-server-vanillajs` example — this machine has no
Node.js/npm and only Python 3.9 with no Homebrew/uv, and that example is a
Vite/TypeScript project requiring Node. Instead: a **from-scratch, dependency-
free MCP server in pure Python stdlib**, talking the raw wire protocol
directly. Arguably a *better* teaching example than the official one for a
video, since nothing is hidden behind an SDK — every JSON-RPC message on the
wire is visible in the code.

Files: `assets/dice-server/server.py` — single file, single tool
(`roll_dice`), one `ui://` resource.

## What it demonstrates

- **Core MCP handshake** — `initialize` → `notifications/initialized` →
  `tools/list` → `tools/call`, plus `resources/list`/`resources/read`, all
  hand-rolled over newline-delimited JSON-RPC on stdio (no SDK).
- **The MCP Apps tool declaration** — the `roll_dice` tool's `_meta.ui.resourceUri`
  points at `ui://dice-server/roller`.
- **The UI resource** — `text/html;profile=mcp-app` mime type, `_meta.ui.csp`
  / `_meta.ui.permissions` declared even though empty (no external domains
  needed — the page is fully self-contained inline HTML/JS).
- **The `ui/initialize` handshake from the app side** — the HTML page sends
  `ui/initialize` to `window.parent` via `postMessage`, waits for the host's
  result, then sends `ui/notifications/initialized`. This is the exact
  request/response shape from the spec (protocolVersion `2026-01-26`,
  `appCapabilities.availableDisplayModes`, etc.) — see episode 02 notes.
- **The full bidirectional loop from the sequence diagram** — the "Roll
  Again" button sends a `tools/call` JSON-RPC *request* straight from the
  iframe back through the host (matched by numeric `id`), the host forwards
  it to the real server, and the response updates the UI — without the model
  being re-prompted. This is the part that's easy to describe abstractly but
  clicks once you see the button visibly re-roll live.

## Exact steps taken

1. Confirmed environment: no `node`/`npm`, `python3` is 3.9.6, no `brew`, no
   `uv`. Claude Desktop *is* installed (`/Applications/Claude.app`) with an
   existing `claude_desktop_config.json`.
2. Pulled the exact MCP Apps wire-protocol shapes from
   `specification/2026-01-26/apps.mdx` in the `ext-apps` repo (tool `_meta.ui`
   fields, resource mime type, `ui/initialize` request/response, the
   `ui/notifications/tool-input` and `ui/notifications/tool-result`
   notifications) — see episode 02/00 source list.
3. Wrote `server.py`: a dispatch table over `initialize`, `tools/list`,
   `tools/call`, `resources/list`, `resources/read`; logging to **stderr**
   only (stdout is reserved for protocol messages — mixing them is the
   classic stdio-MCP-server bug).
4. **Sanity-tested it standalone before touching Claude Desktop at all** —
   piped a scripted sequence of JSON-RPC lines into `python3 server.py` and
   verified every response shape by hand. This caught issues early without
   needing the full app round-trip to debug.
5. Registered it in `~/Library/Application Support/Claude/claude_desktop_config.json`
   under `mcpServers.dice-server`, command `/usr/bin/python3`, args pointing
   at the absolute path of `server.py`. (Asked for explicit confirmation
   before editing this file since it's the user's live app config, not a
   project file.)
6. **Verified live in Claude Desktop** — restarted the app, asked it to
   "roll a d20," and the interactive card rendered inline showing "19 /
   rolled a 19 (d20)." Confirms the full loop end to end: model calls
   `roll_dice` → server responds → host renders the `ui://` resource in a
   sandboxed iframe → app's `ui/initialize` handshake completes → host pushes
   the result via `ui/notifications/tool-result` → app renders it.

## Gotchas / things worth calling out on camera

- **stdout vs stderr discipline** — any stray `print()` to stdout corrupts
  the JSON-RPC stream. This is probably the #1 first-timer bug and worth a
  dedicated beat in the video.
- **No SDK required at all** — MCP is "just" newline-delimited JSON-RPC over
  stdio; the SDKs are convenience, not magic. Good myth-busting moment for
  viewers intimidated by the ecosystem.
- **Sandboxed iframe origin is opaque** — `postMessage` target origin has to
  be `"*"` from the app side since a sandboxed iframe without
  `allow-same-origin` has a `null`/opaque origin.
- **Two different `tools/call` round trips** — one triggered by the model
  (arrives at the app as a `ui/notifications/tool-result` push), and one
  triggered by the app itself via a request/response it initiates directly
  (the "Roll Again" button). Easy to conflate; worth a clear before/after
  diagram on screen (reuse the mermaid sequence diagram from episode 02).
- Environment mismatch (no Node) turned into the actual hook for this
  episode: **you don't need the official SDK or even Node to build an MCP
  App** — worth leading with that instead of treating it as a workaround.

## Still to do before recording

- [x] Confirm live in Claude Desktop that the card renders — done, "rolled a
      19 (d20)" rendered correctly on first try.
- [ ] Click "Roll Again" a few times on camera to confirm the app-initiated
      `tools/call` round trip (not just the model-initiated one) also works,
      and capture a screen recording of it for `assets/`.
- [ ] Decide whether to also show the official `basic-server-vanillajs`
      TypeScript example side-by-side (would need Node installed) as a
      "here's the SDK-assisted version of the same thing" comparison.
