# from django.conf.urls import url
from django.urls import path, reverse_lazy
from django.contrib.auth.views import (PasswordResetView, PasswordResetDoneView,
                                       PasswordResetConfirmView, PasswordResetCompleteView)
from .views import LoginView, SignUpView, ProfileView, SubscribeView, ProfileUpdate, logout_view

app_name = 'core'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('sign-up/', SignUpView.as_view(), name='sign_up'),
    path('logout/', logout_view, name='logout'),
    path('profile/<int:profile_id>/', ProfileView.as_view(), name='profile-detail'),
    path('profile/<int:profile_id>/update/', ProfileUpdate.as_view(), name='profile-update'),
    path('subscribe/<int:user_id>', SubscribeView.as_view(), name='subscribe'),

    path('password_reset/', PasswordResetView.as_view(template_name='core/password_reset.html',
                                                      success_url=reverse_lazy('core:password-reset-done'),
                                                      email_template_name='core/password_reset_email.html'
                                                      ), name='password-reset'),

    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='core/password_reset_done.html'
                                                               ), name='password-reset-done'),
    path('password_reset/<str:uidb64>/<slug:token>/',
         PasswordResetConfirmView.as_view(success_url=reverse_lazy('password-reset-complete'),
                                          template_name='core/password_reset_confirm.html'
                                          ), name='password_reset_confirm'),

    path('password_reset/complete/', PasswordResetCompleteView.as_view(
                                                                       template_name='core/password_reset_complete.html'
                                                                       ), name='password-reset-complete')
]