import uuid
from django.db import models
from app.users.models import User
from app.tests.models import Test


class  TestResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)

    correct_answers = models.PositiveIntegerField()
    score_percent = models.FloatField()

    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "test")
        indexes = [
            models.Index(fields=["user", "test"]),
        ]
class SubjectProgress(models.Model):
    """
    Fan bo‘yicha umumiy progress (per user)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey("subjects.Subject", on_delete=models.CASCADE)

    completed_lessons = models.PositiveIntegerField(default=0)
    average_score = models.FloatField(default=0)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "subject")
        indexes = [
            models.Index(fields=["user", "subject"]),
        ]


class SubjectAnalytics(models.Model):
    """
    Fan bo‘yicha umumiy statistika (GLOBAL)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    subject = models.OneToOneField(
        "subjects.Subject",
        on_delete=models.CASCADE
    )

    total_students = models.PositiveIntegerField(default=0)
    average_score = models.FloatField(default=0)

    updated_at = models.DateTimeField(auto_now=True)
