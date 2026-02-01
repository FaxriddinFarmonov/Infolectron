
import uuid
from django.db import models
from app.lessons.models import Lesson


class Test(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    lesson = models.OneToOneField(
        Lesson,
        on_delete=models.CASCADE,
        related_name="test"
    )

    total_questions = models.PositiveIntegerField(default=20)
    passing_score = models.PositiveIntegerField(default=60)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Test for {self.lesson.title}"


class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name="questions"
    )

    question_text = models.TextField()

    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)

    correct_answer = models.CharField(
        max_length=1,
        choices=[
            ("A", "A"),
            ("B", "B"),
            ("C", "C"),
            ("D", "D"),
        ]
    )

    class Meta:
        indexes = [
            models.Index(fields=["test"]),
        ]

    def __str__(self):
        return self.question_text
