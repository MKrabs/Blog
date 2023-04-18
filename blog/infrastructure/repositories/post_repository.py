from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from blog.domain.entities.post import Post
from blog.domain.repository.post_repository import IPostRepository


class PostRepository(IPostRepository):

    @staticmethod
    @receiver(post_save, sender=Post)
    def create(sender, instance, created, **kwargs) -> Post | None:
        if not created:
            return None

        return Post.objects.create(
            author=instance.author,
            title=instance.title,
            image_type=instance.image_type,
            image=instance.image,
            short=instance.short,
            body=instance.body
        )

    @staticmethod
    @receiver(post_save, sender=Post)
    def save(sender, instance, **kwargs) -> None:
        instance.save()

    @staticmethod
    @receiver(pre_delete, sender=Post)
    def delete(sender, instance, **kwargs) -> None:
        instance.delete()

    def get_by_id(self, post_id) -> Post:
        return Post.objects.get(id=post_id)

    def get_all_from_user(self, user_id: int, order_by: str = None) -> QuerySet:
        return Post.objects.filter(author=user_id).order_by(order_by)

    def get_all(self, order_by: str = None) -> QuerySet:
        return Post.objects.all().order_by(order_by)

    def get_count(self, post_id: int) -> int:
        return self.get_all().count()

    def get_count_by_author(self, user_id: int) -> int:
        return self.get_all_from_user(user_id=user_id).count()
