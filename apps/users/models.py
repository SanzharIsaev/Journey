from django.db import models

from django.contrib.auth.models import User


class FollowUser(models.Model):
    """Модель подписок на пользователей"""
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='following_users'
    )
    
    followed_user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='followers'
    )

    class Meta:
        unique_together = ('user', 'followed_user')
