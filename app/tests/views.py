from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from app.tests.selectors import get_test_questions_selector
from app.tests.services import TestSessionService, TestResultService
from app.tests.serializers import (
    StartTestSerializer,
    AnswerSerializer,
    FinishTestSerializer,
)
from app.tests.models import Test, Question
from app.results.models import TestResult


class StartTestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = StartTestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        test_id = serializer.validated_data["test_id"]
        user_id = request.user.id

        questions = get_test_questions_selector(test_id)
        TestSessionService.start_test(user_id, test_id, questions)

        data = [
            {
                "id": q.id,
                "question": q.question_text,
                "A": q.option_a,
                "B": q.option_b,
                "C": q.option_c,
                "D": q.option_d,
            }
            for q in questions
        ]

        return Response(data, status=status.HTTP_200_OK)


class SubmitAnswerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AnswerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        TestSessionService.submit_answer(
            user_id=request.user.id,
            test_id=serializer.validated_data["test_id"],
            question_id=str(serializer.validated_data["question_id"]),
            answer=serializer.validated_data["answer"],
        )

        return Response({"detail": "Answer saved"})


class FinishTestsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = FinishTestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        test_id = serializer.validated_data["test_id"]
        user_id = request.user.id

        session = TestSessionService.get_session(user_id, test_id)
        if not session:
            return Response(
                {"detail": "Test session expired"},
                status=status.HTTP_400_BAD_REQUEST
            )

        questions = get_test_questions_selector(test_id)
        correct, percent, total = TestResultService.calculate_score(
            questions,
            session["answers"]
        )

        TestResult.objects.update_or_create(
            user=request.user,
            test_id=test_id,
            defaults={
                "correct_answers": correct,
                "score_percent": percent,

            }
        )

        TestSessionService.finish_test(user_id, test_id)

        return Response(
            {
                "correct": correct,
                "percent": percent,
                "total": total,
            },
            status=status.HTTP_200_OK
        )
