#!/usr/bin/env python3
"""
Minimal MCP server exposing one tool (roll_dice) with an MCP Apps UI.

Built from scratch against the raw MCP + MCP Apps wire protocol (JSON-RPC
2.0, newline-delimited, over stdio) -- no SDK -- so every message on the
wire is visible here instead of hidden inside a framework. Only needs the
Python standard library (3.8+).

Wire format: one JSON-RPC 2.0 object per line on stdin/stdout, UTF-8.
stdout is reserved for protocol messages only -- all logging goes to stderr.
"""

import json
import random
import sys

PROTOCOL_VERSION = "2025-06-18"  # core MCP version this server speaks
UI_RESOURCE_URI = "ui://dice-server/roller"


def log(*args):
    print(*args, file=sys.stderr, flush=True)


def send(message: dict):
    sys.stdout.write(json.dumps(message) + "\n")
    sys.stdout.flush()


def send_result(request_id, result: dict):
    send({"jsonrpc": "2.0", "id": request_id, "result": result})


def send_error(request_id, code: int, message: str):
    send({"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}})


# ---------------------------------------------------------------------------
# The interactive UI, as a self-contained HTML/JS page. This is what Claude
# Desktop renders in a sandboxed iframe when the roll_dice tool is used.
# It speaks the MCP Apps postMessage/JSON-RPC dialect to the host directly.
# ---------------------------------------------------------------------------
UI_HTML = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  :root { color-scheme: light dark; }
  body {
    margin: 0; padding: 20px; box-sizing: border-box;
    font-family: var(--font-sans, -apple-system, sans-serif);
    color: var(--color-text-primary, #171717);
    display: flex; flex-direction: column; align-items: center; gap: 14px;
  }
  #die {
    font-size: 64px; line-height: 1; height: 80px;
    display: flex; align-items: center; justify-content: center;
  }
  #label { font-size: 14px; opacity: 0.7; }
  button {
    font-size: 14px; padding: 8px 18px; border-radius: 8px; border: none;
    cursor: pointer; background: #d97757; color: white;
  }
  button:disabled { opacity: 0.5; cursor: default; }
</style>
</head>
<body>
  <div id="die">...</div>
  <div id="label">waiting for roll</div>
  <button id="rollBtn" disabled>Roll Again</button>

<script>
(function () {
  var pending = {};
  var nextId = 1;
  var sides = 6;

  function post(message) {
    window.parent.postMessage(message, "*");
  }

  function call(method, params) {
    return new Promise(function (resolve) {
      var id = nextId++;
      pending[id] = resolve;
      post({ jsonrpc: "2.0", id: id, method: method, params: params || {} });
    });
  }

  function notify(method, params) {
    post({ jsonrpc: "2.0", method: method, params: params || {} });
  }

  function renderRoll(structured) {
    if (!structured) return;
    sides = structured.sides || sides;
    document.getElementById("die").textContent = structured.value;
    document.getElementById("label").textContent =
      "rolled a " + structured.value + " (d" + sides + ")";
    document.getElementById("rollBtn").disabled = false;
  }

  window.addEventListener("message", function (event) {
    var msg = event.data;
    if (!msg || msg.jsonrpc !== "2.0") return;

    // Response to a request we sent (matched by id)
    if (msg.id !== undefined && pending[msg.id]) {
      var resolve = pending[msg.id];
      delete pending[msg.id];
      resolve(msg.result);
      return;
    }

    // Notifications pushed from the host
    if (msg.method === "ui/notifications/tool-input") {
      document.getElementById("label").textContent = "rolling...";
    } else if (msg.method === "ui/notifications/tool-result") {
      renderRoll(msg.params && msg.params.structuredContent);
    }
  });

  document.getElementById("rollBtn").addEventListener("click", function () {
    document.getElementById("rollBtn").disabled = true;
    document.getElementById("label").textContent = "rolling...";
    call("tools/call", { name: "roll_dice", arguments: { sides: sides } })
      .then(function (result) {
        renderRoll(result && result.structuredContent);
      });
  });

  // Handshake with the host per the MCP Apps spec.
  call("ui/initialize", {
    protocolVersion: "2026-01-26",
    clientInfo: { name: "dice-roller-app", version: "0.1.0" },
    capabilities: {},
    appCapabilities: {
      availableDisplayModes: ["inline"],
      tools: { listChanged: false }
    }
  }).then(function () {
    notify("ui/notifications/initialized", {});
  });
})();
</script>
</body>
</html>
"""


def handle_initialize(msg):
    send_result(msg["id"], {
        "protocolVersion": PROTOCOL_VERSION,
        "capabilities": {
            "tools": {},
            "resources": {},
        },
        "serverInfo": {"name": "dice-server", "version": "0.1.0"},
    })


def handle_tools_list(msg):
    send_result(msg["id"], {
        "tools": [
            {
                "name": "roll_dice",
                "description": "Roll an N-sided die and show an interactive dice-roller UI.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "sides": {
                            "type": "integer",
                            "description": "Number of sides on the die",
                            "default": 6,
                        }
                    },
                },
                "_meta": {
                    "ui": {
                        "resourceUri": UI_RESOURCE_URI,
                    }
                },
            }
        ]
    })


def roll(arguments: dict) -> dict:
    sides = int(arguments.get("sides") or 6)
    sides = max(2, sides)
    value = random.randint(1, sides)
    return {"sides": sides, "value": value}


def handle_tools_call(msg):
    params = msg.get("params", {})
    name = params.get("name")
    if name != "roll_dice":
        send_error(msg["id"], -32602, "Unknown tool: %s" % name)
        return

    outcome = roll(params.get("arguments", {}))
    send_result(msg["id"], {
        "content": [
            {"type": "text", "text": "Rolled a %d on a d%d." % (outcome["value"], outcome["sides"])}
        ],
        "structuredContent": outcome,
    })


def handle_resources_list(msg):
    send_result(msg["id"], {
        "resources": [
            {
                "uri": UI_RESOURCE_URI,
                "name": "Dice Roller",
                "description": "Interactive dice-roller UI",
                "mimeType": "text/html;profile=mcp-app",
            }
        ]
    })


def handle_resources_read(msg):
    params = msg.get("params", {})
    uri = params.get("uri")
    if uri != UI_RESOURCE_URI:
        send_error(msg["id"], -32602, "Unknown resource: %s" % uri)
        return

    send_result(msg["id"], {
        "contents": [
            {
                "uri": UI_RESOURCE_URI,
                "mimeType": "text/html;profile=mcp-app",
                "text": UI_HTML,
                "_meta": {
                    "ui": {
                        "csp": {
                            "connectDomains": [],
                            "resourceDomains": [],
                            "frameDomains": [],
                            "baseUriDomains": [],
                        },
                        "permissions": {},
                        "prefersBorder": True,
                    }
                },
            }
        ]
    })


HANDLERS = {
    "initialize": handle_initialize,
    "tools/list": handle_tools_list,
    "tools/call": handle_tools_call,
    "resources/list": handle_resources_list,
    "resources/read": handle_resources_read,
}


def main():
    log("dice-server: starting, waiting for MCP messages on stdin")
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            log("dice-server: could not parse line: %r" % line)
            continue

        method = msg.get("method")
        has_id = "id" in msg

        if method == "notifications/initialized" or method == "notifications/cancelled":
            continue  # client notifications we don't need to act on

        if method in HANDLERS:
            try:
                HANDLERS[method](msg)
            except Exception as exc:  # keep the server alive on bad input
                log("dice-server: error handling %s: %s" % (method, exc))
                if has_id:
                    send_error(msg["id"], -32000, str(exc))
        elif has_id:
            send_error(msg["id"], -32601, "Method not found: %s" % method)
        else:
            log("dice-server: ignoring unknown notification: %s" % method)


if __name__ == "__main__":
    main()
