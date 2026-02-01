from django.contrib import admin
from app.subjects.models import Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "is_active",
        "created_at",
    )
    list_filter = ("is_active",)
    search_fields = ("title",)
    ordering = ("created_at",)
