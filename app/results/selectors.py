from app.results.models import TestResult, SubjectProgress
from app.results.models import SubjectAnalytics


def user_test_results_selector(user):
    return (
        TestResult.objects
        .filter(user=user)
        .select_related("test__lesson__subject")
        .only(
            "score_percent",
            "test__lesson__title",
            "test__lesson__subject__title",
        )
    )


def user_subject_progress_selector(user):
    return (
        SubjectProgress.objects
        .filter(user=user)
        .select_related("subject")
        .only(
            "subject__title",
            "completed_lessons",
            "average_score",
        )
    )



def admin_subject_analytics_selector():
    return (
        SubjectAnalytics.objects
        .select_related("subject")
        .only(
            "subject__title",
            "total_students",
            "average_score",
        )
        .order_by("-average_score")
    )
