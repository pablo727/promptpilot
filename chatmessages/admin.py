from django.contrib import admin

from .models import ChatMessage


class ChatMessageAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "role",
        "short_message",
        "timestamp",
        "is_flagged",
    )
    search_fields = (
        "user__username",
        "message",
    )
    list_filter = (
        "role",
        "is_flagged",
    )
    readonly_fields = (
        "user",
        "role",
        "timestamp",
    )
    ordering = (
        "-timestamp",
        "role",
    )

    @admin.action(description="Mark selected messages as reviewed")
    def mark_reviewed(self, request, queryset):
        queryset.update(is_flagged=False)

    def short_message(self, obj):
        return obj.message[:100] + "..." if len(obj.message) > 100 else obj.message

    short_message.short_description = "Preview"
    actions = [mark_reviewed]


admin.site.register(ChatMessage)
