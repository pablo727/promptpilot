from rest_framework import serializers
from .models import ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    is_flagged = serializers.BooleanField(read_only=True)

    class Meta:
        model = ChatMessage
        fields = [
            "id",
            "username",
            "role",
            "message",
            "timestamp",
            "is_flagged",
        ]
        read_only_fields = [
            "id",
            "timestamp",
            "is_flagged",
        ]
