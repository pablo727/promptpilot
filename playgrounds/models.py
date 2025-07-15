from django.contrib.auth import get_user_model
from django.db import models

from prompts.models import Prompt


class PromptTestRun(models.Model):
    prompt = models.ForeignKey(
        Prompt, related_name="test_run", on_delete=models.CASCADE
    )
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    input_variables = models.JSONField(default=dict)
    llm_used = models.CharField(max_length=50)
    result = models.TextField()
    tokens_used = models.IntegerField(null=True, blank=True)
    latency_ms = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
