# app/lessons/gttt.py
import sys
import os

# Loyiha root papkani sys.path ga qo'shamiz
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Django settings ni sozlash
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Infolectron.settings")
import django
django.setup()

import os
import django
import time
from gtts import gTTS
import pygame

# 1️⃣ Django kontekstini sozlash
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Infolectron.settings")  # settings.py joylashgan modul
django.setup()

# 2️⃣ Django models bilan ishlash mumkin (misol uchun)
from app.subjects.models import Subject


# 3️⃣ Matnni ovozga aylantirish funksiyasi
def play_text(text: str, lang: str = "uz"):
    tts = gTTS(text=text, lang=lang)
    tts.save("voice.mp3")

    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("voice.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(0.5)


# 4️⃣ Funksiyani chaqirish
if __name__ == "__main__":
    my_text = "Assalomu alaykum. Bu suniy intellekt tomonidan o‘qilayotgan prezentatsiya."
    play_text(my_text)
