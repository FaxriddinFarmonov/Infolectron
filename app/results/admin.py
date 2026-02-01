from django.contrib import admin
from app.results.models import (
    TestResult,
    SubjectProgress,
    SubjectAnalytics
)


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "test",
        "correct_answers",
        "score_percent",
        "completed_at",
    )
    list_filter = ("completed_at", "test__lesson__subject")
    search_fields = (
        "user__username",
        "test__lesson__title",
        "test__lesson__subject__title",
    )
    readonly_fields = ("id", "completed_at")


@admin.register(SubjectProgress)
class SubjectProgressAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "subject",
        "completed_lessons",
        "average_score",
        "updated_at",
    )
    list_filter = ("subject",)
    search_fields = ("user__username", "subject__title")
    readonly_fields = ("id", "updated_at")


@admin.register(SubjectAnalytics)
class SubjectAnalyticsAdmin(admin.ModelAdmin):
    list_display = (
        "subject",
        "total_students",
        "average_score",
        "updated_at",
    )
    list_filter = ("subject",)
    readonly_fields = ("id", "updated_at")