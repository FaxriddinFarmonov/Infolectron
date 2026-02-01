from rest_framework import serializers


class SubjectProgressSerializer(serializers.Serializer):
    subject = serializers.CharField(source="subject.title")
    completed_lessons = serializers.IntegerField()
    average_score = serializers.FloatField()


class TestHistorySerializer(serializers.Serializer):
    subject = serializers.CharField(source="test.lesson.subject.title")
    lesson = serializers.CharField(source="test.lesson.title")
    score = serializers.FloatField(source="score_percent")

class AdminSubjectAnalyticsSerializer(serializers.Serializer):
    subject = serializers.CharField(source="subject.title")
    total_students = serializers.IntegerField()
    average_score = serializers.FloatField()
