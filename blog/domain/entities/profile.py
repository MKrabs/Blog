from PIL import Image, ImageOps
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    picture = models.ImageField(blank=True, upload_to='profile_pictures')

    def __str__(self):
        return self.user.username
