from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.http import HttpResponse
from django.db.models import Count
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Post, Comment
from .forms import PostForm, CommentForm


class IndexView(ListView):
    model = Post
    template_name = 'posts/index.html'
    context_object_name = 'posts'
    LIMIT = 10

    def get_queryset(self):
        queryset = self.model.objects.annotate(favorite_nums=Count('favorite')
                                               ).order_by('-favorite_nums')[:self.LIMIT]
        return queryset


class FavoriteListView(IndexView):

    @method_decorator(login_required(login_url='/admin/'))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.request.user.favorite_posts.all()
        return queryset


class FeedView(IndexView):

    @method_decorator(login_required(login_url='/admin/'))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        friends_list = self.request.user.profile.subscriptions.all()
        queryset = Post.objects.filter(author__in=friends_list)
        return queryset


class PostDetail(DetailView):
    model = Post
    template_name = 'posts/detail.html'
    pk_url_kwarg = 'post_id'
    comment_form = CommentForm
    comment_model = Comment

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=object)
        context['comments'] = self.get_comments()

        if request.user.is_authenticated:
            context['comment_form'] = self.comment_form
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.comment_form(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = self.object
            comment.save()
            form = self.comment_form
        return render(request, self.template_name, context={'post': self.object,
                                                            'comments': self.get_comments(),
                                                            'comment_form': form})

    def get_comments(self):
        post = self.object
        comments = post.comments.all().order_by('-date_pub')
        return comments


class PostCreate(CreateView):
    form_class = PostForm
    template_name = 'posts/create.html'

    @method_decorator(login_required(login_url='/admin/'))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args,  **kwargs)

    @method_decorator(login_required(login_url='/admin/'))
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(reverse('posts:post-detail', kwargs={'post_id': post.id}))
        else:
            return render(request, 'posts/create.html', {'form': form})


class PostDelete(DeleteView):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'posts/delete.html'

    def get_success_url(self):
        return reverse('posts:post-delete-success')


class CommentDelete(DeleteView):
    model = Comment
    pk_url_kwarg = 'id'

    def get_success_url(self):
        comment_id = self.kwargs['id']
        comment = Comment.objects.get(id=comment_id)
        return reverse('posts:post-detail', args=(comment.post.id, ))


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'posts/update.html'
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if self.request.user != obj.author:
            raise PermissionDenied('Вы не являяетесь автором данного объявления')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        image = self.object.image
        description = self.object.description
        form = self.get_form()

        if form.is_valid():
            if image != form.cleaned_data['image'] or description != form.cleaned_data['description']:
                self.object.favorite.clear()
                return self.form_valid(form)
            else:
                return self.form_invalid(form)

    def get_success_url(self):
        post_id = self.kwargs['post_id']
        return reverse('posts:post-detail', args=(post_id, ))


@login_required(login_url='/admin/')
def post_favorite(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    if user in post.favorite.all():
        post.favorite.remove(user)
    else:
        post.favorite.add(user)
        post.save()
    return redirect(request.META.get('HTTP_REFERER'), request)