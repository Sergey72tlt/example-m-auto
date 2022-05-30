from django.test import TestCase
import datetime
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class TestProfileModel(TestCase):
    def setUp(self):
        user = User(username='qwerty', email='qwerty@qwerty.com')
        user.set_password('qwerty')
        user.save()
        return super().setUp()

    def test_birth_date(self):
        with self.assertRaises(ValidationError):
            user = User.objects.first()
            user.profile.birth_date = datetime.datetime.now().date()
            user.profile.save()