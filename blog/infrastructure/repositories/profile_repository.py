from random import randint

from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.db.models.signals import post_save
from django.dispatch import receiver

from blog.domain.entities.profile import Profile
from blog.domain.repository.profile_repository import IProfileRepository


class ProfileRepository(IProfileRepository):

    @staticmethod
    @receiver(post_save, sender=User)
    def create(sender, instance, created, **kwargs):
        if created:
            random_default_picture = f'profile_pictures/d{randint(1, 10)}.jpg'
            Profile.objects.create(
                user=instance,
                picture=random_default_picture
            )

    @staticmethod
    @receiver(post_save, sender=User)
    def save(sender, instance, **kwargs):
        instance.profile.save()

    def get_by_id(self, user_id: int) -> Profile:
        user = User.objects.get(id=user_id)
        return Profile.objects.get(user=user)

    def get_by_username(self, username: str) -> Profile:
        user = User.objects.get(username=username)
        return Profile.objects.get(user=user)

    def get_all(self) -> QuerySet:
        return Profile.objects.all()

    def add_additional_fields(self, profile: Profile) -> None:
        pass
