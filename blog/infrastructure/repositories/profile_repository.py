from random import randint

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from abstraction.image_processor import ImageProcessor
from blog.domain.entities.profile import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        random_default_picture = f'profile_pictures/d{randint(1, 10)}.jpg'
        Profile.objects.create(
            user=instance,
            picture=random_default_picture
        )


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.picture.delete(save=False)
    instance.profile.picture = ImageProcessor.process(instance.profile.picture.path)
    instance.profile.save()
