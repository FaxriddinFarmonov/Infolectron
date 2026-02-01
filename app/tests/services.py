from django.core.cache import cache
from app.tests.models import Question


class TestSessionService:

    @staticmethod
    def start_test(user_id, test_id, questions):
        key = f"test:{user_id}:{test_id}"

        cache.set(
            key,
            {
                "answers": {},
                "questions": [str(q.id) for q in questions],
            },
            timeout=60 * 30  # 30 min
        )

    @staticmethod
    def submit_answer(user_id, test_id, question_id, answer):
        key = f"test:{user_id}:{test_id}"
        data = cache.get(key)

        if not data:
            raise ValueError("Test session expired")

        data["answers"][question_id] = answer
        cache.set(key, data, timeout=60 * 30)

    @staticmethod
    def get_session(user_id, test_id):
        return cache.get(f"test:{user_id}:{test_id}")

    @staticmethod
    def finish_test(user_id, test_id):
        cache.delete(f"test:{user_id}:{test_id}")




class TestResultService:

    @staticmethod
    def calculate_score(questions, answers):
        correct = 0

        question_map = {
            str(q.id): q.correct_answer for q in questions
        }

        for q_id, user_answer in answers.items():
            if question_map.get(q_id) == user_answer:
                correct += 1
        total = len(questions)
        percent = (correct / total) * 100 if total else 0


        return correct, percent,total
