from random import randint

from PIL import Image, ImageOps
from django.contrib.auth.models import User
from django.db import models
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
