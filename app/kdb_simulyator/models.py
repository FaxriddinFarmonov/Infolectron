# models.py

from django.db import models


class KDBUpload(models.Model):
    file = models.FileField(upload_to="kdb/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    processed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Upload {self.id}"

# models.py

class KDBEntry(models.Model):
    code = models.CharField(max_length=50, unique=True)
    title = models.TextField()
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children"
    )
    level = models.IntegerField(db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["code"]