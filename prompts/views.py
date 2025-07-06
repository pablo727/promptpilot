from rest_framework import viewsets

from .models import Prompt, PromptRating
from .serializers import PromptSerializer, PromptRatingSerializer


class PromptViewSet(viewsets.ModelViewSet):
    queryset = Prompt.objects.all()
    serializer_class = PromptSerializer


class PromptRatingViewSet(viewsets.ModelViewSet):
    queryset = PromptRating.objects.all()
    serializer_class = PromptRatingSerializer
