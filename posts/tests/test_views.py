import os
from django.test import TestCase
from django.contrib.auth.models import User
from core.models import Profile
from django.urls import reverse
import codecs
from django.core.files.uploadedfile import SimpleUploadedFile
from ..models import Post


class TestFeedView(TestCase):
    def setUp(self):
        dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(dir, 'static', 'img', 'testimage.jpg')
        file_obj = codecs.open(image_path, encoding='base64')
        image = SimpleUploadedFile(file_obj.name, file_obj.read())

        self.test_user1 = User.objects.create(username='test1', email='test@test.com', password='test')
        self.test_user2 = User.objects.create(username='test2', email='test1@test.com', password='test')

        post = Post.objects.create(author=self.test_user1, image=image)
        return super().setUp()

    def test_feed_blank_content(self):
        self.client.login(username='test1', password='test')
        response = self.client.get(reverse('posts:index'))
        self.assertIn('posts', response.context)