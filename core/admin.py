from django.contrib import admin
from .models import Profile, UserPhoto


class PhotoInline(admin.TabularInline):
    model = UserPhoto


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    inlines = [
        PhotoInline
    ]