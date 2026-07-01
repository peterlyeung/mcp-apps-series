# 02 — MCP Apps Deep Dive: Protocol, Lifecycle, Security

## Core pattern

Two MCP primitives combined:
1. A **tool** whose description includes `_meta.ui.resourceUri` pointing to a
   `ui://` resource.
2. A **UI resource** — an HTML page (usually bundled with its own JS/CSS)
   that the host renders in place of/alongside plain tool output.

## Lifecycle, step by step

1. **UI preloading** — because the tool description already names the
   `ui://` resource, the host can prefetch it *before* the tool is even
   called (enables things like streaming tool inputs straight into the app).
2. **Resource fetch** — host fetches the HTML bundle from the server. Apps
   can also load external scripts/styles, but only from origins allow-listed
   in `_meta.ui.csp` (content-security-policy).
3. **Sandboxed rendering** — host renders the HTML in a sandboxed `<iframe>`
   in the conversation. `_meta.ui.permissions` can request extra capabilities
   (mic, camera, etc.), which the host may grant or deny.
4. **Bidirectional communication** — app ↔ host talk over JSON-RPC carried on
   `postMessage`. This is a *dialect* of MCP: some methods are shared with
   core MCP (`tools/call`), some are new and prefixed `ui/` (e.g.
   `ui/initialize`). Over this channel the app can:
   - request tool calls (which the host forwards to the real MCP server)
   - send messages into the conversation
   - update the model's context
   - receive pushed data/results from the host

## Sequence (mermaid, from the official docs)

```
User -> Agent: "show me analytics"
Agent -> Server: tools/call
Server -> Agent: tool input/result
Agent -> App (iframe): tool result pushed to app
User -> App: user interacts
App -> Agent: tools/call request
Agent -> Server: tools/call (forwarded)
Server -> Agent: fresh data
Agent -> App: fresh data
App -> Agent: context update
```

Key point: the app never talks to the MCP server directly — everything is
proxied through the host, which is what lets the host enforce security/consent
on every UI-initiated action just like a normal tool call.

## Security model (the part worth a dedicated segment)

- **Iframe sandbox** — app can't touch the parent DOM, can't read host
  cookies/localStorage, can't navigate the parent page or run scripts in the
  parent context.
- **All comms via postMessage** — no direct access; host mediates everything.
- **Host controls capabilities** — host decides which tools an app is allowed
  to call, can disable things like `sendOpenLink`.
- **Pre-declared templates** — because the UI resource is declared in the
  tool description ahead of time, hosts can review/cache/audit it before
  anything executes, rather than trusting arbitrary runtime-generated HTML.
- **Auditable JSON-RPC messaging** — every UI-initiated action rides the same
  audit/consent path as a direct tool call (i.e., no special back door for
  the embedded app to bypass user consent).

## Framework support

No required framework — it's standard web primitives (HTML/JS/CSS +
postMessage). Two implementation paths for *host* authors:
- `@mcp-ui/client` (React components for rendering/interacting with MCP Apps)
- **App Bridge**, part of the official SDK, handles iframe rendering, message
  passing, tool-call proxying, and security policy enforcement.

For *server/app* authors, `@modelcontextprotocol/ext-apps` provides an `App`
class as a convenience wrapper around the postMessage protocol — not
mandatory, you can implement the raw protocol yourself. Starter templates
exist for React, Vue, Svelte, Preact, Solid, and vanilla JS.

## Video hook idea

Draw the sequence diagram live on screen while narrating a real example (e.g.
a budget-allocator app) — this is the diagram that explains 80% of "how does
this actually work."
