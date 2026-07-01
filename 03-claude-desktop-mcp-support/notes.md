# 03 — What Claude Desktop Specifically Supports

Claude Desktop has (at least) **three related but distinct** MCP-adjacent
capabilities. Worth being precise about this on camera since it's the part
most likely to confuse viewers.

## 1. MCP servers (the base protocol)

Claude Desktop can connect to MCP servers — local (stdio) or remote — giving
Claude tools/resources/prompts from that server. This is the foundational
layer everything else builds on. Configured historically via
`claude_desktop_config.json` / Settings.

## 2. MCPB — Desktop Extensions (`.mcpb` files)

- An `.mcpb` file = a zip archive containing a local MCP server + a
  `manifest.json`.
- One-click install: double-click the file, drag it into Claude Desktop, or
  Settings → Extensions → "Install Extension…".
- Runs locally on the user's machine over stdio; bundles its own
  dependencies; works offline; no OAuth needed.
- Good fit for: internal/corporate-firewalled systems, local tools, anything
  wanting to piggyback on existing SSO instead of implementing OAuth.
- Build flow: install `mcpb` CLI → build a stdio MCP server with the MCP SDK
  → `mcpb init` to generate the manifest → `mcpb pack` to bundle → test by
  double-clicking the `.mcpb`.
- Users get an install UI showing permissions + config before it runs.
- Previously called "DXT" (Desktop Extensions) — renamed to MCPB.
- There's also a public directory: Settings → Extensions → "Browse
  extensions" lists Anthropic-reviewed third-party extensions.

## 3. MCP Apps support (interactive UI rendering)

- Claude (both claude.ai web **and** Claude Desktop) is a launch host for MCP
  Apps as of the 2026-01-26 announcement.
- When a connected MCP server's tool declares a `ui://` resource, Claude
  Desktop renders it as a sandboxed iframe directly in the chat — dashboards,
  forms, 3D viewers, etc. — per the mechanism from episode 02.
- This works for MCP servers regardless of how they were connected (i.e. an
  MCPB-installed local server *or* a remote MCP server can both expose MCP
  Apps UI) — MCPB is the install mechanism, MCP Apps is the render mechanism,
  and they're orthogonal.
- Known rough edges: there's at least one open GitHub issue
  (`modelcontextprotocol/ext-apps#671`) about MCP Apps UI resources not
  rendering in Claude Desktop / claude.ai in some cases — worth a quick
  "this is bleeding edge, expect bugs" caveat in the video, and worth
  re-checking issue status before recording since it may be closed by then.

## How a viewer would actually try this today

1. Settings → Extensions in Claude Desktop.
2. Browse extensions (Anthropic-reviewed) or install a custom `.mcpb`.
3. If the installed server's tools declare MCP Apps UI resources, calling
   those tools in a normal conversation renders the interactive UI inline.
4. For remote MCP servers (no `.mcpb` needed), same MCP Apps rendering
   applies once the server is connected.

## Open questions to verify closer to recording (things move fast)

- [ ] Check `ext-apps` issue #671 status — still open / reproducible?
- [ ] Confirm current exact Settings path/wording in the shipping Claude
      Desktop build (UI text drifts between versions).
- [ ] Re-check the 2026-07-28 MCP spec RC once finalized — does it change
      anything about the Apps extension specifically, or just core MCP?

## Video hook idea

Screen-record the actual Settings → Extensions flow in Claude Desktop, then
trigger a tool call that renders an MCP App live, narrating which of the
three layers (MCP connection / MCPB install / MCP Apps render) is doing the
work at each step.
