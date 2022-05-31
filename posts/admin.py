from django.contrib import admin
from .models import Post, Comment, COMMENT_STATUSES


class CommentInLine(admin.TabularInline):
    model = Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Main Info', {'fields': ['author', 'image']}),
        ('Other Info', {'fields': ['description', 'favorite_count']}),
        ('Date Info', {'fields': ['date_pub', 'date_edit']}),
    ]
    readonly_fields = ['date_pub', 'favorite_count', 'date_edit']

    inlines = [CommentInLine]


def comment_set_publicated_status(modeladmin, request, queryset):
    for comment in queryset:
        comment.status = COMMENT_STATUSES[2][0]
        comment.save()

def comment_set_moderation_status(modeladmin, request, queryset):
    for comment in queryset:
        comment.status = COMMENT_STATUSES[0][0]
        comment.save()


def comment_set_archive_status(modeladmin, request, queryset):
    for comment in queryset:
        comment.status = COMMENT_STATUSES[1][0]
        comment.save()


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Main Info', {'fields': ['author', 'post', 'text', 'status']}),
        ('Date Info', {'fields': ['date_pub', 'date_edit']}),
    ]
    readonly_fields = ['date_pub', 'date_edit']
    list_display = ('author', 'date_pub', 'text', 'date_edit', 'status')
    list_filter = ('author', 'date_pub', 'status')
    search_fields = ('author__username', 'text')
    actions = [comment_set_publicated_status, comment_set_moderation_status, comment_set_archive_status]