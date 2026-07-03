"""Build a YouTube description for each episode from its content/*.json."""

import json
import pathlib

CONTENT_DIR = pathlib.Path(__file__).parent.parent / "remotion-video" / "content"
REPO_URL = "https://github.com/peterlyeung/mcp-apps-series"


def build_description(data: dict) -> str:
    title = data["title"]
    slides = data["slides"]

    subtitle = ""
    if slides and slides[0]["type"] == "title":
        subtitle = slides[0].get("subtitle", "")

    topics = [s["heading"] for s in slides if s.get("heading")]

    lines = [title]
    if subtitle:
        lines.append(subtitle)
    lines.append("")
    lines.append("Part of a series on MCP Apps (a new Model Context Protocol")
    lines.append("extension for interactive UI) and what Claude Desktop supports.")

    if topics:
        lines.append("")
        lines.append("In this video:")
        for t in topics:
            lines.append(f"- {t}")

    lines.append("")
    lines.append(f"Full write-up + working code: {REPO_URL}")

    return "\n".join(lines)


def load_all():
    episodes = []
    for path in sorted(CONTENT_DIR.glob("*.json")):
        data = json.loads(path.read_text())
        episodes.append({"file": path.name, "id": data["id"], "title": data["title"], "description": build_description(data)})
    return episodes


if __name__ == "__main__":
    for ep in load_all():
        print(f"=== {ep['file']} ({ep['id']}) ===")
        print(ep["description"])
        print(f"\n[{len(ep['description'])} characters]\n")
