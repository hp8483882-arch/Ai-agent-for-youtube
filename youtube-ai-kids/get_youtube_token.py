"""
BIR MARTA, o'z kompyuteringizda ishga tushiring:
    python get_youtube_token.py

Brauzer ochiladi, Google hisobingiz (YouTube kanali ulangan) bilan
kiring va ruxsat bering. Terminalda chiqqan refresh_token qiymatini
.env fayliga (YT_REFRESH_TOKEN=...) va GitHub Secrets'ga qo'shing.

Oldindan Google Cloud Console'da:
1. Yangi loyiha yarating
2. "YouTube Data API v3" ni yoqing
3. OAuth consent screen sozlang (Test user sifatida o'zingizni qo'shing)
4. Credentials -> Create OAuth client ID -> Desktop app
5. client_id va client_secret'ni oling, pastga yoki .env ga yozing
"""

import os
from google_auth_oauthlib.flow import InstalledAppFlow
from dotenv import load_dotenv

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

client_config = {
    "installed": {
        "client_id": os.environ["YT_CLIENT_ID"],
        "client_secret": os.environ["YT_CLIENT_SECRET"],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": ["http://localhost"],
    }
}

flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
creds = flow.run_local_server(port=0)

print("\n\n=== BUNI .env FAYLIGA VA GITHUB SECRETS'GA SAQLANG ===")
print(f"YT_REFRESH_TOKEN={creds.refresh_token}")
