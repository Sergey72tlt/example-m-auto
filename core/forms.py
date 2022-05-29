from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm
from django.contrib.auth.models import User
from django import forms
from posts.widgets import PictureWidget
from .models import Profile


class LoginForm(AuthenticationForm):
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))
    username = UsernameField(label='', widget=forms.TextInput(attrs={'autofocus': True, 'placeholder': 'Username'}))
    error_messages = {'invalid_login': 'Введён неправильный логин или пароль'}


class SignupForm(UserCreationForm):
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'plaseholder': 'Пароль'})
    )

    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'plaseholder': 'Повторите пароль'})
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email-ом уже зарегистрирован')
        return email


DATE_FORMAT = '%d-%m-%Y'


class UpdateProfileForm(forms.ModelForm):
    max_size_img = 3
    birth_date = forms.DateField(label='Дата рождения', input_formats=[DATE_FORMAT],
                                 widget=forms.DateInput(format=(DATE_FORMAT), attrs={'placeholder': 'dd-mm-yyyy'}))

    class Meta:
        model = Profile
        fields = ['avatar', 'birth_date', 'about']
        labels = {
            'about': 'Обо мне',
            'avatar': 'Фото профиля'
        }
        widgets = {
            'avatar': PictureWidget()
        }

    def clean_avatar(self):
        image = self.cleaned_data.get('avatar')
        if image:
            if image.size > self.max_size_img*1024*1024:
                raise forms.ValidationError(f'Файл должен быть меньше {self.max_size_img} мб')
            return image
        else:
            raise forms.ValidationError('Не удалось прочитать файл')
