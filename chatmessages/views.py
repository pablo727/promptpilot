from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import ChatMessage
from .serializers import ChatMessageSerializer


class ChatMessageViewSet(ModelViewSet):
    queryset = ChatMessage.objects.all().order_by("-timestamp")
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return messages for the current authenticated user
        return ChatMessage.objects.filter(user=self.request.user).order_by("-timestamp")

    def perform_create(self, serializer):
        # Automatically associate the message with the logged-in user
        serializer.save(user=self.request.user)
