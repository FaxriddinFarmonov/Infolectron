from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from app.lessons.models import Lesson, LessonAudio


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "subject",
        "order",
        "has_test",
        "test_questions_count",
        "add_test_excel",
        "is_active",
        "created_at",
    )
    list_filter = ("subject", "is_active")
    search_fields = ("title", "description")
    ordering = ("subject", "order")
    autocomplete_fields = ("subject",)

    # Test borligini ko'rsatish
    def has_test(self, obj):
        return hasattr(obj, 'test') and obj.test is not None

    has_test.short_description = "Test"
    has_test.boolean = True

    # Testdagi savollar soni
    def test_questions_count(self, obj):
        if hasattr(obj, 'test') and obj.test:
            return obj.test.total_questions
        return 0

    test_questions_count.short_description = "Savollar"

    # Excel yuklash/import qilish tugmalari
    def add_test_excel(self, obj):
        # Excel yuklash uchun URL
        add_excel_url = reverse('admin:tests_testexcel_add')

        if hasattr(obj, 'test') and obj.test:
            # Test mavjud bo'lsa
            view_test_url = reverse('admin:tests_test_change', args=[obj.test.id])
            return format_html(
                '<a class="button" href="{}?lesson={}" style="padding:5px 10px;background:#2196F3;color:white;'
                'text-decoration:none;border-radius:3px;margin-right:5px;">📤 Excel yuklash</a>'
                '<a class="button" href="{}" style="padding:5px 10px;background:#4CAF50;color:white;'
                'text-decoration:none;border-radius:3px;">👁️ Testni koʻrish</a>',
                add_excel_url, obj.id,
                view_test_url
            )
        else:
            # Test mavjud bo'lmasa
            return format_html(
                '<a class="button" href="{}?lesson={}" style="padding:5px 10px;background:#2196F3;color:white;'
                'text-decoration:none;border-radius:3px;">📤 Excel yuklash</a>',
                add_excel_url, obj.id
            )

    add_test_excel.short_description = "Test boshqaruvi"


@admin.register(LessonAudio)
class LessonAudioAdmin(admin.ModelAdmin):
    list_display = ("lesson", "duration", "created_at")
    search_fields = ("lesson__title",)
    list_filter = ("created_at",)