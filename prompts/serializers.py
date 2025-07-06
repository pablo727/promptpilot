from rest_framework import serializers

from .models import Prompt, PromptRating


class PromptRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromptRating
        fields = [
            "prompt",
            "user",
            "rating",
            "comment",
            "created_at",
        ]

    def validate(self, data):
        user = data["user"]
        prompt = data["prompt"]
        if PromptRating.objects.filter(user=user, prompt=prompt).exists():
            raise serializers.ValidationError("You have already rated this prompt.")
        return data


class PromptSerializer(serializers.ModelSerializer):
    ratings = PromptRatingSerializer(many=True, read_only=True)

    class Meta:
        fields = (
            "user",
            "content",
            "created_at",
            "updated_at",
            "is_public",
            "ratings",
        )
        model = Prompt

    def create(self, validated_data):
        return Prompt.objects.create(**validated_data)
