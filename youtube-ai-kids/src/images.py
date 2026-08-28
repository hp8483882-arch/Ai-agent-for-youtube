"""
Rasm generatori — Pollinations.ai (bepul, API kalit kerak emas).
Har bir sahna uchun bolalar multfilmi uslubidagi rasm yaratadi.
"""

import os
import time
import urllib.parse
import requests

STYLE_SUFFIX = (
    ", children's cartoon style, colorful, cute, friendly, soft lighting, "
    "storybook illustration, safe for kids, no text, no watermark"
)


def generate_image(prompt: str, out_path: str, width=1080, height=1920, seed=None):
    """Bitta rasmni yuklab, out_path ga saqlaydi."""
    full_prompt = prompt + STYLE_SUFFIX
    encoded = urllib.parse.quote(full_prompt)
    seed = seed if seed is not None else int(time.time() * 1000) % 1_000_000

    url = (
        f"https://image.pollinations.ai/prompt/{encoded}"
        f"?width={width}&height={height}&seed={seed}&nologo=true"
    )

    for attempt in range(3):
        try:
            resp = requests.get(url, timeout=90)
            resp.raise_for_status()
            with open(out_path, "wb") as f:
                f.write(resp.content)
            return out_path
        except Exception:
            if attempt == 2:
                raise
            time.sleep(5)


def generate_scene_images(scenes: list, out_dir: str, vertical: bool = True):
    """Har bir sahna uchun rasm yaratib, fayl yo'llari ro'yxatini qaytaradi."""
    os.makedirs(out_dir, exist_ok=True)
    width, height = (1080, 1920) if vertical else (1920, 1080)
    paths = []
    for i, scene in enumerate(scenes):
        out_path = os.path.join(out_dir, f"scene_{i:03d}.jpg")
        generate_image(scene["image_prompt"], out_path, width, height, seed=i)
        paths.append(out_path)
    return paths
