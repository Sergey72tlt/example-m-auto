from django.db import models
from django.contrib.auth.models import User


def user_avatar_path(instance, filename):
    user_id = instance.user.id
    return f'user_{user_id}/avatar/{filename}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    birth_date = models.DateField(blank=True, null=True)
    about = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to=user_avatar_path)
    subscriptions = models.ManyToManyField(User, blank=True, related_name='subscribers')

    def __str__(self):
        return f'Profile of {self.user.username}'

    def get_subscribers_count(self):
        """Количество пользователей подписавшихся на пользователя"""
        subscribers_count = self.user.subscribers.count()
        return subscribers_count

    def get_subscriptions_count(self):
        """Количество пользователей на которых подписан пользователь"""
        subscriptions_count = self.subscriptions.count()
        return subscriptions_count


class UserPhoto(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='gallery')
