# services.py

import re
import pdfplumber
from django.db import transaction
from .models import KDBEntry


CODE_PATTERN = re.compile(
    r"""
    ^\s*
    (?:=)?
    (?:\()?
    (?P<code>\d+(?:\.\d+)*)
    (?:\))?
    \s*
    (?P<title>.*)
    """,
    re.VERBOSE,
)


def detect_level(code: str) -> int:
    return code.count(".")


def normalize_text(text: str) -> str:
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


@transaction.atomic
def parse_pdf(pdf_path: str):
    # KDBEntry.objects.all().delete()
    # 🔥 1. PDF o‘qish
    with pdfplumber.open(pdf_path) as pdf:
        lines = []
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                lines.extend(text.split("\n"))

    # 🔥 2. Parse qilish
    parsed_data = {}
    current_code = None
    current_title_lines = []

    def save_current():
        if not current_code:
            return
        parsed_data[current_code] = normalize_text(
            " ".join(current_title_lines)
        )

    for line in lines:
        line = line.strip()
        if not line:
            continue

        match = CODE_PATTERN.match(line)

        if match:
            new_code = match.group("code")

            if current_code:
                save_current()

            current_code = new_code
            current_title_lines = []

            first_part = match.group("title")
            if first_part:
                current_title_lines.append(first_part)

        else:
            if current_code:
                current_title_lines.append(line)

    if current_code:
        save_current()

    # 🔥 3. DB bilan sync
    existing_entries = {
        e.code: e for e in KDBEntry.objects.filter(code__in=parsed_data.keys())
    }

    objects_to_create = []
    objects_to_update = []

    code_instance_map = {}

    # 🔥 4. Create / Update
    for code, title in parsed_data.items():

        level = detect_level(code)

        if code in existing_entries:
            entry = existing_entries[code]
            entry.title = title
            entry.level = level
            objects_to_update.append(entry)
            code_instance_map[code] = entry
        else:
            entry = KDBEntry(
                code=code,
                title=title,
                level=level,
            )
            objects_to_create.append(entry)
            code_instance_map[code] = entry

    # 🔥 5. Bulk create
    KDBEntry.objects.bulk_create(objects_to_create, batch_size=1000)

    # 🔥 6. Parent bog‘lash (ikkinchi pass)
    all_entries = KDBEntry.objects.filter(code__in=parsed_data.keys())
    db_map = {e.code: e for e in all_entries}

    for code, entry in db_map.items():
        parent = None
        if "." in code:
            parent_code = code.rsplit(".", 1)[0]
            parent = db_map.get(parent_code)

        if entry.parent != parent:
            entry.parent = parent
            objects_to_update.append(entry)

    # 🔥 7. Bulk update
    if objects_to_update:
        KDBEntry.objects.bulk_update(
            objects_to_update,
            ["title", "level", "parent"],
            batch_size=1000
        )

    return f"{len(parsed_data)} entries synced successfully"