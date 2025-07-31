from django.contrib import admin

from .models import PromptTestRun


class PromptTestRunAdmin(admin.ModelAdmin):
    model = PromptTestRun
    list_display = (
        "user",
        "input_variables",
        "llm_used",
        "result",
        "tokens_used",
        "latency_ms",
        "created_at",
    )
    search_fields = ("result", "user__username")
    list_filter = ("input_variables", "llm_used", "created_at")
    readonly_fields = ("llm_used", "tokens_used", "latency_ms", "created_at")
    ordering = ("-created_at", "llm_used")


admin.site.register(PromptTestRun)
