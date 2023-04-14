from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    image_choice = (
        ('iFrame', 'iFrame'),
        ('image', 'image'),
        ('bi-icon', 'bi-icon'),
    )

    author = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True)
    title = models.CharField(max_length=200)
    image_type = models.CharField(max_length=20, choices=image_choice, default='bi-icon')
    image = models.CharField(max_length=500, default='bi-robot')
    short = models.CharField(max_length=255)
    body = models.TextField(max_length=20000)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author} - {self.title}'
