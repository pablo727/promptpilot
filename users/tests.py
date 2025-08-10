from django.contrib.auth import get_user_model
from django.test import TestCase

from .views import CustomUserSignupSerializer


class UsersManagersTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass1234",
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "testuser@example.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username="testsuperuser",
            email="testsuperuser@example.com",
            password="testpass1234",
        )
        self.assertEqual(admin_user.username, "testsuperuser")
        self.assertEqual(admin_user.email, "testsuperuser@example.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    def test_signup(self):
        User = get_user_model()
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpass1234",
            "password2": "testpass1234",
        }

        serializer = CustomUserSignupSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        user = serializer.save()

        self.assertEqual(user.username, data["username"])
        self.assertEqual(user.email, data["email"])
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_login(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="testuser",
            email="testuserexample@example.com",
            password="testpass1234",
        )

        # Test login with the Django test client
        login = self.client.login(username="testuser", password="testpass1234")
        self.assertTrue(login)

        # Access a view that requires login (adjust URL as needed)
        response = self.client.get("/users/home/")
        self.assertEqual(response.status_code, 200)

    def test_failed_login(self):
        response = self.client.post(
            "/login/",
            {
                "username": "wronguser",
                "password": "wrongpass",
            },
        )
        self.assertContains(
            response, "Please enter a correct username and password", status_code=200
        )
