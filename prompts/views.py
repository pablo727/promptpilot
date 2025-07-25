from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import Q

from .models import Prompt, PromptRating
from .serializers import PromptSerializer, PromptRatingSerializer


class PromptViewSet(viewsets.ModelViewSet):
    queryset = Prompt.objects.all()
    serializer_class = PromptSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        return {"request": self.request}

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Prompt.objects.filter(Q(is_public=True) | Q(user=self.request.user))
        return Prompt.objects.filter(is_public=True)


class PromptRatingViewSet(viewsets.ModelViewSet):
    queryset = PromptRating.objects.all()
    serializer_class = PromptRatingSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {"request": self.request}
