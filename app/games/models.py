import uuid
from django.db import models
from app.lessons.models import Lesson


class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="games"
    )

    title = models.CharField(max_length=255)
    game_type = models.CharField(
        max_length=50,
        choices=[
            ("quiz", "Quiz"),
            ("drag_drop", "Drag & Drop"),
            ("true_false", "True / False"),
        ]
    )

    config = models.JSONField()  # game rules

    created_at = models.DateTimeField(auto_now_add=True)

    

class GameItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name="items"
    )

    question = models.TextField()
    correct_answer = models.JSONField()
    options = models.JSONField(blank=True, null=True)

    order = models.PositiveIntegerField()

    class Meta:
        ordering = ["order"]
        indexes = [
            models.Index(fields=["game"]),
        ]

