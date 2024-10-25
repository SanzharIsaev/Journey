from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from taggit.managers import TaggableManager
from taggit.models import Tag

from apps.countries.models import Country


def validate_min_length_body(value):
    if len(value) < 3:
        raise ValidationError('Длина текста должна быть не менее 3 символов.')


def validate_image_size(image):
    file_size = image.file.size
    limit_kb = 5 * 1024 * 1024  
    if file_size > limit_kb:
        raise ValidationError("Размер изображения не должен превышать 5 МБ.")
    

class Post(models.Model):
    """Модель постов"""
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )
    
    country = models.ForeignKey(
        Country, 
        on_delete=models.CASCADE,
        related_name='posts'
    )
    
    title = models.CharField(
        max_length=200
    )
    
    body = models.TextField(
        validators=[validate_min_length_body]
    )
    
    tags = TaggableManager(
        blank=True
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    
    is_active = models.BooleanField(
        default=True
    )
    
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class PostImage(models.Model):
    """Модель изображений постов"""
    
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='images'
    )
    
    image = models.ImageField(
        upload_to='images/', 
        validators=[validate_image_size],
        null=True,
        blank=True
    )

    def __str__(self):
        return f'Изображения "{self.post.title}"'


class Likes(models.Model):
    """Модель лайков"""
    
    ip = models.CharField(
        max_length=100,
        verbose_name='IP-адрес'
    )
    
    pos = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )
    

class FollowTag(models.Model):
    """Модель подписки на теги"""
    
    user = models.ForeignKey(
        User, 
        related_name='following_tags', 
        on_delete=models.CASCADE
    )
    
    tag = models.ForeignKey(
        Tag, 
        related_name='followers',
        on_delete=models.CASCADE
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('user', 'tag')

    def __str__(self):
        return f'{self.user.username} -> {self.tag.name}'