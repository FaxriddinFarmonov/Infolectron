def generate_voice(text: str) -> tuple[str, int]:
    """
    Returns: (file_path, duration_seconds)
    """
    # BU YERDA:
    # OpenAI / ElevenLabs / Azure TTS ulanish bo‘ladi
    # hozir abstract qoldiramiz

    file_path = "lesson_audio/sample.mp3"
    duration = len(text.split()) // 2

    return file_path, duration
