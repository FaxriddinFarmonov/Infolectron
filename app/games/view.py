from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from app.games.services.session import get_game_session


class GameStartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, game_id):
        game = get_object_or_404(Game, id=game_id, is_active=True)

        start_game_session(
            user_id=request.user.id,
            game_id=game.id,
            duration=game.time_limit
        )

        return Response({
            "game_id": game.id,
            "time_limit": game.time_limit
        })


class GameSubmitAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, game_id):
        session = get_game_session(request.user.id, game_id)

        if not session:
            return Response(
                {"detail": "Session expired"},
                status=403
            )

        answers = request.data["answers"]

        game = Game.objects.prefetch_related("items").get(id=game_id)

        correct = 0
        for item in game.items.all():
            if str(item.id) in answers:
                if answers[str(item.id)] == item.correct_answer:
                    correct += 1

        score = calculate_score(game, correct, game.items.count())

        end_game_session(request.user.id, game_id)

        return Response({
            "score": score,
            "correct": correct,
            "total": game.items.count()
        })
