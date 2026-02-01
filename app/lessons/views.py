from rest_framework.generics import ListAPIView
from django.core.cache import cache
from rest_framework.permissions import IsAuthenticated

from app.lessons.selectors import lesson_list_by_subject_selector, get_lesson_audio
from app.lessons.serializers import LessonListSerializer
from app.common.pagination import LessonPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache

from app.lessons.selectors import lesson_detail_selector
from app.lessons.serializers import LessonDetailSerializer
from app.lessons.services import LessonViewService

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from app.lessons.models import Lesson





class LessonListView(ListAPIView):
    serializer_class = LessonListSerializer
    pagination_class = LessonPagination

    def get_queryset(self):
        subject_id = self.kwargs["subject_id"]
        cache_key = f"lessons:subject:{subject_id}"

        queryset = cache.get(cache_key)
        if not queryset:
            queryset = lesson_list_by_subject_selector(subject_id)
            cache.set(cache_key, queryset, timeout=60 * 10)

        return queryset



class LessonDetailView(APIView):

    def get(self, request, lesson_id):
        cache_key = f"lesson:detail:{lesson_id}"

        lesson = cache.get(cache_key)
        if not lesson:
            lesson = lesson_detail_selector(lesson_id)
            cache.set(cache_key, lesson, timeout=60 * 10)

        # 👀 View count Redis’da
        LessonViewService.increase_view(lesson_id)
        views = LessonViewService.get_views(lesson_id)

        serializer = LessonDetailSerializer(
            lesson,
            context={"views": views}
        )

        data = serializer.data
        data["views"] = views

        return Response(data, status=status.HTTP_200_OK)





class LessonFileDownloadView(APIView):

    def get(self, request, lesson_id, file_type):
        lesson = get_object_or_404(Lesson, id=lesson_id)

        if file_type == "word":
            file = lesson.word_file
        elif file_type == "ppt":
            file = lesson.presentation_file
        else:
            return Response(
                {"detail": "Invalid file type"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return FileResponse(
            file.open("rb"),
            as_attachment=True,
            filename=file.name.split("/")[-1]
        )


class LessonAudioView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, lesson_id):
        audio = get_lesson_audio(lesson_id)

        if audio:
            return Response({
                "audio_url": audio.audio_file.url,
                "duration": audio.duration
            })

        generate_lesson_audio_task.delay(lesson_id)

        return Response(
            {"status": "processing"},
            status=202
        )
