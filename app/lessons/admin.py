from django.contrib import admin
from app.lessons.models import Lesson, LessonAudio


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "subject",
        "order",
        "is_active",
        "created_at",
    )
    list_filter = ("subject", "is_active")
    search_fields = ("title", "description")
    ordering = ("subject", "order")
    autocomplete_fields = ("subject",)


@admin.register(LessonAudio)
class LessonAudioAdmin(admin.ModelAdmin):
    list_display = (
        "lesson",
        "duration",
        "created_at",
    )
    search_fields = ("lesson__title",)
