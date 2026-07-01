# 01 — MCP Recap & Why "Apps" Got Added

## MCP in one paragraph

MCP is a standard protocol (JSON-RPC based) that lets an LLM host (Claude
Desktop, an IDE, etc.) connect to external **servers** exposing three main
primitives: **tools** (functions the model can call), **resources** (data the
host/model can read), and **prompts** (reusable prompt templates). Before MCP
Apps, everything a tool returned was text, structured JSON, images, or links
— rendered as plain conversational content.

## The gap MCP Apps fills

Text-only responses break down for:
- **Exploring data** — "show me sales by region" as a wall of numbers vs. an
  interactive map you can click/hover/drill into.
- **Configuring many options at once** — instead of 10 back-and-forth
  questions ("which region?" "what size?" "autoscale?"), show a form with
  defaults and validation.
- **Rich media** — PDFs, 3D models, generated images need an actual viewer,
  not a description.
- **Real-time monitoring** — dashboards need a persistent connection that
  updates live, not "ask again for the latest status."
- **Multi-step workflows** — approvals/triage need navigation + state that
  persists across turns.

## Why not just send a link to a normal web app?

MCP Apps' pitch vs. "just build a website":
1. **Context preservation** — the UI lives inside the conversation; no tab
   switching or losing track of which thread had the dashboard.
2. **Bidirectional data flow for free** — the embedded app can call any tool
   on the same MCP server, and the host can push fresh data to it, reusing
   MCP's existing auth/session — no separate API/auth stack needed.
3. **Delegation to the host's other connected tools** — the app can ask the
   host to "schedule this meeting" and the host routes it through whatever
   the user already has connected, instead of the app author building direct
   integrations with every possible email/calendar provider.
4. **Security guarantees by construction** — sandboxed iframe means the host
   can safely render a UI from a server it doesn't fully trust.

## Who built it

Co-developed by Anthropic and OpenAI, building on the community **MCP-UI**
project. Shipped as **SEP-1865**, the first official MCP extension, announced
2026-01-26. Launch host support: Claude (web + desktop), ChatGPT, VS Code
Copilot, Goose — plus app/tool launch partners like Figma, Canva, Slack,
Salesforce, Asana, Box, monday.com, Clay, Hex, Amplitude.

## Video hook idea

Open with a side-by-side: same MCP tool call, one host shows a wall of JSON
text, the other shows a live interactive chart — that's the whole pitch in
one shot.
