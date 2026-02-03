import pandas as pd
from django.db import transaction
from app.tests.models import Test, Question, TestExcel

# Javob xaritasi
ANSWER_MAP = {
    "1": "A", "2": "B", "3": "C", "4": "D",
    "A": "A", "B": "B", "C": "C", "D": "D",
    "a": "A", "b": "B", "c": "C", "d": "D",
    "а": "A", "б": "B", "в": "C", "г": "D",
}


class TestExcelImportService:
    """
    Excel fayldan test savollarini import qilish uchun servis
    """

    @staticmethod
    @transaction.atomic
    def import_excel(excel: TestExcel):
        """
        Excel fayl ma'lumotlarini o'qib, test va savollarni yaratadi
        Bo'sh qatorlarni avtomat o'tkazib yuboradi
        """
        # Agar oldin import qilingan bo'lsa
        if excel.is_imported:
            raise ValueError("Bu Excel allaqachon import qilingan")

        # Excel faylni o'qiymiz
        try:
            # Barcha ustunlarni string sifatida o'qiyapmiz
            df = pd.read_excel(excel.file.path, dtype=str, keep_default_na=False)
        except Exception as e:
            raise ValueError(f"Excel faylni o'qishda xatolik: {str(e)}")

        if df.empty:
            raise ValueError("Excel fayli bo'sh")

        # Ustun nomlarini tozalash
        df.columns = [str(col).strip() for col in df.columns]

        print(f"Excel fayli: {excel.file.name}")
        print(f"Jami qatorlar: {len(df)}")
        print(f"Ustunlar: {df.columns.tolist()}")

        # Kerakli ustunlarni topish
        question_col = None
        correct_col = None
        option_cols = []

        for col in df.columns:
            col_str = str(col)
            col_lower = col_str.lower()

            # Savol ustuni
            if 'savol' in col_lower and not question_col:
                question_col = col

            # To'g'ri javob ustuni (turli yozilishlari uchun)
            elif any(keyword in col_lower for keyword in
                     ['togri', 'to\'g\'ri', 'to‘g‘ri', 'javob', 'answer']) and not correct_col:
                correct_col = col

            # Variant ustunlari (A, B, C, D harflari bilan)
            elif col_str.upper() in ['A', 'B', 'C', 'D']:
                option_cols.append(col)

        # Agar A, B, C, D harflari bilan ustunlar topilmasa
        if len(option_cols) < 4:
            # Raqamlar bilan (1, 2, 3, 4) variantlarni qidirish
            for i in range(1, 5):
                for col in df.columns:
                    if str(col).strip() == str(i):
                        option_cols.append(col)

        # Agar hali ham 4 ta ustun topilmasa
        if len(option_cols) < 4:
            # Boshqa ustunlardan 4 tasini tanlash
            other_cols = [col for col in df.columns if
                          col not in [question_col, correct_col] and col not in option_cols]
            option_cols.extend(other_cols[:4 - len(option_cols)])

        # Tekshirish
        if not question_col:
            raise ValueError(f"Excel'da 'Savol' ustuni topilmadi. Mavjud ustunlar: {df.columns.tolist()}")

        if not correct_col:
            raise ValueError(f"Excel'da 'to'g'ri javob' ustuni topilmadi. Mavjud ustunlar: {df.columns.tolist()}")

        if len(option_cols) < 4:
            raise ValueError(f"Excel'da 4 ta variant ustuni kerak. Faqat {len(option_cols)} ta topildi: {option_cols}")

        print(f"Topilgan ustunlar:")
        print(f"  Savol: '{question_col}'")
        print(f"  To'g'ri javob: '{correct_col}'")
        print(f"  Variantlar: {option_cols}")

        # Testni yaratish
        test, created = Test.objects.get_or_create(
            lesson=excel.lesson,
            defaults={"total_questions": 0}
        )

        if not created:
            test.questions.all().delete()

        questions = []
        empty_rows_count = 0
        error_rows = []

        for index, row in df.iterrows():
            try:
                # Savol matni
                question_text = str(row[question_col]).strip()

                # Agar savol bo'sh bo'lsa, qatorni o'tkazib yuboramiz
                if not question_text or question_text.lower() in ['', 'nan', 'none', 'null', '-', '--']:
                    empty_rows_count += 1
                    continue

                # To'g'ri javob
                raw_answer = str(row[correct_col]).strip()

                # Agar to'g'ri javob bo'sh bo'lsa, qatorni o'tkazib yuboramiz
                if not raw_answer or raw_answer.lower() in ['', 'nan', 'none', 'null', '-', '--']:
                    error_rows.append(f"{index + 2}-qator: To'g'ri javob bo'sh")
                    continue

                # .0 bilan tugasa (1.0, 2.0 kabi)
                if raw_answer.endswith(".0"):
                    raw_answer = raw_answer[:-2]

                # Katta harfga o'tkazamiz
                raw_answer = raw_answer.upper().strip()
                correct_answer = ANSWER_MAP.get(raw_answer)

                if not correct_answer:
                    error_rows.append(
                        f"{index + 2}-qator: Noto'g'ri javob '{raw_answer}'. Iltimos, 1,2,3,4 yoki A,B,C,D kiriting.")
                    continue

                # Variantlar
                option_a = str(row[option_cols[0]]).strip() if option_cols[0] in row and not pd.isna(
                    row[option_cols[0]]) else ""
                option_b = str(row[option_cols[1]]).strip() if len(option_cols) > 1 and option_cols[
                    1] in row and not pd.isna(row[option_cols[1]]) else ""
                option_c = str(row[option_cols[2]]).strip() if len(option_cols) > 2 and option_cols[
                    2] in row and not pd.isna(row[option_cols[2]]) else ""
                option_d = str(row[option_cols[3]]).strip() if len(option_cols) > 3 and option_cols[
                    3] in row and not pd.isna(row[option_cols[3]]) else ""

                # Agar variantlar bo'sh bo'lsa
                if not option_a:
                    error_rows.append(f"{index + 2}-qator: A variant bo'sh")
                    continue

                # Savolni yaratish
                questions.append(
                    Question(
                        test=test,
                        question_text=question_text,
                        option_a=option_a,
                        option_b=option_b,
                        option_c=option_c,
                        option_d=option_d,
                        correct_answer=correct_answer,
                    )
                )

            except Exception as e:
                error_rows.append(f"{index + 2}-qator: {str(e)}")
                continue

        print(f"Topilgan savollar: {len(questions)}")
        print(f"Bo'sh qatorlar: {empty_rows_count}")

        # Agar xatolar juda ko'p bo'lsa (5% dan ortiq)
        total_rows = len(df)
        if error_rows and len(error_rows) > total_rows * 0.05:
            # Faqat birinchi 10 ta xatoni ko'rsatamiz
            first_errors = error_rows[:10]
            error_msg = "; ".join(first_errors)
            if len(error_rows) > 10:
                error_msg += f" ... va yana {len(error_rows) - 10} ta xato"
            raise ValueError(f"{len(error_rows)} ta xato topildi: {error_msg}")
        elif error_rows:
            # Agar oz xato bo'lsa, faqat ogohlantirish beramiz
            print(f"Ogohlantirishlar ({len(error_rows)} ta):")
            for err in error_rows[:5]:
                print(f"  {err}")

        # Agar savollar bo'lmasa
        if not questions:
            raise ValueError("Hech qanday savol import qilinmadi")

        # Barcha savollarni bir vaqtda bazaga saqlaymiz
        Question.objects.bulk_create(questions, batch_size=500)

        # Testdagi savollar sonini yangilaymiz
        test.total_questions = len(questions)
        test.save(update_fields=["total_questions"])

        print(f"✅ {len(questions)} ta savol muvaffaqiyatli import qilindi")
        if empty_rows_count > 0:
            print(f"ℹ️  {empty_rows_count} ta bo'sh qator o'tkazib yuborildi")
        if error_rows:
            print(f"⚠️  {len(error_rows)} ta qatorda xatolar bor (lekin import davom ettirildi)")

        # Excel import qilingan deb belgilaymiz
        excel.is_imported = True
        excel.save(update_fields=["is_imported"])

        return len(questions)   