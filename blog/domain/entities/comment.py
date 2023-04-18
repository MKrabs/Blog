from django.contrib.auth.models import User
from django.db import models

from blog.domain.entities.post import Post


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    body = models.TextField(blank=False, null=False)

    def __str__(self):
        return f'{self.author} > {self.post_id} - {self.body[:10]}'
