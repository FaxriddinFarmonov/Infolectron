from celery import shared_task
from app.lessons.models import Lesson, LessonAudio
from app.ai.voice import generate_voice


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=5)
def generate_lesson_audio_task(self, lesson_id):
    lesson = Lesson.objects.only("id", "content").get(id=lesson_id)

    audio_path, duration = generate_voice(
        text=lesson.content
    )

    LessonAudio.objects.update_or_create(
        lesson=lesson,
        defaults={
            "audio_file": audio_path,
            "duration": duration
        }
    )
