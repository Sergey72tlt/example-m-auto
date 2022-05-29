from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


def user_post_image_path(instance, filename):
    user_id = instance.author.id
    return f'user_{user_id}/posts/{filename}'


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_post_image_path,
                              validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'jpg'])])
    description = models.TextField(max_length=1000, blank=True)
    date_pub = models.DateTimeField(auto_now_add=True)
    date_edit = models.DateTimeField(auto_now=True)
    favorite = models.ManyToManyField(User, blank=True, related_name='favorite_posts')

    @property
    def favorite_count(self):
        return self.favorite.count()

    def __str__(self):
        return f'posts {self.id}, author {self.author.username}'


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.CharField(max_length=50)
    date_pub = models.DateTimeField(auto_now_add=True)
    date_edit = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Author - {self.author.username}, publicated - {self.date_pub}, post - {self.post.description[:15]}...'