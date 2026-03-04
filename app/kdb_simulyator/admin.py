from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import redirect
from django.utils.timezone import now

from .models import KDBUpload, KDBEntry
from .services import parse_pdf


@admin.register(KDBEntry)
class KDBEntryAdmin(admin.ModelAdmin):
    list_display = ("code", "title", "created_at")
    search_fields = ("code", "title")


@admin.register(KDBUpload)
class KDBUploadAdmin(admin.ModelAdmin):
    list_display = ("id", "uploaded_at", "processed", "process_button")

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<int:upload_id>/process/",
                self.admin_site.admin_view(self.process_pdf),
                name="kdb-process",
            ),
        ]
        return custom_urls + urls

    def process_button(self, obj):
        if not obj.processed:
            return format_html(
                '<a class="button" href="{}">Process PDF</a>',
                f"{obj.id}/process/",
            )
        return "Already Processed"

    process_button.short_description = "Action"

    def process_pdf(self, request, upload_id):
        upload = KDBUpload.objects.get(pk=upload_id)

        print("🔥 PROCESS BOSHLANDI")

        result = parse_pdf(upload.file.path)

        print("🔥 NATIJA:", result)

        upload.processed = True
        upload.save()

        self.message_user(request, f"Result: {result}")

        return redirect("../../")

