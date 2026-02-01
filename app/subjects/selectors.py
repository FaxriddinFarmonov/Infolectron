from app.subjects.models import Subject


def subject_list_selector():
    """
    Faqat active fanlar
    Juda tez, cache-friendly
    """
    return (
        Subject.objects
        .filter(is_active=True)
        .only("id", "title", "description")
        .order_by("created_at")
    )
