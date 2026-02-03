# app/tests/debug_excel.py faylini yarating:

import pandas as pd
from app.tests.models import TestExcel


def analyze_excel_file(excel_id):
    """Excel faylni tahlil qilish"""
    try:
        excel = TestExcel.objects.get(id=excel_id)
        df = pd.read_excel(excel.file.path, dtype=str, keep_default_na=False)

        print("=" * 60)
        print(f"EXCEL FAYL TAFSILOTLARI: {excel.file.name}")
        print("=" * 60)

        print(f"\n📊 UMUMIY MA'LUMOTLAR:")
        print(f"   Jami qatorlar: {len(df)}")
        print(f"   Jami ustunlar: {len(df.columns)}")

        print(f"\n📋 USTUN NOMLARI:")
        for i, col in enumerate(df.columns):
            print(f"   {i + 1:2d}. '{col}'")

        print(f"\n🔍 'to'g'ri javob' USTUNI TAFSILOTLARI:")
        # 'to'g'ri javob' ustunini topish
        correct_col = None
        for col in df.columns:
            if 'togri' in str(col).lower() or 'javob' in str(col).lower():
                correct_col = col
                break

        if correct_col:
            print(f"   Ustun nomi: '{correct_col}'")

            # Bo'sh emas qatorlarni hisoblash
            non_empty = df[correct_col].apply(lambda x: str(x).strip() not in ['', 'nan', 'none'])
            non_empty_count = non_empty.sum()
            empty_count = len(df) - non_empty_count

            print(f"   To'ldirilgan qatorlar: {non_empty_count}")
            print(f"   Bo'sh qatorlar: {empty_count}")

            # Birinchi 5 ta qiymat
            print(f"   Dastlabki 5 ta qiymat:")
            for i in range(min(5, len(df))):
                val = df[correct_col].iloc[i]
                print(f"     {i + 1}. '{val}'")

            # 138-qatordagi qiymat
            if len(df) >= 138:
                print(f"\n   📍 138-QATORDAGI QIYMAT:")
                print(f"     '{df[correct_col].iloc[137]}'")

            # Oxirgi 5 ta qiymat
            print(f"\n   Oxirgi 5 ta qiymat:")
            for i in range(max(0, len(df) - 5), len(df)):
                val = df[correct_col].iloc[i]
                print(f"     {i + 1}. '{val}'")

        print(f"\n📄 DASTLABKI 3 QATOR:")
        print(df.head(3).to_string())

        print(f"\n📄 OXIRGI 3 QATOR:")
        print(df.tail(3).to_string())

        # Bo'sh qatorlarni tekshirish
        print(f"\n⚠️  BO'SH QATORLAR TAFSILOTLARI:")
        empty_rows = []
        for i in range(len(df)):
            row_empty = True
            for col in df.columns:
                if str(df[col].iloc[i]).strip() not in ['', 'nan', 'none']:
                    row_empty = False
                    break
            if row_empty:
                empty_rows.append(i + 2)  # Excel qator raqami (+2 chunki 0-index va sarlavha)

        if empty_rows:
            print(f"   Jami bo'sh qatorlar: {len(empty_rows)}")
            print(f"   Bo'sh qator raqamlari (dastlabki 10 tasi): {empty_rows[:10]}")
            if len(empty_rows) > 10:
                print(f"   ... va yana {len(empty_rows) - 10} ta")
        else:
            print("   Bo'sh qatorlar topilmadi")

        print("\n" + "=" * 60)

    except Exception as e:
        print(f"❌ Xatolik: {str(e)}")

# Terminalda ishlatish:
# python manage.py shell
# >>> from app.tests.debug_excel import analyze_excel_file
# >>> analyze_excel_file('your-excel-uuid')