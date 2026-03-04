from rest_framework import serializers
from .models import KDBEntry


class KDBSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = KDBEntry
        fields = ["id", "code", "title"]