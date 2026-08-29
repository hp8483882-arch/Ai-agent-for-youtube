import asyncio
import os
import edge_tts


def generate_audio(text, output_path="audio.mp3"):
    """Matnni Edge-TTS orqali ovozga aylantiradi."""

    async def _main():
        communicate = edge_tts.Communicate(text, "uz-UZ-MadinaNeural")
        await communicate.save(output_path)

    asyncio.run(_main())
    return output_path


if __name__ == "__main__":
    generate_audio(
        "Akkurat va qiziqarli ertaklar dunyosiga xush kelibsiz!", "test.mp3"
    )
    print("Ovoz muvaffaqiyatli yaratildi: test.mp3")
