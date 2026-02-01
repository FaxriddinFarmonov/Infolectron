from celery import shared_task
from django.db.models import Avg, Count

from app.results.models import TestResult, SubjectProgress


@shared_task
def calculate_user_subject_progress(user_id):
    """
    Og‘ir hisob-kitob — Celery’da
    """
    results = (
        TestResult.objects
        .filter(user_id=user_id)
        .select_related("test__lesson__subject")
        .values("test__lesson__subject")
        .annotate(
            avg_score=Avg("score_percent"),
            completed=Count("test"),
        )
    )

    for row in results:
        SubjectProgress.objects.update_or_create(
            user_id=user_id,
            subject_id=row["test__lesson__subject"],
            defaults={
                "average_score": row["avg_score"] or 0,
                "completed_lessons": row["completed"],
            }
        )


from django.db.models import Avg, Count
from app.results.models import TestResult, SubjectAnalytics


@shared_task
def calculate_global_subject_analytics():
    """
    Admin analytics (periodic task)
    """
    data = (
        TestResult.objects
        .select_related("test__lesson__subject")
        .values("test__lesson__subject")
        .annotate(
            avg_score=Avg("score_percent"),
            students=Count("user", distinct=True),
        )
    )

    for row in data:
        SubjectAnalytics.objects.update_or_create(
            subject_id=row["test__lesson__subject"],
            defaults={
                "average_score": row["avg_score"] or 0,
                "total_students": row["students"],
            }
        )
