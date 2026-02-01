from rest_framework import serializers


class StartTestSerializer(serializers.Serializer):
    test_id = serializers.UUIDField()


class AnswerSerializer(serializers.Serializer):
    test_id = serializers.UUIDField()
    question_id = serializers.UUIDField()
    answer = serializers.ChoiceField(choices=["A", "B", "C", "D"])


class FinishTestSerializer(serializers.Serializer):
    test_id = serializers.UUIDField()
