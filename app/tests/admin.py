from django.contrib import admin, messages
from django.utils.html import format_html
from django.urls import path
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test

from app.tests.models import Test, Question, TestExcel
from app.tests.excel_import import TestExcelImportService


# ===========================
# Question inline (Test ichida)
# ===========================
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    readonly_fields = ("id", "created_at")
    fields = ("question_text", "option_a", "option_b", "option_c", "option_d",
              "correct_answer", "created_at")
    show_change_link = True


# ===========================
# Test admin
# ===========================
@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ("lesson", "total_questions", "passing_score", "created_at", "view_questions")
    list_filter = ("created_at", "lesson__subject")
    search_fields = ("lesson__title",)
    readonly_fields = ("id", "created_at")
    inlines = [QuestionInline]

    def view_questions(self, obj):
        url = reverse('admin:tests_question_changelist') + f'?test__id__exact={obj.id}'
        return format_html(
            '<a class="button" href="{}" style="padding:5px 10px;background:#4CAF50;color:white;'
            'text-decoration:none;border-radius:3px;">👁️ Savollar</a>',
            url
        )

    view_questions.short_description = "Amallar"


# ===========================
# Question admin
# ===========================
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("short_question", "test", "correct_answer", "created_at")
    list_filter = ("test__lesson", "correct_answer", "created_at")
    search_fields = ("question_text", "option_a", "option_b", "option_c", "option_d")
    readonly_fields = ("id", "created_at")
    list_per_page = 20

    def short_question(self, obj):
        return obj.question_text[:100] + "..." if len(obj.question_text) > 100 else obj.question_text

    short_question.short_description = "Savol"


# ===========================
# TestExcel admin (TUZATILGAN VERSIYA)
# ===========================
@admin.register(TestExcel)
class TestExcelAdmin(admin.ModelAdmin):
    list_display = ("lesson", "file_name", "is_imported", "created_at", "import_actions")
    list_filter = ("is_imported", "created_at", "lesson__subject")
    search_fields = ("lesson__title", "file")
    readonly_fields = ("id", "created_at", "is_imported")
    actions = ["import_selected_excels", "mark_as_not_imported"]

    # Admin panelda fayl nomini ko'rsatish (bu admin method)
    def file_name(self, obj):
        if obj.file:
            filename = obj.file.name.split('/')[-1]
            return filename[:30] + "..." if len(filename) > 30 else filename
        return "-"

    file_name.short_description = "Fayl nomi"

    # Import qilish tugmalari
    def import_actions(self, obj):
        if not obj.is_imported:
            return format_html(
                '<a class="button" href="{}" style="padding:5px 10px;background:#4CAF50;color:white;'
                'text-decoration:none;border-radius:3px;margin-right:5px;">📥 Import</a>',
                reverse('admin:import_excel', args=[obj.id])
            )
        else:
            return format_html(
                '<span style="color:green;padding:5px 10px;">✅ Import qilingan</span>'
                '<a class="button" href="{}" style="padding:5px 10px;background:#FF9800;color:white;'
                'text-decoration:none;border-radius:3px;margin-left:10px;">🔄 Qayta</a>',
                reverse('admin:reimport_excel', args=[obj.id])
            )

    import_actions.short_description = "Amallar"

    # ===========================
    # ADMIN ACTIONS (Dropdown'dan tanlash)
    # ===========================

    # TestExcelAdmin class ichiga qo'shing:

    def import_selected_excels(self, request, queryset):
        imported_count = 0
        for excel in queryset:
            if not excel.is_imported:
                try:
                    # Yangi funksiyani chaqiramiz
                    count = TestExcelImportService.import_excel_custom_format(excel)
                    imported_count += 1
                    self.message_user(
                        request,
                        f"✅ {self.file_name(excel)} dan {count} ta savol import qilindi",
                        level=messages.SUCCESS
                    )
                except Exception as e:
                    self.message_user(
                        request,
                        f"❌ {self.file_name(excel)} — xatolik: {e}",
                        level=messages.ERROR
                    )

        if imported_count > 0:
            self.message_user(
                request,
                f"✅ {imported_count} ta Excel fayl muvaffaqiyatli import qilindi",
                level=messages.SUCCESS
            )
    # Action 2: Import holatini bekor qilish
    def mark_as_not_imported(self, request, queryset):
        updated = queryset.update(is_imported=False)
        self.message_user(
            request,
            f"🔄 {updated} ta fayl import qilinmagan holatga o'zgartirildi",
            level=messages.SUCCESS
        )

    mark_as_not_imported.short_description = "🔄 Import holatini bekor qilish"

    # ===========================
    # CUSTOM VIEWS (Tugmalar orqali)
    # ===========================

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<uuid:excel_id>/import/',
                self.import_excel_view,
                name='import_excel',
            ),
            path(
                '<uuid:excel_id>/reimport/',
                self.reimport_excel_view,
                name='reimport_excel',
            ),
        ]
        return custom_urls + urls

    # Import qilish view (dekoratorsiz)
    def import_excel_view(self, request, excel_id):
        # Ruxsatni tekshirish
        if not request.user.has_perm('tests.change_testexcel'):
            messages.error(request, "Sizda bu amalni bajarish uchun ruxsat yo'q")
            return HttpResponseRedirect('../../')

        try:
            excel = TestExcel.objects.get(id=excel_id)

            if excel.is_imported:
                messages.warning(request, "Bu fayl allaqachon import qilingan!")
                return HttpResponseRedirect('../../')

            count = TestExcelImportService.import_excel(excel)
            messages.success(request, f"✅ {count} ta savol import qilindi")

        except Exception as e:
            messages.error(request, f"❌ Xatolik: {str(e)}")

        return HttpResponseRedirect('../../')

    # Qayta import qilish view (dekoratorsiz)
    def reimport_excel_view(self, request, excel_id):
        # Ruxsatni tekshirish
        if not request.user.has_perm('tests.change_testexcel'):
            messages.error(request, "Sizda bu amalni bajarish uchun ruxsat yo'q")
            return HttpResponseRedirect('../../')

        try:
            excel = TestExcel.objects.get(id=excel_id)

            # Avvalgi test savollarini o'chiramiz
            try:
                test = Test.objects.get(lesson=excel.lesson)
                test.questions.all().delete()
                test.total_questions = 0
                test.save()
            except Test.DoesNotExist:
                pass

            # Excel import holatini qaytaramiz
            excel.is_imported = False
            excel.save()

            # Yangidan import qilamiz
            count = TestExcelImportService.import_excel(excel)
            messages.success(request, f"🔄 {count} ta savol qayta import qilindi")

        except Exception as e:
            messages.error(request, f"❌ Xatolik: {str(e)}")

        return HttpResponseRedirect('../../')

    # Excel qo'shganda lesson ni avtomat tanlash
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "lesson" and request.method == "GET":
            # URL'dan lesson_id ni olamiz
            lesson_id = request.GET.get('lesson')
            if lesson_id:
                kwargs["initial"] = lesson_id
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
