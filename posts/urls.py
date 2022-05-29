from django.urls import path
from django.views.generic import TemplateView
from .views import IndexView, FeedView, PostDetail, PostCreate, PostUpdate, PostDelete, CommentDelete, post_favorite


app_name ='posts'


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('feed/', FeedView.as_view(), name='feed'),
    path('posts/<int:post_id>', PostDetail.as_view(), name='post-detail'),
    path('posts/<int:post_id>/edit/', PostUpdate.as_view(), name='post-edit'),
    path('posts/<int:post_id>/delete/', PostDelete.as_view(), name='post-delete'),
    path('posts/<int:post_id>/favorite/', post_favorite, name='post-favorite'),
    path('posts/create/', PostCreate.as_view(), name='post-create'),
    path('posts/success/', TemplateView.as_view(template_name='posts/delete_success.html'), name='post-delete-success'),
    path('posts/comment/delete/<int:id>/', CommentDelete.as_view(), name='comment-delete')
]