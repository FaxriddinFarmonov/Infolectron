import openpyxl
from django.db import transaction

from app.tests.models import Test, Question


REQUIRED_COLUMNS = [
    "Savol",
    "A",
    "B",
    "C",
    "D",
    "Togri javob",  # faqat oddiy ASCII
]


def import_test_from_excel(test_excel):
    """
    TestExcel faylidan savollarni o'qib,
    Test va Question bazasini to'ldiradi.
    """

    workbook = openpyxl.load_workbook(test_excel.file.path, data_only=True)
    sheet = workbook.active

    # Headerlarni olish
    headers = [str(cell.value).strip() if cell.value else "" for cell in sheet[1]]

    if headers != REQUIRED_COLUMNS:
        raise ValueError(
            f"Excel ustunlari noto'g'ri.\n"
            f"Kutilgan: {REQUIRED_COLUMNS}\n"
            f"Topilgan: {headers}"
        )

    with transaction.atomic():
        # Test yaratish yoki olish
        test, _ = Test.objects.get_or_create(lesson=test_excel.lesson)

        questions_to_create = []

        for row in sheet.iter_rows(min_row=2, values_only=True):
            if not any(row):
                continue

            question_text, a, b, c, d, correct = row

            correct = str(correct).strip().upper()

            if correct not in {"A", "B", "C", "D"}:
                raise ValueError(f"Noto'g'ri javob qiymati: {correct}")

            questions_to_create.append(
                Question(
                    test=test,
                    question_text=str(question_text).strip(),
                    option_a=str(a).strip(),
                    option_b=str(b).strip(),
                    option_c=str(c).strip(),
                    option_d=str(d).strip(),
                    correct_answer=correct,
                )
            )

        # Eski savollarni o'chiramiz
        test.questions.all().delete()

        # Yangi savollarni bulk yaratamiz
        Question.objects.bulk_create(questions_to_create, batch_size=500)

        # Test statistikasi
        test.total_questions = len(questions_to_create)
        test.save(update_fields=["total_questions"])

        # Excel import bo'lganini belgilash
        test_excel.is_imported = True
        test_excel.save(update_fields=["is_imported"])
