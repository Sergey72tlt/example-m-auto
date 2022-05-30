import os
from django.test import TestCase
from django.contrib.auth.models import User
from core.models import Profile
from django.urls import reverse
from ..models import Post


class TestFeedView(TestCase):
    def setUp(self):
        dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(dir, 'static', 'img', 'testimage.jpg')
        self.test.user1 = User.objects.create(username='test1', email='test@test.com', password='test')
        self.test.user2 = User.objects.create(username='test2', email='test1@test.com', password='test')
        return super().setUp()