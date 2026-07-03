#!/usr/bin/env python3
"""
Match this channel's uploaded videos to episodes by title, then update each
matched video's description.

By default this is a dry run: it only prints the proposed video -> episode
matches and the new description text. Nothing is written to YouTube unless
you pass --apply.
"""

import argparse
import difflib
import re

from auth import get_youtube_client
from descriptions import load_all


def normalize(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def best_match(video_title: str, episodes: list[dict]) -> tuple[dict, float] | None:
    norm_title = normalize(video_title)
    scored = []
    for ep in episodes:
        candidates = [ep["id"], ep["title"], ep["file"].replace(".json", "")]
        best = max(
            difflib.SequenceMatcher(None, norm_title, normalize(c)).ratio()
            for c in candidates
        )
        scored.append((ep, best))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[0] if scored else None


def list_channel_videos(youtube):
    channels = youtube.channels().list(part="contentDetails", mine=True).execute()
    uploads_playlist_id = channels["items"][0]["contentDetails"]["relatedPlaylists"][
        "uploads"
    ]

    videos = []
    page_token = None
    while True:
        resp = (
            youtube.playlistItems()
            .list(
                part="snippet",
                playlistId=uploads_playlist_id,
                maxResults=50,
                pageToken=page_token,
            )
            .execute()
        )
        for item in resp["items"]:
            snippet = item["snippet"]
            videos.append(
                {"videoId": snippet["resourceId"]["videoId"], "title": snippet["title"]}
            )
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    return videos


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--apply", action="store_true", help="Actually write the new descriptions to YouTube"
    )
    parser.add_argument(
        "--min-score",
        type=float,
        default=0.3,
        help="Minimum title-similarity score (0-1) to consider a match",
    )
    args = parser.parse_args()

    youtube = get_youtube_client()
    episodes = load_all()
    videos = list_channel_videos(youtube)

    print(f"Found {len(videos)} videos on the channel, {len(episodes)} episodes to match.\n")

    matches = []
    for v in videos:
        result = best_match(v["title"], episodes)
        if result is None:
            continue
        ep, score = result
        status = "MATCH" if score >= args.min_score else "no confident match"
        print(f"[{status}] score={score:.2f}  '{v['title']}'  ->  {ep['id']} ({ep['file']})")
        if score >= args.min_score:
            matches.append((v, ep))

    if not matches:
        print("\nNo confident matches found. Nothing to do.")
        return

    print(f"\n{len(matches)} video(s) will be updated:\n")
    for v, ep in matches:
        print(f"--- {v['title']} ({v['videoId']}) ---")
        print(ep["description"])
        print()

    if not args.apply:
        print("Dry run only (no changes made). Re-run with --apply to write these descriptions.")
        return

    for v, ep in matches:
        current = (
            youtube.videos()
            .list(part="snippet", id=v["videoId"])
            .execute()["items"][0]["snippet"]
        )
        current["description"] = ep["description"]
        youtube.videos().update(
            part="snippet", body={"id": v["videoId"], "snippet": current}
        ).execute()
        print(f"Updated {v['videoId']} ({v['title']})")


if __name__ == "__main__":
    main()
