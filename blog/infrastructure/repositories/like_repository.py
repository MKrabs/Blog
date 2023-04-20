from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from blog.domain.entities.like import Like
from blog.domain.repository.like_repository import ILikeRepository


class LikeRepository(ILikeRepository):
    @staticmethod
    @receiver(post_save, sender=Like)
    def create(sender, instance, created, **kwargs) -> Like | None:
        if created:
            return None

        return Like.objects.create(
            author=instance.author,
            post=instance.post
        )

    @staticmethod
    @receiver(post_save, sender=Like)
    def save(sender, instance, **kwargs) -> None:
        pass

    @staticmethod
    @receiver(pre_delete, sender=Like)
    def delete(sender, instance, **kwargs) -> None:
        pass

    def get_count_post(self, post_id: int) -> int:
        return Like.objects.filter(post=post_id).count()

    def get_count_author(self, author_id: int) -> int:
        return Like.objects.filter(author=author_id).count()

    def did_user_like(self, user_id: int, post_id: int) -> bool:
        return Like.objects.filter(post=post_id, author=user_id)
