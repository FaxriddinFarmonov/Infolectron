from app.lessons.models import Lesson
from django.core.cache import cache
from app.lessons.models import LessonAudio


def lesson_list_by_subject_selector(subject_id):
    return (
        Lesson.objects
        .filter(subject_id=subject_id, is_active=True)
        .select_related("subject")
        .only(
            "id",
            "title",
            "description",
            "word_file",
            "presentation_file",
            "video_url",
            "audio_file",
            "order",
        )
        .order_by("order")
    )


def lesson_detail_selector(lesson_id):
    return (
        Lesson.objects
        .select_related("subject")
        .only(
            "id",
            "title",
            "description",
            "word_file",
            "presentation_file",
            "video_url",
            "audio_file",
            "subject__id",
            "subject__title",
        )
        .get(id=lesson_id, is_active=True)
    )



AUDIO_CACHE_KEY = "lesson_audio:{lesson_id}"


def get_lesson_audio(lesson_id):
    key = AUDIO_CACHE_KEY.format(lesson_id=lesson_id)

    cached = cache.get(key)
    if cached:
        return cached

    try:
        audio = LessonAudio.objects.select_related("lesson").get(
            lesson_id=lesson_id
        )
    except LessonAudio.DoesNotExist:
        return None

    cache.set(key, audio, timeout=60 * 60 * 24)
    return audio
