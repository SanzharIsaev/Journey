from django.db import models
from django.contrib.auth.models import User


class Country(models.Model):
    """Модель стран"""
    
    name = models.CharField(
        max_length=120
    )
    
    description = models.TextField()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'


class FollowCountry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_countries')
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'country')