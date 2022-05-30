from django.test import TestCase
from django.urls import reverse


class TestLoginView(TestCase):
    def test_login_view_200(self):
        response = self.client.get(reverse('core:login'))
        self.assertEqual(response.status_code, 200)

    def test_login_view_content(self):
        response = self.client.get(reverse('core:login'))
        self.assertContains(response, 'Авторизация')