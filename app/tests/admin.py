# from django.contrib import admin, messages
# from django.shortcuts import redirect
# from django.urls import path
# from django.utils.html import format_html
#
# from .models import Test, Question, TestExcel
# from app.tests.excel_import import import_test_from_excel
#
#
# @admin.register(Test)
# class TestAdmin(admin.ModelAdmin):
#     list_display = ("lesson", "total_questions", "passing_score", "created_at")
#     search_fields = ("lesson__title",)
#
#
# @admin.register(Question)
# class QuestionAdmin(admin.ModelAdmin):
#     list_display = ("short_question", "test", "correct_answer")
#     search_fields = ("question_text",)
#
#     def short_question(self, obj):
#         return obj.question_text[:60]
#
#     short_question.short_description = "Savol"
#
#
# @admin.register(TestExcel)
# class TestExcelAdmin(admin.ModelAdmin):
#     list_display = ("lesson", "file", "is_imported", "created_at", "import_button")
#     list_filter = ("is_imported", "created_at")
#
#     def get_urls(self):
#         urls = super().get_urls()
#
#         custom_urls = [
#             path(
#                 "<uuid:pk>/import/",
#                 self.admin_site.admin_view(self.process_import),
#                 name="testexcel-import",
#             ),
#         ]
#
#         return custom_urls + urls
#
#     def process_import(self, request, pk, *args, **kwargs):
#         obj = self.get_object(request, pk)
#
#         try:
#             import_test_from_excel(obj)
#             self.message_user(
#                 request,
#                 "Excel muvaffaqiyatli import qilindi.",
#                 level=messages.SUCCESS,
#             )
#         except Exception as e:
#             self.message_user(
#                 request,
#                 f"Import xatoligi: {str(e)}",
#                 level=messages.ERROR,
#             )
#
#         return redirect(request.META.get("HTTP_REFERER", "../"))
#
#     def import_button(self, obj):
#         if obj.is_imported:
#             return format_html(
#                 '<span style="color: green; font-weight: bold;">Import qilingan</span>'
#             )
#
#         return format_html(
#             '<a class="button" href="{}/import/">Import qilish</a>',
#             obj.id,
#         )
#
#     import_button.short_description = "Import"


from django.contrib import admin, messages
from django.shortcuts import redirect
from django.urls import path
from django.utils.html import format_html

from .models import Test, Question, TestExcel
from app.tests.excel_import import import_test_from_excel


# =========================
# Question INLINE
# =========================
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0
    fields = (
        "question_text",
        "option_a",
        "option_b",
        "option_c",
        "option_d",
        "correct_answer",
    )
    show_change_link = True


# =========================
# TEST ADMIN
# =========================
@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = (
        "lesson",
        "total_questions",
        "passing_score",
        "created_at",
    )
    search_fields = ("lesson__title",)
    list_filter = ("created_at",)
    inlines = [QuestionInline]
    readonly_fields = ("total_questions", "created_at")

    fieldsets = (
        ("Asosiy ma'lumot", {
            "fields": ("lesson", "passing_score")
        }),
        ("Statistika", {
            "fields": ("total_questions", "created_at")
        }),
    )


# =========================
# QUESTION ADMIN
# =========================
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("short_question", "test", "correct_answer")
    search_fields = ("question_text",)
    list_filter = ("correct_answer", "test")

    def short_question(self, obj):
        return obj.question_text[:70]

    short_question.short_description = "Savol"


# =========================
# TEST EXCEL ADMIN
# =========================
@admin.register(TestExcel)
class TestExcelAdmin(admin.ModelAdmin):
    list_display = (
        "lesson",
        "file",
        "is_imported",
        "created_at",
        "import_button",
    )
    list_filter = ("is_imported", "created_at")
    search_fields = ("lesson__title",)
    readonly_fields = ("is_imported", "created_at")

    # -------- CUSTOM URL --------
    def get_urls(self):
        urls = super().get_urls()

        custom_urls = [
            path(
                "<uuid:pk>/import/",
                self.admin_site.admin_view(self.process_import),
                name="testexcel-import",
            ),
        ]

        return custom_urls + urls

    # -------- IMPORT LOGIC --------
    def process_import(self, request, pk, *args, **kwargs):
        obj = self.get_object(request, pk)

        try:
            import_test_from_excel(obj)

            self.message_user(
                request,
                "✅ Excel muvaffaqiyatli import qilindi.",
                level=messages.SUCCESS,
            )

        except Exception as e:
            self.message_user(
                request,
                f"❌ Import xatoligi: {str(e)}",
                level=messages.ERROR,
            )

        return redirect(request.META.get("HTTP_REFERER", "../"))

    # -------- IMPORT BUTTON --------
    def import_button(self, obj):
        if obj.is_imported:
            return format_html(
                '<span style="color:green; font-weight:600;">Import qilingan</span>'
            )

        return format_html(
            '<a class="button" style="background:#0d6efd; color:white; padding:4px 10px; border-radius:6px;" href="{}/import/">Import</a>',
            obj.id,
        )

    import_button.short_description = "Import"
