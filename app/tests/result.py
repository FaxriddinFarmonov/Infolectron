# app/tests/services/result.py
class TestResultService:

    @staticmethod
    def calculate_score(questions, answers: dict):
        correct = 0

        for q in questions:
            if str(q.id) in answers and answers[str(q.id)] == q.correct_answer:
                correct += 1

        total = len(questions)
        percent = int((correct / total) * 100) if total else 0

        return correct, percent, total
