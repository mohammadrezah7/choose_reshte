from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from accounts.models import Profile


class DashboardViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="TestPassword123"
        )

        self.profile = Profile.objects.create(
            user=self.user
        )

    def test_dashboard_requires_login(self):
        response = self.client.get(
            reverse("dashboard")
        )

        self.assertEqual(
            response.status_code,
            302
        )

    def test_dashboard_for_authenticated_user(self):
        self.client.login(
            username="testuser",
            password="TestPassword123"
        )

        response = self.client.get(
            reverse("dashboard")
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertTemplateUsed(
            response,
            "dashboard.html"
        )

    def test_profile_is_sent_to_template(self):
        self.client.login(
            username="testuser",
            password="TestPassword123"
        )

        response = self.client.get(
            reverse("dashboard")
        )

        self.assertEqual(
            response.context["profile"],
            self.profile
        )