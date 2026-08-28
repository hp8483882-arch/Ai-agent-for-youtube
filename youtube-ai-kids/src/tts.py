"""
Ovoz generatori — Aisha AI (aisha.group), o'zbek tiliga ixtisoslashgan TTS.

DIQQAT: Aisha AI'ning aniq API so'rov formati (endpoint, parametr nomlari)
ularning developer panelida beriladi va vaqt o'tishi bilan o'zgarishi mumkin.
Ro'yxatdan o'tgach https://aisha.group developer bo'limidan aniq
endpoint/parametrlarni oling va pastdagi AISHA_TTS_ENDPOINT hamda
so'rov tanasini (payload) shunga moslang -- bu yerda eng keng tarqalgan
REST TTS shakli (matn -> audio URL yoki audio bytes) namuna sifatida yozilgan.

Agar Aisha ishlamasa, muqobil sifatida SpeechGen.io yoki Maestra.ai kabi
'uz-UZ' ovozini qo'llab-quvvatlaydigan xizmatlardan birini shu funksiyalar
o'rniga ulashingiz mumkin -- pastdagi generate_speech() imzosini saqlang.
"""

import os
import requests

AISHA_TTS_ENDPOINT = "https://api.aisha.group/api/v1/tts/uz"  # devpaneldan tasdiqlang


def generate_speech(text: str, out_path: str, mood: str = "friendly", speed: float = 1.0) -> str:
    api_key = os.environ["AISHA_API_KEY"]

    resp = requests.post(
        AISHA_TTS_ENDPOINT,
        headers={"Authorization": f"Bearer {api_key}"},
        json={"text": text, "language": "uz", "mood": mood, "speed": speed},
        timeout=120,
    )
    resp.raise_for_status()

    content_type = resp.headers.get("content-type", "")
    if "audio" in content_type:
        audio_bytes = resp.content
    else:
        # Ba'zi TTS xizmatlari audio faylga havola qaytaradi
        audio_url = resp.json().get("audio_url") or resp.json()["url"]
        audio_bytes = requests.get(audio_url, timeout=120).content

    with open(out_path, "wb") as f:
        f.write(audio_bytes)
    return out_path


def generate_scene_audio(scenes: list, out_dir: str) -> list:
    os.makedirs(out_dir, exist_ok=True)
    paths = []
    for i, scene in enumerate(scenes):
        out_path = os.path.join(out_dir, f"scene_{i:03d}.mp3")
        generate_speech(scene["text"], out_path)
        paths.append(out_path)
    return paths
