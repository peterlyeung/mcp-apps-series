# 00 — Series Overview & Glossary

## What this series is about

MCP (Model Context Protocol) has been about connecting LLMs to tools/data via
text. **MCP Apps** is a new extension that lets an MCP server hand back a
whole interactive UI (not just text/JSON) that renders live inside the chat
window. This series is about understanding that extension and specifically
how **Claude Desktop** implements/supports it.

## Glossary

- **MCP (Model Context Protocol)** — open protocol (Anthropic-originated, now
  broadly adopted) for connecting LLM apps to external tools, data, and
  prompts via a standard client/server JSON-RPC interface.
- **MCP Apps (SEP-1865)** — official MCP extension (shipped 2026-01-26) that
  lets a tool declare a `ui://` resource; the host renders that resource's
  HTML in a sandboxed iframe inside the conversation.
- **Host** — the client application embedding the MCP App, e.g. Claude
  Desktop, Claude.ai, VS Code Copilot, ChatGPT, Goose.
- **`ui://` resource** — an MCP resource (usually bundled HTML+JS+CSS) that
  represents the interactive UI for a tool.
- **App Bridge** — SDK module (`@modelcontextprotocol/ext-apps`) that hosts
  use to render apps in sandboxed iframes and manage the postMessage/JSON-RPC
  channel.
- **MCPB (MCP Bundle, `.mcpb` file)** — Claude Desktop's packaging format for
  *local* MCP servers as one-click-installable desktop extensions. Distinct
  from MCP Apps — MCPB is about *installing a server*, MCP Apps is about
  *rendering UI from a server's tool call*. (Formerly called "DXT".)
- **MCP-UI** — the community project MCP Apps built on top of/alongside;
  provides `@mcp-ui/client` React components for hosts.

## Key distinction to hammer home in the video

Two different things both live under "Claude Desktop + MCP UI," easy to
conflate:

1. **MCPB extensions** = how you *install* an MCP server into Claude Desktop
   (Settings → Extensions, `.mcpb` file, stdio transport, local).
2. **MCP Apps** = what happens *after* a tool call — the server returns a
   `ui://` resource and Claude Desktop renders an interactive iframe in the
   chat itself.

A single MCP server can use both: ship as an `.mcpb` for easy install, and
also expose tools that return MCP Apps UI.

## Source index (used across this series)

- MCP Apps overview: https://modelcontextprotocol.io/extensions/apps/overview
- MCP Apps announcement blog: https://blog.modelcontextprotocol.io/posts/2026-01-26-mcp-apps/
- Spec RC blog (2026-07-28): https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/
- ext-apps repo (spec + SDK + examples): https://github.com/modelcontextprotocol/ext-apps/
- MCP Apps API docs: https://apps.extensions.modelcontextprotocol.io/api/
- Claude MCPB build guide: https://claude.com/docs/connectors/building/mcpb
- Claude Desktop Extensions engineering post: https://www.anthropic.com/engineering/desktop-extensions
- Claude Help Center — local MCP servers: https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop
- The Register coverage: https://www.theregister.com/special-features/2026/01/26/claude-supports-mcp-apps-presents-ui-within-chat-window/4645652
