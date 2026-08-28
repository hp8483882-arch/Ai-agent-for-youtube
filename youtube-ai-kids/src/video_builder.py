"""
Video yig'uvchi: har bir sahna uchun (rasm + ovoz) ni Ken Burns
(sekin zoom) effekti bilan birlashtirib, subtitr qo'shib,
yakuniy mp4 faylni yig'adi.
"""

import os
from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    CompositeVideoClip,
    TextClip,
    concatenate_videoclips,
    CompositeAudioClip,
)


def _ken_burns(image_path, duration, size):
    clip = ImageClip(image_path).set_duration(duration)
    clip = clip.resize(lambda t: 1 + 0.04 * (t / duration))  # sekin zoom-in
    clip = clip.set_position(("center", "center")).resize(newsize=size)
    return clip


def _subtitle_clip(text, duration, size):
    txt = (
        TextClip(
            text,
            fontsize=int(size[0] * 0.055),
            color="white",
            stroke_color="black",
            stroke_width=2,
            method="caption",
            size=(int(size[0] * 0.9), None),
            font="DejaVu-Sans-Bold",
        )
        .set_duration(duration)
        .set_position(("center", "bottom"))
        .margin(bottom=int(size[1] * 0.06), opacity=0)
    )
    return txt


def build_video(scenes, image_paths, audio_paths, out_path, vertical=True, music_path=None):
    size = (1080, 1920) if vertical else (1920, 1080)
    scene_clips = []

    for scene, img_path, audio_path in zip(scenes, image_paths, audio_paths):
        audio = AudioFileClip(audio_path)
        duration = audio.duration + 0.3
        bg = _ken_burns(img_path, duration, size)
        sub = _subtitle_clip(scene["text"], duration, size)
        composed = CompositeVideoClip([bg, sub], size=size).set_audio(audio)
        scene_clips.append(composed)

    final = concatenate_videoclips(scene_clips, method="compose")

    if music_path and os.path.exists(music_path):
        bg_music = AudioFileClip(music_path).volumex(0.08)
        loops = int(final.duration // bg_music.duration) + 1
        bg_music = concatenate_videoclips([bg_music] * loops).set_duration(final.duration) \
            if hasattr(bg_music, "set_duration") else bg_music
        final_audio = CompositeAudioClip([final.audio, bg_music])
        final = final.set_audio(final_audio)

    final.write_videofile(
        out_path, fps=30, codec="libx264", audio_codec="aac", threads=4, preset="medium"
    )
    return out_path
