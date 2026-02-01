from django.contrib import admin
from app.tests.models import Test, Question


# Inline class: Test ichida savollarni ko‘rsatish
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1  # yangi savollar qo‘shish uchun satrlar soni
    readonly_fields = ("id",)
    show_change_link = True


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ("lesson", "total_questions", "passing_score", "created_at")
    list_filter = ("created_at",)
    search_fields = ("lesson__title",)
    readonly_fields = ("id",)
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "test", "correct_answer")
    list_filter = ("test", "correct_answer")
    search_fields = ("question_text", "test__lesson__title")
    readonly_fields = ("id",)