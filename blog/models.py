import math
from random import randint

from PIL import Image, ImageOps
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    picture = models.ImageField(blank=True, upload_to='profile_pictures')

    def save(self, new_image=False, *args, **kwargs):
        super().save()

        if new_image:
            self.user.profile.picture.delete(save=False)

            img = Image.open(self.picture.path)
            img = ImageOps.exif_transpose(img)

            h = img.height
            w = img.width

            if w > h:
                space_start = round((w - h) / 2)
                crop_area = (space_start, 0, space_start + h, h)
            else:
                space_start = round((h - w) / 2)
                crop_area = (0, space_start, w, space_start + w)

            img = img.crop(crop_area)
            img.save(self.picture.path)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, picture=f'profile_pictures/d{randint(1, 10)}.jpg')


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


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

    def __str__(self):
        return self.name


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


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, null=True)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    body = models.TextField(blank=False, null=False)

    def __str__(self):
        return f'{self.author} > {self.post_id} - {self.body[:10]}'


class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author.username} > {self.post_id}'
