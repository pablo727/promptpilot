from rest_framework import serializers
from .models import PromptTestRun


class PromptTestRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromptTestRun
        fields = "__all__"
        read_only_fields = ("result", "tokens_used", "latency_ms", "created_at")
