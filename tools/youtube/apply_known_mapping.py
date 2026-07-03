#!/usr/bin/env python3
"""
Update descriptions for the 6 mcp-apps-series episodes using an explicit,
hand-confirmed video ID mapping (no fuzzy title matching) - this channel
has 238+ videos, many of which also use "Episode NN" in their titles for
an unrelated life-sciences series, so fuzzy matching is unsafe here.

Video IDs below were confirmed via search.list(forMine=True, order='date')
on the @lifesciencesai channel, matching titles exactly:
  "Episode00 series overview", "Episode01 mcp recap why apps", etc.
"""

import argparse

from auth import get_youtube_client
from descriptions import load_all

# content json file -> confirmed YouTube video ID
VIDEO_ID_MAP = {
    "00.json": "cQ6P0Du86Mc",  # Episode00 series overview
    "01.json": "3gVjzFNrhlM",  # Episode01 mcp recap why apps
    "02.json": "5hFtElmVMiI",  # Episode02 mcp apps deep dive
    "03.json": "Wab6VCvD_Vk",  # Episode03 claude desktop mcp support
    "04.json": "RNoIwWMSsvs",  # Episode04 build your first mcp app
    "05.json": "h3WdDxxwHFA",  # Episode05 real world examples
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    episodes = {ep["file"]: ep for ep in load_all()}
    youtube = get_youtube_client()

    for file, video_id in VIDEO_ID_MAP.items():
        ep = episodes[file]
        current = (
            youtube.videos()
            .list(part="snippet", id=video_id)
            .execute()["items"][0]["snippet"]
        )
        print(f"--- {video_id}  ({current['title']}) ---")
        print(f"CURRENT description ({len(current.get('description', ''))} chars):")
        print(current.get("description") or "(empty)")
        print(f"\nNEW description ({len(ep['description'])} chars):")
        print(ep["description"])
        print()

        if args.apply:
            current["description"] = ep["description"]
            youtube.videos().update(
                part="snippet", body={"id": video_id, "snippet": current}
            ).execute()
            print(f"UPDATED {video_id}\n")

    if not args.apply:
        print("Dry run only. Re-run with --apply to write these descriptions.")


if __name__ == "__main__":
    main()
