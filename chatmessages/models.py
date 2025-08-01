from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=10, choices=[("user", "User"), ("assistant", "Assistant")]
    )
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_flagged = models.BooleanField(default=True)

    def __str__(self):
        return f"[{self.timestamp}] {self.user.username} ({self.role}): {self.message[:30]}..."
