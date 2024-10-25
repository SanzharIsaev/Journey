from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    """Форма для добавления комментариев"""
    
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите ваш комментарий'}),
        }
        
        labels = {
            'content': '',
        }