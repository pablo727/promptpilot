from django.contrib.auth import get_user_model
from django.test import TestCase

from datetime import datetime

from .models import Prompt, PromptRating
from .serializers import PromptRatingSerializer


class PromptManagerTests(TestCase):
    def test_prompt_str_method(self):

        User = get_user_model()
        user = User.objects.create_user(username="testuser", password="testpass1234")
        long_content = "A" * 60
        prompt = Prompt.objects.create(user=user, content=long_content)
        self.assertEqual(str(prompt), long_content[:50])
        self.assertIsInstance(prompt.created_at, datetime)

    def test_promptrating_str_method(self):
        User = get_user_model()
        user = User.objects.create_user(username="testuser", password="testspass1234")
        prompt = Prompt.objects.create(user=user, content="Some prompt")
        rating = PromptRating.objects.create(
            user=user, prompt=prompt, rating=5, comment="Great!"
        )
        self.assertEqual(str(rating), f"Rating 5 for Some prompt")
        self.assertEqual(rating.rating, 5)
        self.assertEqual(rating.comment, "Great!")
        self.assertIsInstance(rating.created_at, datetime)

    def test_user_rating_prompt(self):
        User = get_user_model()
        user = User.objects.create_user(username="testuser", password="testpass1234")
        prompt = Prompt.objects.create(user=user, content="Some rating")
        rating = PromptRating.objects.create(user=user, prompt=prompt, rating=5)
        self.assertEqual(rating.prompt, prompt)
        self.assertEqual(rating.rating, 5)
        self.assertIsInstance(rating.created_at, datetime)
        self.assertNotEqual(prompt.content, "")

    def test_promptrating_serializer(self):
        User = get_user_model()
        user = User.objects.create_user(username="testuser", password="testpass1234")
        prompt = Prompt.objects.create(user=user, content="Some prompt")

        data = {"user": user.id, "prompt": prompt.id, "rating": 5, "comment": "Nice"}
        serializer = PromptRatingSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        promptrating = PromptRating.objects.create(
            user=user, prompt=prompt, rating=5, comment="Nice comment!"
        )

        self.assertIsInstance(promptrating.created_at, datetime)
