#!/usr/bin/env python3
"""List all videos on the authenticated user's channel (title, video ID, description length)."""

from auth import get_youtube_client


def main():
    youtube = get_youtube_client()

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
                {
                    "videoId": snippet["resourceId"]["videoId"],
                    "title": snippet["title"],
                    "publishedAt": snippet["publishedAt"],
                    "descriptionLen": len(snippet.get("description", "")),
                }
            )
        page_token = resp.get("nextPageToken")
        if not page_token:
            break

    print(f"Found {len(videos)} videos:\n")
    for v in videos:
        print(f"  {v['videoId']}  {v['publishedAt'][:10]}  desc={v['descriptionLen']:4d}c  {v['title']}")


if __name__ == "__main__":
    main()
