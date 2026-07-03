"""Shared OAuth helper for YouTube Data API v3 scripts."""

import pathlib

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

HERE = pathlib.Path(__file__).parent
CLIENT_SECRET_PATH = HERE / "client_secret.json"
TOKEN_PATH = HERE / "token.json"
SCOPES = ["https://www.googleapis.com/auth/youtube"]


def get_youtube_client():
    if not CLIENT_SECRET_PATH.exists():
        raise SystemExit(
            f"Missing {CLIENT_SECRET_PATH}. Download your OAuth client JSON from "
            "Google Cloud Console and save it there first."
        )

    creds = None
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CLIENT_SECRET_PATH), SCOPES
            )
            creds = flow.run_local_server(port=0)
        TOKEN_PATH.write_text(creds.to_json())

    return build("youtube", "v3", credentials=creds)
