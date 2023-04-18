from django.db.models import QuerySet
from django.db.models.signals import post_save
from django.dispatch import receiver

from blog.domain.entities.profile import Profile
from blog.domain.entities.tag import Tag
from blog.domain.repository.tag_repository import ITagRepository


class TagRepository(ITagRepository):
    @staticmethod
    @receiver(post_save, sender=Tag)
    def create(sender, instance, created, **kwargs) -> Tag | None:
        if not created:
            return None

        return Tag.objects.create(
            author=instance.author,
            title=instance.title,
            image_type=instance.image_type,
            image=instance.image,
            short=instance.short,
            body=instance.body
        )

    @staticmethod
    @receiver(post_save, sender=Tag)
    def save(sender, instance, **kwargs) -> None:
        instance.save()

    @staticmethod
    @receiver(post_save, sender=Tag)
    def delete(sender, instance, **kwargs) -> None:
        instance.delete()

    def get_all_profile(self, profile: Profile) -> Tag:
        return Tag.objects.filter()

    def get_all_username(self, username: str) -> Tag:
        pass

    def get_by_id(self, tag_id: int) -> Tag:
        pass

    def get_by_name(self, name: str) -> Tag:
        pass

    def get_all(self) -> QuerySet:
        return Tag.objects.all()