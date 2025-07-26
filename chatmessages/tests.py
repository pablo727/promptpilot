from django.contrib.auth import get_user_model
from django.test import TestCase

from datetime import datetime

from .models import ChatMessage
from .serializers import ChatMessageSerializer


class ChatMessageTests(TestCase):
    def test_chatmessage_str_method(self):
        User = get_user_model()
        user = User.objects.create_user(username="testuser", password="testpass1234")
        long_content = "A" * 400
        chatmessage = ChatMessage.objects.create(
            user=user, role="user", message=long_content
        )
        expected_str = f"[{chatmessage.timestamp}] {chatmessage.user} ({chatmessage.role}): {chatmessage.message[:30]}..."
        self.assertEqual(str(chatmessage), expected_str)
        self.assertEqual(chatmessage.role, "user")
        self.assertEqual(chatmessage.message, long_content)
        self.assertIsInstance(chatmessage.timestamp, datetime)

    def test_chatmessage_serializers(self):
        User = get_user_model()
        user = User.objects.create_user(username="testuser", password="testpass1234")
        chatmessage = ChatMessage.objects.create(
            user=user, role="admin", message="Some message"
        )
        data = {"id", "username", "role", "message"}
        serializer = ChatMessageSerializer(instance=chatmessage)
        self.assertEqual(serializer.data["username"], "testuser")
        self.assertEqual(serializer.data["role"], "admin")
        self.assertIn("timestamp", serializer.data)
