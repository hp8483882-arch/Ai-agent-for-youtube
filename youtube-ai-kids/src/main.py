import os
import shutil
import traceback
from dotenv import load_dotenv

from script_generator import generate_script
from images import generate_scene_images
from tts import generate_scene_audio
from video_builder import build_video
from youtube_upload import upload_video

load_dotenv()

WORK_DIR = "work"


def make_and_upload(video_type: str, index: int):
    """video_type: 'shorts' yoki 'long'"""
    tag = f"{video_type}_{index}"
    scene_dir = os.path.join(WORK_DIR, tag)
    os.makedirs(scene_dir, exist_ok=True)

    print(f"[{tag}] Skript yozilmoqda...")
    data = generate_script(video_type)

    print(f"[{tag}] Rasmlar yaratilmoqda ({len(data['scenes'])} ta sahna)...")
    images = generate_scene_images(
        data["scenes"], os.path.join(scene_dir, "images"), vertical=(video_type == "shorts")
    )

    print(f"[{tag}] Ovoz yaratilmoqda...")
    audios = generate_scene_audio(data["scenes"], os.path.join(scene_dir, "audio"))

    print(f"[{tag}] Video yig'ilmoqda...")
    out_path = os.path.join(scene_dir, f"{tag}.mp4")
    build_video(
        data["scenes"], images, audios, out_path,
        vertical=(video_type == "shorts"),
        music_path="assets/background_music.mp3",
    )

    print(f"[{tag}] YouTube'ga yuklanmoqda...")
    upload_video(
        out_path,
        title=data["title"],
        description=data["description"],
        tags=data["tags"],
        is_short=(video_type == "shorts"),
    )

    shutil.rmtree(scene_dir, ignore_errors=True)


def main():
    os.makedirs(WORK_DIR, exist_ok=True)
    jobs = [("shorts", 1), ("shorts", 2), ("long", 1)]

    for video_type, index in jobs:
        try:
            make_and_upload(video_type, index)
        except Exception:
            print(f"XATOLIK ({video_type} {index}):")
            traceback.print_exc()
            # Bitta video muvaffaqiyatsiz bo'lsa ham, qolganlarini davom ettiramiz
            continue


if __name__ == "__main__":
    main()
