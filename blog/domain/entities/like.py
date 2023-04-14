from django.contrib.auth.models import User
from django.db import models

from blog.domain.entities.post import Post


class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author.username} > {self.post_id}'
