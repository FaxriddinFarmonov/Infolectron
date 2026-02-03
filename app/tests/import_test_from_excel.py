# Papka struktura:
# app/tests/management/commands/import_excel.py

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from app.tests.models import TestExcel
from app.tests.excel_import import TestExcelImportService


class Command(BaseCommand):
    help = "Yuklangan Excel faylidan test import qilish"

    def add_arguments(self, parser):
        parser.add_argument("--excel_id", type=str, required=True,
                            help="Import qilish uchun Excel fayl ID si")

    def handle(self, *args, **options):
        try:
            excel = TestExcel.objects.get(id=options["excel_id"])
        except TestExcel.DoesNotExist:
            raise CommandError(f"❌ {options['excel_id']} ID ga ega Excel topilmadi")

        try:
            # Import qilamiz
            count = TestExcelImportService.import_excel(excel)

            self.stdout.write(
                self.style.SUCCESS(f"✅ {count} ta savol muvaffaqiyatli import qilindi")
            )

        except Exception as e:
            raise CommandError(f"❌ Import qilishda xatolik: {str(e)}")