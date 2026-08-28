"""
Skript generatori.
Groq (bepul) yoki Anthropic Claude API (arzon, sifatli) orqali
bolalar uchun o'zbek tilida video ssenariysi yozadi.

Chiqish formati (JSON):
{
  "title": "YouTube uchun sarlavha",
  "description": "YouTube tavsifi",
  "tags": ["bolalar", "..."],
  "scenes": [
     {"text": "Diktor matni (bir sahna uchun)", "image_prompt": "Rasm uchun ingliz tilida tavsif"},
     ...
  ]
}
"""

import os
import json
import requests

NICHE = os.getenv("CHANNEL_NICHE", "Bolalar uchun qiziqarli va ta'limiy AI hikoyalar")


def _build_prompt(video_type: str) -> str:
    if video_type == "shorts":
        length_hint = (
            "YouTube Shorts uchun, umumiy uzunligi 40-55 soniya bo'lsin. "
            "5-8 ta qisqa sahna yetarli."
        )
    else:
        length_hint = (
            "Uzun video uchun, umumiy uzunligi taxminan 10 daqiqa bo'lsin "
            "(o'rtacha ovoz tezligida ~1300-1500 so'z). 18-25 ta sahnaga bo'ling."
        )

    return f"""
Sen bolalar uchun YouTube kanali ssenaristisan. Kanal mavzusi: "{NICHE}".

Vazifa: {length_hint}
Til: o'zbek tili (lotin alifbosi), sodda, jonli, bolalarga tushunarli va xavfsiz
(zo'ravonlik, qo'rqinchli yoki nomaqbul mazmun bo'lmasin).

Faqat quyidagi JSON formatida javob ber, boshqa hech narsa yozma
(matn oldidan yoki keyin izoh, ``` belgilar ham kerak emas):

{{
  "title": "qiziqarli, bosiladigan sarlavha",
  "description": "YouTube uchun 2-3 gapli tavsif, oxirida tegishli hashtaglar",
  "tags": ["kalit so'z1", "kalit so'z2", "..."],
  "scenes": [
    {{"text": "shu sahnada diktor aytadigan o'zbekcha matn",
      "image_prompt": "shu sahna uchun rasm tavsifi, INGLIZ TILIDA, bolalar multfilmi uslubida, xavfsiz mazmunda"}}
  ]
}}
""".strip()


def _call_groq(prompt: str) -> str:
    api_key = os.environ["GROQ_API_KEY"]
    resp = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.9,
        },
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def _call_claude(prompt: str) -> str:
    api_key = os.environ["ANTHROPIC_API_KEY"]
    resp = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json={
            "model": "claude-haiku-4-5-20251001",
            "max_tokens": 4000,
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()["content"][0]["text"]


def generate_script(video_type: str = "shorts") -> dict:
    """video_type: 'shorts' yoki 'long'"""
    prompt = _build_prompt(video_type)

    if os.getenv("ANTHROPIC_API_KEY"):
        raw = _call_claude(prompt)
    elif os.getenv("GROQ_API_KEY"):
        raw = _call_groq(prompt)
    else:
        raise RuntimeError(
            "GROQ_API_KEY yoki ANTHROPIC_API_KEY o'rnatilmagan (.env fayliga qarang)"
        )

    raw = raw.strip()
    # Ba'zan model ```json bilan o'raydi -- tozalaymiz
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw)


if __name__ == "__main__":
    data = generate_script("shorts")
    print(json.dumps(data, ensure_ascii=False, indent=2))
