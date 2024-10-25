from django import forms
from django.core.exceptions import ValidationError

from .models import Post, PostImage


class PostForm(forms.ModelForm):
    """Форма для создания постов"""

    class Meta:
        model = Post
        fields = ['title', 'body', 'country', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите заголовок'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите текст поста'}),
            'country': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Заголовок',
            'body': 'Текст поста',
            'country': 'Страна',
        }


class PostImageForm(forms.ModelForm):
    """Форма для добавления изображений к посту"""
    
    images = forms.ImageField(
        widget=forms.FileInput(attrs={'multiple': True}),
        required=False,
        label="Загрузить изображения"
    )
    
    class Meta:
        model = PostImage
        fields = ['images']

    def clean_image(self):
        """Проверка количества загружаемых изображений"""
        images = self.cleaned_data.get('images')
        if images:
            # Преобразуем images в список, если передано несколько файлов
            if isinstance(images, list) and len(images) > 10:
                raise ValidationError("Можно загрузить не более 10 изображений.")
        return images