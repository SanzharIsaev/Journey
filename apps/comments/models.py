from django.db import models
from django.contrib.auth.models import User
from apps.posts.models import Post

class Comment(models.Model):
    """Модель комментариев"""
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Комментарий от {self.user.username} на пост {self.post.title}'
