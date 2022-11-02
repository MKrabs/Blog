from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Tag(models.Model):
    colour_choices = (
        ("primary", "primary"),
        ("secondary", "secondary"),
        ("success", "success"),
        ("danger", "danger"),
        ("warning", "warning"),
        ("info", "info"),
        ("light", "light"),
        ("dark", "dark"),
    )

    name = models.CharField(
        max_length=50
    )
    color = models.CharField(
        max_length=10,
        choices=colour_choices,
        default="dark"
    )
    icon = models.CharField(
        max_length=20,
        null=True
    )
    icon_colour = models.CharField(
        max_length=6,
        default="000000"
    )
    link = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )


class Post(models.Model):
    image_choice = (
        ('iFrame', 'iFrame'),
        ('image', 'image'),
        ('bi-icon', 'bi-icon'),
    )

    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, null=True)
    title = models.CharField(max_length=200)
    image_type = models.CharField(max_length=20, choices=image_choice, default='bi-icon')
    image = models.CharField(max_length=500, default='bi-robot')
    short = models.CharField(max_length=255)
    body = models.TextField(max_length=20000)
    pub_date = models.DateTimeField('date published')


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, null=True)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    time = models.DateTimeField('posted on')
    body = models.TextField(blank=False, null=False)


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=20000)
    image = models.ImageField()
    last_updated = models.DateTimeField('last updated')
