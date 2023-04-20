from django.db.models import QuerySet
from django.db.models.signals import post_save
from django.dispatch import receiver

from blog.domain.entities.tag import Tag
from blog.domain.repository.tag_repository import ITagRepository


class TagRepository(ITagRepository):
    @staticmethod
    @receiver(post_save, sender=Tag)
    def create(sender, instance, created, **kwargs) -> Tag | None:
        if created:
            return None

        return Tag.objects.create(
            name=instance.name,
            color=instance.color,
            icon=instance.icon,
            icon_colour=instance.icon_colour,
            link=instance.link,
        )

    @staticmethod
    @receiver(post_save, sender=Tag)
    def save(sender, instance, **kwargs) -> None:
        pass

    @staticmethod
    @receiver(post_save, sender=Tag)
    def delete(sender, instance, **kwargs) -> None:
        pass

    def get_all_user(self, user_id: int) -> Tag:
        pass

    def get_all_username(self, username: str) -> Tag:
        pass

    def get_by_id(self, tag_id: int) -> Tag:
        pass

    def get_by_name(self, name: str) -> Tag:
        pass

    def get_all(self) -> QuerySet:
        return Tag.objects.all()
