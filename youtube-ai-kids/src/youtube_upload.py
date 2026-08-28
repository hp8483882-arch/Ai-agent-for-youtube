"""
Tayyor videoni YouTube'ga avtomatik yuklaydi (YouTube Data API v3).
Oldindan get_youtube_token.py orqali YT_REFRESH_TOKEN olingan bo'lishi kerak.
"""

import os
import google.oauth2.credentials
import googleapiclient.discovery
import googleapiclient.http


def _get_service():
    creds = google.oauth2.credentials.Credentials(
        token=None,
        refresh_token=os.environ["YT_REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["YT_CLIENT_ID"],
        client_secret=os.environ["YT_CLIENT_SECRET"],
        scopes=["https://www.googleapis.com/auth/youtube.upload"],
    )
    return googleapiclient.discovery.build("youtube", "v3", credentials=creds)


def upload_video(file_path, title, description, tags, is_short=False, privacy="public"):
    youtube = _get_service()

    if is_short and "#shorts" not in title.lower() and "#shorts" not in description.lower():
        description = description.rstrip() + "\n\n#shorts"

    body = {
        "snippet": {
            "title": title[:100],
            "description": description[:5000],
            "tags": tags[:15],
            "categoryId": "24",  # Entertainment
        },
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": True,
        },
    }

    media = googleapiclient.http.MediaFileUpload(file_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"  Yuklanmoqda: {int(status.progress() * 100)}%")

    video_id = response["id"]
    print(f"  Yuklandi: https://youtu.be/{video_id}")
    return video_id
