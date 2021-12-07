from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import *
from django.core.exceptions import ValidationError


# Пример формы, связанной с моделью
class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # преобразование
        self.fields['cat'].empty_label = "Категория не выбрана"
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Review  # Связь с моделью(все поля беруться из нее автоматически)
        fields = ['title', 'slug', 'content', 'is_published', 'photo', 'raiting', 'cat']  # отображаемые поля

        # Собственный валидатор:
        def clean_title(self):
            title = self.cleaned_data['title']
            if len(title) > 200:
                raise ValidationError('Длина превышает 200 символов')
            return title


class RegisterUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # преобразование
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    # Переопределяю методы для нормалього отображения
    username = forms.CharField(label='Логин')
    email = forms.CharField(label='Email')
    password1 = forms.CharField(label='Пароль')
    password2 = forms.CharField(label='Повтор пароля')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # преобразование
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('text',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # преобразование
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
