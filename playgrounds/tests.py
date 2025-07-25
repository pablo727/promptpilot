from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from prompts.models import Prompt


class PlaygroundRunTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass1234"
        )
        self.client = APIClient()
        self.run_url = reverse("runprompt-list")

    def test_run_prompt_unauthenticated(self):
        """Should return 401 for anonymous  users"""
        response = self.client.post(self.run_url, {"prompt": "Hello AI"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_run_prompt_authenticated(self):
        """Should return a valid LLM response for authenticated users"""
        self.client.force_authenticate(user=self.user)

        prompt = Prompt.objects.create(
            user=self.user,
            content="What's the capital of Spain?",
            provider="ollama",
            is_public=True,
        )
        response = self.client.post(
            self.run_url,
            {"prompt": prompt.id, "llm": "ollama"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("result", response.data)
        self.assertTrue(len(response.data["result"]) > 0)

    def test_run_prompt_invalid_payload(self):
        """Should return 400 if prompt text is missing"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.run_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
