from django.urls import path
from app.lessons.views import (
    LessonListView,
    LessonDetailView,
    LessonAudioView,
    LessonFileDownloadView,
)

urlpatterns = [
    # Subject bo‘yicha darslar
    path("<uuid:subject_id>/", LessonListView.as_view(), name="lesson-list"),

    # Lesson detail
    path(
        "detail/<uuid:lesson_id>/",
        LessonDetailView.as_view(),
        name="lesson-detail",
    ),

    # Lesson audio
    path(
        "audio/<uuid:lesson_id>/",
        LessonAudioView.as_view(),
        name="lesson-audio",
    ),

    # Lesson file download
    path(
        "download/<uuid:lesson_id>/<str:file_type>/",
        LessonFileDownloadView.as_view(),
        name="lesson-download",
    ),
]
