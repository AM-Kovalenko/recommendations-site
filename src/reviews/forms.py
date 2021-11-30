from django import forms
from .models import *
from django.core.exceptions import ValidationError


# Пример формы, не связанной с моделью
# class AddPostForm(forms.Form):
#     title = forms.CharField(max_length=255, label='Заголовок')
#     slug = forms.SlugField(max_length=255, label="URL")
#     content = forms.CharField(widget=forms.Textarea(attrs={'cols':60,'rows':10}), label="Контент")
#     is_published = forms.BooleanField(label="Публикация", required=False, initial=True)
#     cat = forms.ModelChoiceField(queryset=Category.objects.all(), label="Категории")

# Пример формы, связанной с моделью
class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = "Категория не выбрана"

    class Meta:
        model = Review  # Связь с моделью(все поля беруться из нее автоматически)
        fields = ['title', 'slug', 'content', 'is_published', 'raiting', 'cat']  # отображаемые поля


        # Собственный валидатор:
        def clean_title(self):
            title = self.cleaned_data['title']
            if len(title) > 200:
                raise ValidationError('Длина превышает 200 символов')
            return title