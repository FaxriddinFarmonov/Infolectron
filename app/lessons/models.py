import uuid
from django.db import models
from app.subjects.models import Subject


def lesson_upload_path(instance, filename):
    return f"lessons/{instance.id}/{filename}"


class Lesson(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="lessons"
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    word_file = models.FileField(upload_to=lesson_upload_path)
    presentation_file = models.FileField(upload_to=lesson_upload_path)
    video_url = models.URLField(blank=True)
    audio_file = models.FileField(upload_to=lesson_upload_path, blank=True)

    order = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order"]
        indexes = [
            models.Index(fields=["subject", "order"]),
        ]

    def __str__(self):
        return self.title


class LessonAudio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    lesson = models.OneToOneField(
        "lessons.Lesson",
        on_delete=models.CASCADE,
        related_name="audio"
    )

    audio_file = models.FileField(upload_to="lesson_audio/")
    duration = models.PositiveIntegerField(help_text="seconds")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["lesson"]),
        ]
