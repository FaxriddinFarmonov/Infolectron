from rest_framework import serializers
from app.lessons.models import Lesson


class LessonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = (
            "id",
            "title",
            "description",
            "word_file",
            "presentation_file",
            "video_url",
            "audio_file",
        )
class LessonDetailSerializer(serializers.ModelSerializer):
    subject = serializers.SerializerMethodField()
    views = serializers.IntegerField(read_only=True)

    class Meta:
        model = Lesson
        fields = (
            "id",
            "title",
            "description",
            "word_file",
            "presentation_file",
            "video_url",
            "audio_file",
            "subject",
            "views",
        )

    def get_subject(self, obj):
        return {
            "id": obj.subject.id,
            "title": obj.subject.title,
        }
