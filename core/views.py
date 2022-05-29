from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View, DetailView, UpdateView
from django.http import Http404
from django.urls import reverse
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from .forms import LoginForm, SignupForm, UpdateProfileForm
from .models import Profile

MAIN_PAGE_URL = '/'


class LoginView(LoginView):
    template_name = 'core/login.html'
    form_class = LoginForm
    next_page = MAIN_PAGE_URL


class ProfileUpdate(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'core/profile_update.html'
    pk_url_kwarg = 'profile_id'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != request.user:
            raise Http404('Такой страницы нет.')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('core:profile-detail', args=(self.object.id, ))


class SignUpView(View):
    template_name = 'core/signup.html'
    form_class = SignupForm

    def get(self, request, *args, **kwargs):
        context = {
            'form': self.form_class
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(MAIN_PAGE_URL)
        else:
            return render(request, self.template_name, {'form': form})


class ProfileView(DetailView):
    model = Profile
    template_name = 'core/profile.html'
    pk_url_kwarg = 'profile_id'


class SubscribeView(View):
    def post(self, request, user_id, *args, **kwargs):
        profile = get_object_or_404(Profile, user=request.user)
        sub_user = get_object_or_404(User, id=user_id)
        if sub_user in profile.subscriptions.all():
            profile.subscriptions.remove(sub_user)
        else:
            profile.subscriptions.add(sub_user)
        return redirect(request.META.get('HTTP_REFERER'), request)


@login_required
def logout_view(request):
    logout(request)
    return redirect(MAIN_PAGE_URL)