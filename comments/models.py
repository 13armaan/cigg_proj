from django.db import models
from django.conf import settings
from photos.models import Photo

class Comment(models.Model):
    id = models.AutoField(primary_key=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name="comments")

    content = models.TextField()

    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment {self.id} by {self.user}"
