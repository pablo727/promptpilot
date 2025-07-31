from django.contrib import admin

from .models import Prompt, PromptRating


class PromptRatingInline(admin.TabularInline):
    model = PromptRating
    extra = 0
    readonly_fields = (
        "user",
        "rating",
        "comment",
        "created_at",
    )
    ordering = ("-created_at",)


class CustomPromptAdmin(admin.ModelAdmin):
    model = Prompt
    inlines = [PromptRatingInline]
    list_display = (
        "user",
        "short_content",
        "provider",
        "created_at",
        "updated_at",
        "is_public",
    )
    search_fields = ("content", "user__username")
    list_filter = ("provider", "is_public", "created_at")
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    ordering = ("-created_at",)

    def short_content(self, obj):
        content = obj.content
        return content[:60] + "..." if len(content) > 60 else content

    short_content.short_description = "Preview"


admin.site.register(Prompt, CustomPromptAdmin)
