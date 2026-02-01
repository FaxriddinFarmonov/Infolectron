from app.tests.models import Question


def get_test_questions_selector(test_id):
    return (
        Question.objects
        .filter(test_id=test_id)
        .only(
            "id",
            "question_text",
            "option_a",
            "option_b",
            "option_c",
            "option_d",
        )
        .order_by("?")[:20]
    )
