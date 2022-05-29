from django import forms
from .models import Post, Comment
from .widgets import PictureWidget


class PostForm(forms.ModelForm):
    max_size_image = 5

    class Meta:
        model = Post
        fields = ('image', 'description')
        labels = {
            'image': 'Фото',
            'description': 'Описание'
        }
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите описание'}),
            # 'image': PictureWidget()
        }

    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            if image.size > self.max_size_image*1024*1024:
                raise forms.ValidationError(f'Фото долно быть меньше {self.max_size_image} мб')
            else:
                return image
        else:
            raise forms.ValidationError('Не удалось прочитать файл')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
