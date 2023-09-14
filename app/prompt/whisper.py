import openai
from app.core.config import config


openai_api_key = config.OPENAI_API_KEY
openai.api_key = openai_api_key


def whisper(
    file,
):
    with open("audio.mp3", "wb") as f:
        f.write(file)
    with open("audio.mp3", "rb") as f:
        transcript = openai.Audio.transcribe("whisper-1", f)
    return transcript["text"]
