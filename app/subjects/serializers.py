from rest_framework import serializers
from app.subjects.models import Subject


class SubjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ("id", "title", "description")
